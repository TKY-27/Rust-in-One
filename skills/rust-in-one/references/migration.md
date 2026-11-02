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

Agree which foreign components may remain in the delivered system. A wrapper around the old implementation does not satisfy a requirement to replace it.

## 2. Characterize before translating

Build a differential harness early. It runs the reference build and the Rust build on the same inputs and compares stdout, stderr, exit status, and output files. Feed it:

- the existing tests and real sample data;
- edge cases: empty input, huge input, boundary numbers, invalid and non-ASCII bytes, CRLF line endings, very long lines and tokens, missing and unreadable files, a directory where a file is expected;
- generated inputs from a property-based generator or a simple random generator with a fixed seed.

Keep the harness and the reference binary out of the shipped crate, for example as a dev-only test that is skipped when the reference binary is absent, or as a script.

Separate intended behavior from defects. When the source has a bug, undefined behavior, or nondeterminism, decide explicitly whether to preserve the observable behavior or fix it. For a requested drop-in replacement, preservation is the default; deviate only where preserving would be unsound or silently lose data. Ask the user only when the choice is consequential and the request does not settle it. Record each accepted difference and its reason, and do not copy a suspected bug into expected outputs without that decision. Documented quirks such as truncation limits, separator rules, and rounding are part of the contract.

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
| `std::map` / `std::unordered_map` | `BTreeMap` (ordered iteration) / `HashMap` (random iteration order) |
| Hand-written hash tables and containers | std collections unless measurement shows a need |
| `char*` text treated as bytes | `&[u8]`/`Vec<u8>`. Use `str` only if the input is guaranteed UTF-8 |

## 4. Semantic traps

- **Integers**: signed overflow is UB in C and C++, while Rust panics in debug builds and wraps in release builds; make the intended semantics explicit with `wrapping_*`/`checked_*`. Shifts by at least the bit width are UB in C, panic in debug Rust, and mask the shift amount in release. `i32::MIN / -1` always panics in Rust. `long` is 64-bit on 64-bit Linux and macOS but 32-bit on Windows, `char` is signed on x86 and unsigned on ARM Linux, and `size_t` arithmetic wraps. Use fixed-width Rust types that match the actual ranges.
- **Parsing numbers**: `atoi`, `strtol`, and `sscanf` accept leading whitespace and a `+` sign; `atoi` returns 0 on garbage, and `strtol` reports overflow only through `errno`. Rust's `str::parse` accepts `+` but rejects whitespace and trailing characters. Match the source's accepted inputs where they are part of the interface.
- **Text and I/O**: `BufRead::lines()` and `str::lines()` strip `\r\n` as well as `\n` and reject invalid UTF-8, whereas `fgets` keeps `\r` and accepts any bytes. Process bytes when the source does. Rust's `io::Error` displays as `No such file or directory (os error 2)`, so if scripts parse the source's `strerror` messages, format the message from `io::Error::kind()` or `raw_os_error()` deliberately.
- **Process behavior**: these are part of a drop-in contract, and scripts using `set -o pipefail` or checking `$?` observe them.
  - Before `main` runs, Rust sets SIGPIPE to ignored, so `tool | head` yields an `EPIPE` write error instead of death by signal (status 141 in shells). To match a C tool, restore the default disposition first thing in `main`: `unsafe { libc::signal(libc::SIGPIPE, libc::SIG_DFL) }`, with a `SAFETY:` comment. This small FFI call is justified, and forbidding `unsafe` crate-wide is not a reason to diverge.
  - Rust also reopens closed standard descriptors on `/dev/null` before `main`, so `tool <&-` reads empty input where C reports `EBADF`. Matching that needs an `#![no_main]` entry point. Usually record it as an accepted difference unless something depends on it.
  - C code often ignores `printf` and `fflush` failures (for example, `> /dev/full` still exits 0), while idiomatic Rust reports them. Decide which behavior the contract requires, and report the choice either way.
- **Floating point**: Rust's `{}` prints the shortest round-trip representation, which differs from C's `%g`. Use explicit precision (`{:.6}`) or replicate `%g` when output must match. Fixed-precision formatting (`{:.2}` against `%.2f`) rounds identically on the common glibc toolchain, but verify against the reference. C compilers may contract `a*b+c` into FMA (GCC's default outside strict ISO mode on FMA-capable targets) or be built with `-ffast-math`; Rust never does this implicitly (`mul_add` is explicit). Check the source's build flags before treating small numeric differences as bugs.
- **Ordering and determinism**: `qsort` and `std::sort` are unstable, while Rust's `sort` is stable. With incomplete comparators, equal elements can come out in a different order, so make the comparator total. Iteration order of the source's hash tables leaks into output surprisingly often. Reproduce it only if it is part of the contract, and otherwise define an order. If outputs depend on a PRNG (`rand()`, `std::mt19937`), reproduce the exact generator when sequences must match.
- **Memory and lifetime**: code that relied on UB (use-after-free, reading uninitialized memory, out-of-bounds reads) may have produced "working" outputs. Treat those as defects to decide on, not behavior to imitate.
- **Concurrency**: map C++ memory orders exactly rather than defaulting everything to `SeqCst` or `Relaxed`. Do not replace a lock-free structure with a `Mutex`, or the reverse, without checking progress and performance requirements. A C++ object shared between threads without synchronization is a data race to fix, not a design to copy.

## 5. Choose a transition strategy

- **Whole replacement**: suits small to medium, self-contained components with a good characterization harness. It is simplest to verify and leaves no FFI in the end state.
- **Incremental replacement through FFI**: suits large systems. Replace leaf modules with narrow interfaces first, keep both builds and the differential harness green at every step, and remove each bridge once its module is replaced. Use `bindgen` for calling C, `cbindgen` for exposing Rust to C, `cxx` for C++ interop, and the `cc` crate in `build.rs` to compile remaining C/C++. Read [unsafe-ffi.md](unsafe-ffi.md) before writing the boundary.
- Replace the build and packaging integration too: Makefile and CMake targets, install rules, and packaging scripts. Otherwise the migration is not usable.

## 6. Performance and completion

- Measure the original with its shipped compiler flags on representative inputs, on the same machine, after confirming both versions produce the same output. Follow [performance.md](performance.md). If the original uses SIMD intrinsics or platform-specific paths, provide equivalent Rust paths (`std::arch` with runtime feature detection) or show that portable code meets the requirement.
- The migration is complete when the inventory is covered or each gap is agreed and documented; the differential suite passes, and the Rust build also has its own tests that remain useful after the C/C++ is deleted; build and packaging work without the old code, unless it is agreed to remain; and performance requirements are met with measurements.
- Report covered behavior, accepted differences with reasons, remaining foreign components, measured performance against the original, and verification gaps.
