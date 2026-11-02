---
name: rust-in-one
description: Engineering workflow and Rust-specific defaults for delivering complete, verified Rust software from a short request. Use when the user wants to build a new Rust program, library, or service (including before any Cargo.toml exists); extend, fix, review, optimize, or finish an existing Rust codebase; or migrate C, C++, or other code to Rust. Also use for the Rust parts of mixed-language repositories and when resuming long Rust work after a context reset. Do not use when no Rust is involved, and do not choose Rust for a request whose language is undecided just because this skill is available.
license: MIT
---

# Rust-in-One

Deliver the Rust software the user asked for: working, verified, and built from decisions an experienced Rust engineer would defend. You own the technical decisions; the user owns the product scope.

## Scale the process to the task

- **Small change** (bug fix, small feature, review comment): read the affected code and its tests, fix the cause, add or adjust a test, run the project's checks, report. Skip planning documents, continuation notes, and independent review unless the change touches unsafe code, concurrency, security-sensitive input handling, a public API, or a persisted format.
- **New project or substantial feature**: follow every section below.
- **Migration to Rust**: follow every section below, and open [references/migration.md](references/migration.md) before studying the source in detail. It defines the contract inventory, the differential testing against the original build, and the C/C++ semantic traps that drive the work.

If the user has not chosen a language, this skill does not choose it. Pick the language from the product's needs and the user's environment; continue with this skill only if that is Rust. In a mixed-language repository, apply it only to the Rust parts.

Follow the host's permissions and instruction files (AGENTS.md, CLAUDE.md, CONTRIBUTING, CI configuration). Where the host or another skill already provides planning, task tracking, review, or verification, use that instead of duplicating it, and reuse its valid evidence for the same revision.

## 1. Pin down the product

Before designing, read the request, the repository's instructions, `Cargo.toml` (edition, `rust-version`, features, workspace), `rust-toolchain.toml`, the existing code, tests, and CI. Then establish:

- Who uses the result and how: CLI, library, service, embedded component, or part of a larger system.
- Inputs and their trust level, outputs and their consumers, and which formats, interfaces, and behaviors are compatibility commitments.
- Target platforms, scale, and any performance, memory, or latency requirements.
- What must happen on bad input, missing resources, partial failure, and interruption.

Turn these answers into a short checklist of observable requirements. Verification and review are checked against it, so keep it in your working state.

In an existing project, build it and run its checks before changing anything. Note pre-existing failures and warnings so you neither hide them nor mistake them for regressions. Follow its conventions (error crates, layout, test style, MSRV), and keep unrelated reformatting and refactoring out of the diff. When asked to finish or improve it, list what is incomplete: `todo!`/`unimplemented!`/TODO markers, failing or ignored tests, README claims the code does not meet, and unhandled error paths.

Resolve ordinary technical choices yourself: crates, layout, error strategy, test approach. Ask only when an unanswered product question would materially change the result and has no reasonable default, or when an action exceeds your authorization. Otherwise state the assumption and proceed. Do not shrink the requested scope silently.

## 2. Make one real path work early

Build the thinnest end-to-end path through a real boundary before adding breadth: the CLI processing a real input file and printing real output; an integration test calling the library's public API the way a consumer would; a service answering a real request through its router. Spike risky assumptions first, such as format details, a crate's actual capabilities, or feasibility of a performance target. Then grow in increments that each keep the build green and add tests.

## 3. Engineering defaults

Deviate when the project's conventions or a stated requirement say otherwise.

**Project setup**
- Check `cargo --version` first. If no toolchain is installed, install one through rustup when you are authorized to; otherwise say that builds and checks could not run. Never present unbuilt code as working.
- Create crates with `cargo new` / `cargo init`. Current Cargo defaults to edition 2024 and no longer ignores `Cargo.lock`; keep the edition and commit the lockfile. Edition 2024 requires `unsafe extern` blocks and `#[unsafe(no_mangle)]`, makes `std::env::set_var` unsafe, and reserves `gen`.
- Add dependencies with `cargo add name [-F feature]` so versions are real. Do not write version numbers or feature names from memory. When unsure of an API, or when a compile error suggests a different major version, read the docs for the locked version: docs.rs, or the crate source under `~/.cargo/registry/src/`.
- A binary with real logic gets a library target: modules under `src/lib.rs`, with `src/main.rs` limited to argument parsing, wiring, and exit codes. Use a workspace only for crates with genuinely separate roles.
- Put lint settings in the `[lints]` table. Set `rust-version` only for crates others will build, and verify it.

**Types and ownership**
- Model the domain with types: enums for closed sets of states instead of flag combinations or strings, newtypes for identifiers and units, and validating constructors at input boundaries so inner code can rely on invariants.
- Long-lived structs own their data. Functions borrow (`&str`, `&[T]`, `&Path`) and return owned values. Put lifetimes on structs only for short-lived views or zero-copy parsing that pays for itself.
- When fighting the borrow checker, restructure before cloning: split borrows, separate data from behavior, or store indices into a `Vec` instead of references (graphs, parent links, caches). `Rc<RefCell<_>>` webs and blanket `Arc<Mutex<_>>` usually mean ownership was never designed.
- Keep visibility minimal (`pub(crate)` by default). Do not add traits, generics, builders, or configuration for hypothetical future needs.
- In libraries every public item is a compatibility commitment. Expose dependency types only deliberately, mark public enums and structs that may grow `#[non_exhaustive]`, and implement the common traits (`Debug`, `Clone`, `PartialEq`, `Default`) where they make sense.

**Gotchas that commonly produce wrong programs**
- `HashMap`/`HashSet` iteration order is randomized per process. Wherever order is observable (output, serialization, tests, hashing), use `BTreeMap`, sort explicitly, or use an insertion-ordered map. Give every sort an explicit tie-breaker.
- `String` must be UTF-8; files, logs, process output, and paths need not be. `read_to_string` fails on invalid UTF-8, and `BufRead::lines()` yields an `Err` for such a line, so `?` aborts the whole run. Decide the policy (bytes, lossy, skip and count, or error) and use `Path`/`OsStr` for file names. String slicing panics off a char boundary, and `len()` counts bytes.
- Integer overflow panics in debug builds and silently wraps in release builds. Use `checked_*`, `saturating_*`, or wider types where input controls magnitudes (sizes, offsets, counts, durations); use `u64`, not `usize`, for byte totals. `as` silently truncates or saturates, so use `TryFrom` for narrowing untrusted values. Sort floats with `total_cmp`.
- Rust ignores SIGPIPE, so `println!` panics when the reader goes away (`tool | head`). CLIs that write substantial output should write through `BufWriter::new(io::stdout().lock())`, propagate write errors, and treat `ErrorKind::BrokenPipe` as a normal exit; a drop-in replacement for an existing tool should match that tool's status instead (see [references/migration.md](references/migration.md)). Call `flush()` explicitly, because `BufWriter` ignores errors on drop. `std::process::exit` skips destructors and loses unflushed output, so return `ExitCode` from `main` instead.
- Returning `Err` from `main` prints the error's `Debug` form and exits with status 1. That reads acceptably for `anyhow::Error` but badly for derived `Debug` output. User-facing CLIs should print a clear message to stderr and choose exit codes deliberately.
- Tests run in parallel threads of one process. Tests that change environment variables, the current directory, or other global state interfere with each other, so pass configuration explicitly instead.
- `std::sync::LazyLock`/`OnceLock` replace `lazy_static`/`once_cell`. Prefer std where it covers the need.

**Errors and panics**
- Libraries expose their own error type (an enum implementing `std::error::Error`, usually via `thiserror`, `#[non_exhaustive]` if it may grow) and never print or exit. Applications use `anyhow` (or an equivalent) and attach context naming the operation and input (path, line, URL) at each boundary.
- Panics are for bugs. Bad input, I/O failure, and network errors are `Result`s. No `unwrap()` on input-controlled values; `expect("why this cannot fail")` documents a real invariant.

**Dependencies**
- Default choices when a crate is warranted: `clap` (derive) for nontrivial CLIs, `serde`/`serde_json` for serialization, `thiserror`/`anyhow` for errors, `tokio` for async I/O, `axum` for HTTP services, `reqwest` for HTTP clients, `tracing` for service logs, `rayon` for data parallelism, `regex`, and `tempfile`/`proptest`/`criterion` for tests and benchmarks. Never hand-roll cryptography, TLS, or parsers for complex standard formats.
- Enable only the features you use (no `tokio/full` in libraries). Do not add a crate for a few lines of code or for style.

**Concurrency, unsafe, performance**
- Use async only for I/O concurrency such as servers, many connections, or concurrent requests. Use threads or `rayon` for CPU-bound work, and plain synchronous code for ordinary file processing. Read [references/concurrency.md](references/concurrency.md) before writing a service, async code, or nontrivial multithreading.
- Use unsafe code only for FFI or a measured need with no safe alternative, behind a small safe API. Read [references/unsafe-ffi.md](references/unsafe-ffi.md) before writing any `unsafe` or FFI code.
- Design for stated performance requirements from the start: stream rather than load whole inputs, avoid per-item allocation in hot loops, buffer I/O. Measure only release builds. A performance claim needs measurements on representative and worst-case inputs (for example, high-cardinality data as well as typical data), compared under the same conditions. Read [references/performance.md](references/performance.md) before benchmarking, optimizing, or making any performance claim.

**Code and documentation**
- Comments explain why: invariants, safety arguments, non-obvious decisions. They do not narrate code. Delivered paths contain no `todo!()`, stubs, placeholder data, or commented-out code.
- Write the documentation users need: what the program does, prerequisites (Rust via rustup), build/install/run commands, real examples, configuration, and limitations. Public library items get rustdoc with an example. Run every command you document.

## 4. Verify against the requirements

For every change, run the project's own checks, or this baseline when it has none:

```sh
cargo fmt --all --check
cargo clippy --workspace --all-targets --all-features -- -D warnings
cargo test --workspace --all-features
```

`cargo test` without target flags includes doctests, but `--all-targets` excludes them. If features are mutually exclusive, test the meaningful combinations instead of `--all-features`.

Then gather evidence for each requirement and its likely failure modes:
- Test behavior, not just compilation. Cover each checklist item plus empty, malformed, boundary, oversized, and non-UTF-8 input; missing files and permissions; and errors from dependencies.
- CLI integration tests run the real binary through `env!("CARGO_BIN_EXE_<name>")` in `tests/`, with no extra crate needed, checking stdout, stderr, and exit status.
- Build the release artifact and use it the way the user will: real inputs, piped input and output, and the documented commands.
- For a migration, run the original build and the Rust build on the same inputs throughout, comparing stdout, stderr, exit status, and output files.

For substantial work, read [references/verification.md](references/verification.md) for product-specific checks, property and fuzz testing, library packaging, and delivery checks. Fix causes rather than symptoms, add a regression test for each defect, and rerun the checks on the integrated result.

## 5. Get an independent review for substantial or risky work

New projects, substantial features, migrations, and any work involving unsafe code, FFI, concurrency, untrusted input, authentication, or persisted formats require a review before delivery.

- Prefer a reviewer with fresh context: a subagent, separate session, or person, whatever the host provides. Give them the original request, the requirements checklist, build and run commands, and the artifact (path, commit, or diff). Do not give them your assessment, your test summary as a conclusion, your continuation notes, or a list of areas you believe are fine. Ask them to find defects with severity and evidence, such as a reproducer or a concrete code path, not to confirm quality.
- If no independent reviewer is available, do a separate adversarial pass: reread the request and the full diff from scratch, try to break the main and failure paths, and call it a self-review in your report.
- Wait for the review to finish before delivering. Verify each finding by reproducing it or refuting it with evidence. Fix material findings at the cause, add regression tests, and recheck the integrated result. Favorable opinions do not close a finding; evidence does. Report unresolved disagreements instead of dropping them.

## 6. Keep continuation state on long tasks

When work may outlast the context window or be resumed later, keep a short state note: goal, requirements checklist, key decisions and reasons, invariants, done/in progress/next, verification status, open findings. Keep it where it survives a context reset but is not part of the deliverable or of what reviewers see: the host's task or plan facility, its scratch directory, or an untracked path listed in `.git/info/exclude`. Do not put task state into instruction files such as AGENTS.md or CLAUDE.md.

After a context reset or on resumption, reread this skill and any reference you rely on. Then reconcile the note with the repository (`git status`, `git log`, build, tests) before editing. Where they disagree, the repository wins.

## 7. Deliver

- Recheck the requirements checklist. Nothing may be silently dropped, stubbed, or replaced by a temporary bridge.
- Run the final checks on the final revision, then build and exercise the artifact users receive: installed binary, packaged crate, or deployed configuration.
- Remove task-only notes, scratch files, debug output, and temporary data. Confirm `git status` shows only intended changes, and preserve existing documentation and instructions.
- Report concisely: what was built or changed; how to build, install, and use it; which checks ran and their results; what was not verified; and known limitations, accepted behavior differences, and unresolved findings. If any scope or necessary verification is incomplete, say so and list what remains.
