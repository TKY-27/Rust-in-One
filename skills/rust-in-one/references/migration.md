# Migrating C, C++, and other code to Rust

Read this before deciding what to replace, how to stage it, or what counts as compatible.

## 1. Inventory the contract

Pin the source revision, build it with its normal release flags, and run its tests. Then list everything users or other systems depend on:

- Command-line syntax, including option permutation, attached values (`-n5`), `--`, and `-` for stdin; exit codes; stdout content and order; stderr messages that scripts may parse.
- File formats, network protocols, byte order, alignment and padding of binary data, text encoding, line endings.
- Library API or ABI: function signatures, ownership of returned memory, thread-safety, callbacks, error reporting (`errno`, return codes, exceptions).
- Environment variables, configuration files, locale, time zones, signals.
- Performance envelope: throughput, latency, memory, startup time, measured on representative workloads.
- Supported platforms and toolchains.

Determine from the request which foreign components may remain in the delivered system. Ask the user only when an unresolved consequential choice has no reasonable default. A wrapper around the old implementation does not satisfy a requirement to replace it.

## 2. Characterize before translating

Build a differential harness early. It runs the reference build and the Rust build on the same inputs and compares stdout, stderr, exit status, and output files. Feed it:

- the existing tests and real sample data;
- edge cases: empty input, huge input, boundary numbers, invalid and non-ASCII bytes, CRLF line endings, very long lines and tokens, missing and unreadable files, a directory where a file is expected;
- generated inputs from a property-based generator or a simple random generator with a fixed seed.

Keep the reference binary and task-only differential harness outside the published package, or exclude them explicitly in Cargo packaging metadata and check `cargo package --list`. A dev-only integration test or script is not automatically excluded from the crate archive. Keep reusable Rust regression tests that do not need the old build.

Identify which source behavior is part of the contract, including documented quirks and permitted nondeterminism. For a drop-in replacement, preserve defined behavior by default, including documented quirks such as truncation limits, separator rules, and rounding. Undefined behavior has no portable output contract; replace it with safe, defined behavior rather than reproducing memory unsafety. When resolving a source bug, nondeterminism, or undefined behavior changes observable results, ask the user only if the choice is consequential and the request does not settle it. Record each accepted difference and its reason, and do not copy a suspected source bug into expected test outputs without an explicit decision.

## 3. Design for Rust, not line-by-line

Understand the source's data model, ownership, and state transitions first, then map them to idiomatic constructs:

| Source construct | Usual Rust design |
| --- | --- |
| Class hierarchy with a closed set of variants | `enum` with `match` |
| Open extension through virtual methods | trait, used generically or as `dyn Trait` |
| Pointer graphs, parent pointers, intrusive lists | indices into a `Vec` (arena), or `Weak` for back-references |
| `shared_ptr` everywhere | single ownership plus borrowing. Use `Rc`/`Arc` only where ownership is really shared |
| Exceptions and error codes | `Result` with a typed error. Panic only for bugs |
| Null pointers and sentinel values | `Option` |
| Out-parameters | return values, tuples, or structs |
| Tagged unions | `enum` |
| Global mutable state | an explicit context struct passed where needed |
| Macros for constants and generic code | `const`, generics, functions. Use `macro_rules!` only when necessary |
| `std::map` / `std::unordered_map` | `BTreeMap` (ordered iteration) / `HashMap` (unspecified iteration order) |
| Hand-written hash tables and containers | std collections unless measurement shows a need |
| `char*` text treated as bytes | `&[u8]`/`Vec<u8>`. Use `str` only if the input is guaranteed UTF-8 |

## 4. Semantic traps

- **Integers**: signed overflow is UB in C and C++, while Rust's ordinary arithmetic overflow follows configured checks (default Cargo debug panics, release wraps); make the intended semantics explicit with `wrapping_*`/`checked_*`. In C/C++, a shift count that is negative or at least as large as the width of the promoted left operand causes undefined behavior. In Rust, negative or out-of-range shift counts are overflow conditions controlled by the overflow-check settings; use checked or wrapping shifts to state the intended policy. Signed `MIN / -1` and `MIN % -1` always panic for Rust's ordinary `/` and `%`, even when overflow checks are disabled. `long` is 64-bit on 64-bit Linux and macOS but 32-bit on Windows, plain `char` signedness depends on target and compiler flags, and `size_t` arithmetic wraps. Use fixed-width Rust types that match the actual ranges.
- **Lexical rules**: compare the actual source parser and stream rules, not similar-looking API names. Whitespace sets, signs, prefixes, locale, partial-token acceptance, and range failures differ even between C/C++ APIs. Generate boundary inputs for each class; Rust ASCII/Unicode helpers are not automatically equivalent to the source's character classification.
- **Parsing numbers**: `atoi`, `strtol`, and numeric `sscanf` conversions accept leading whitespace and a `+` sign. `atoi` does not provide reliable error reporting; `strtol` reports range errors through `errno == ERANGE` with a saturated return value. Rust's `str::parse` accepts `+` but rejects whitespace and trailing characters. Match the source's accepted inputs where they are part of the interface.
- **Text and I/O**: `BufRead::lines()` strips `\r\n` as well as `\n` and can fail on invalid UTF-8. `str::lines()` also strips those delimiters but operates on already-valid UTF-8 and has no decoding error, whereas POSIX or binary-mode `fgets` retains `\r` and does not validate UTF-8. C text-mode translation is platform-dependent: Windows CRT commonly translates CRLF and treats Ctrl-Z as EOF. Process bytes when the source does. An OS-backed `io::Error` can display text such as `No such file or directory (os error 2)`. If scripts depend on the source's `strerror` messages, reproduce the required target-specific text deliberately; neither `io::Error` nor `ErrorKind` formatting guarantees a match.
- **Process behavior**: signal handling, standard descriptors, and exit statuses are part of a drop-in contract, and scripts using `set -o pipefail` or checking `$?` observe them.
  - On Unix, Rust's default standard-library startup ignores `SIGPIPE`, so a broken-pipe write returns `EPIPE` instead of terminating the process. If the compatibility contract requires termination by `SIGPIPE`, restore `SIG_DFL` in platform-gated setup before starting work and check for setup failure. Otherwise preserve the source's signal policy.
  - On some Unix targets Rust's startup sanitizes closed standard descriptors, so `tool <&-` can differ from the reference before application code runs. Verify the target behavior. Exact parity may need platform-specific startup work; do not prescribe `#![no_main]` as a portable fix or silently accept a difference in a drop-in contract.
  - C code often ignores `printf` and `fflush` failures (for example, `> /dev/full` still exits 0), while idiomatic Rust reports them. Decide which behavior the contract requires, and report the choice either way. Exercise small and large output with real failing stdout destinations: buffering and process-exit flushing can change status even when a unit test with an injected failing writer passes.
- **Floating point**: Rust's `{}` prints the shortest round-trip representation, which differs from C's `%g`. Rust `{:.6}` is not a replacement for C `%g`'s significant-digit and exponent-selection rules. Match the required format deliberately, including signed zero, non-finite values, locale, and rounding, and verify against the reference. C compilers may contract `a*b+c` into FMA (GCC's default outside strict ISO mode on FMA-capable targets), or the source may be built with `-ffast-math`. Check the Rust compiler/target flags too; `mul_add` explicitly requests fused semantics. Check the source's build flags before treating small numeric differences as bugs.
- **Ordering and determinism**: `qsort` and `std::sort` are unstable, while Rust's `sort` is stable. With incomplete comparators, equal elements can come out in a different order, so preserve defined tie behavior or establish an explicit deterministic policy; adding a tie-breaker can itself break compatibility. Iteration order of the source's hash tables leaks into output surprisingly often. Reproduce it only if it is part of the contract, and otherwise define an order. If outputs depend on a PRNG (`rand()`, `std::mt19937`), reproduce the exact generator when sequences must match.
- **Memory and lifetime**: code that relied on UB (use-after-free, reading uninitialized memory, out-of-bounds reads) may have produced "working" outputs. Treat those as defects to decide on, not behavior to imitate.
- **Concurrency**: preserve the synchronization and progress argument rather than mechanically translating memory-order names or defaulting everything to `SeqCst` or `Relaxed`. Do not replace a lock-free structure with a `Mutex`, or the reverse, without checking progress and performance requirements. Fix data races in the source (concurrent conflicting accesses, at least one non-atomic, without a happens-before relationship). Sharing immutable data alone is not a data race.

## 5. Choose a transition strategy

- **Whole replacement**: suits small to medium, self-contained components with a good characterization harness. It is simplest to verify and leaves no FFI in the end state.
- **Incremental replacement through FFI**: suits large systems. Replace leaf modules with narrow interfaces first, keep both builds and the differential harness green at every step, and remove each bridge once its module is replaced. Use `bindgen` for calling C, `cbindgen` for exposing Rust to C, `cxx` for C++ interop, and the `cc` crate in `build.rs` to compile remaining C/C++. Read [unsafe-ffi.md](unsafe-ffi.md) before writing the boundary.
- Replace the build and packaging integration too: Makefile and CMake targets, install rules, and packaging scripts. Otherwise the migration is not usable.

## 6. Performance and completion

- Measure the original with its shipped compiler flags on representative inputs, on the same machine, after confirming both versions meet the agreed correctness contract. Follow [performance.md](performance.md). If the original uses SIMD intrinsics or platform-specific paths, provide equivalent Rust paths (`std::arch` with runtime feature detection) or show that portable code meets the requirement.
- The migration is complete when:
  - the contract inventory is covered, or each remaining gap is explicitly accepted by the user and documented;
  - the differential suite passes, and the Rust build has standalone tests that remain useful after the original source code is removed;
  - build and packaging succeed without the old code (except for foreign components explicitly permitted to remain); and
  - performance requirements are met and verified with measurements.
- Report covered behavior, accepted differences with reasons, remaining foreign components, measured performance against the original, and verification gaps.
