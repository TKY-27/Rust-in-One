---
name: rust-in-one
description: Build and verify new Rust CLIs, libraries, and services; migrate C/C++ or other software to Rust with explicit compatibility and performance checks; fix, extend, review, or optimize existing Rust code. Applies before Cargo.toml exists and when resuming Rust work. Use only for Rust work, including Rust components of mixed repositories. Do not choose Rust merely because this skill is available when the language is undecided.
license: MIT
---

# Rust-in-One

Deliver the requested behavior with defensible Rust engineering decisions and evidence from the artifact users receive. Follow the user's scope and the host's permissions and repository instructions. Reuse planning, verification, and review supplied by the host or another skill; do not duplicate valid work for the same revision.

## Choose the scope and checks

- **New project or substantial feature:** identify the observable requirements, build one real end-to-end path, then expand and verify it.
- **Migration:** first read [migration.md](references/migration.md). Establish the source behavior and performance baseline before designing the Rust replacement. A wrapper is not a native migration unless the user requested one.
- **Focused fix:** inspect the affected code and tests, reproduce the defect, make the smallest coherent correction, and run relevant checks. No planning document or extra reviewer by default. Escalate review when the *changed behavior* has material safety, security, concurrency, persistence, or compatibility risk.

Read existing instructions, Cargo manifests, toolchain pins, and CI. Preserve edition, MSRV, features, conventions, and unrelated edits. Run relevant baseline checks in existing projects; distinguish pre-existing failures from regressions. For a new project, check the available toolchain and choose a supported edition and layout.

Write a short observable checklist: inputs, outputs, failure behavior, public interfaces, platforms, and any resource constraints. Resolve routine technical choices yourself. Ask only when an unresolved product choice materially changes the result and has no reasonable default. Do not silently reduce scope.

For substantial work, read the relevant product row and checks in [verification.md](references/verification.md) **while planning the first working path**, not only at delivery. Read additional references at their triggers below, and reassess those triggers when the design changes: an initially safe rewrite can acquire an FFI boundary. A link in this file is not loaded reference content: open the relevant file before relying on it; if unavailable, report that limit and use primary documentation.

## Build a real path early

Exercise a real CLI input/output, a library call from outside the crate, or a request through the service's actual transport. Test risky assumptions early: format details, external API usability, dependency capabilities, cancellation, and performance feasibility. Add breadth in buildable increments.

Choose the smallest useful design:

- Use `cargo new` / `cargo init` when appropriate. Keep a lockfile for reproducible development; published library consumers resolve their own dependency graph. Set and verify `rust-version` when promising an MSRV. Do not change existing compatibility policy incidentally.
- Separate reusable logic from CLI wiring when it improves testing or reuse; a small binary need not have a library target. Use workspaces for genuinely separate crates.
- Verify dependency versions and features through Cargo, the existing lockfile, or registry/docs; `cargo add` is convenient, not mandatory. Read docs or source for the resolved version when uncertain. Respect offline and vendored builds.
- Prefer private items, borrow inputs when useful, and choose owned results or borrowed views according to lifetime and allocation needs. Use enums and validating constructors for meaningful invariants; avoid abstractions for hypothetical needs.
- Before cloning to satisfy the borrow checker, consider smaller borrow scopes, splitting fields, or indices into an arena. Shared ownership and locks are legitimate when the design needs them.
- Treat public types as API decisions. `#[non_exhaustive]` permits evolution but restricts downstream construction and exhaustive matching; provide constructors/accessors and test a separate consumer. Add traits such as `Debug`, `Clone`, or `Default` only when their semantics fit.
- Return useful errors. Libraries normally return errors rather than printing or exiting; typed errors are useful when callers need to distinguish cases. Applications may use `anyhow` or simpler errors. Attach operation/input context at boundaries. Invalid input and I/O failures are not reasons to panic.

## Rust pitfalls to check

- **Observable order:** hash collection iteration is unspecified. Sort when deterministic output is required; define tie behavior where it affects results. Do not add a new tie-breaker that changes a compatibility contract.
- **Bytes and text:** `String` requires UTF-8; files, process output, and paths may not. Decide whether to reject, preserve, or transform invalid bytes. Use `Path`/`OsStr` for paths. String length is bytes and slicing requires character boundaries.
- **Arithmetic:** default Cargo profiles check ordinary integer overflow in debug and wrap in release, but flags can change this; division/remainder by zero and signed MIN / -1 still panic. Use checked, saturating, or wrapping operations to express the required behavior. Validate narrowing conversions with `TryFrom`; choose count/offset widths from the format and platform contract. Define a NaN policy before ordering floats (`total_cmp` provides a total order).
- **CLI output:** propagate write and explicit `flush()` failures; `BufWriter` drop ignores them. For ordinary filter CLIs, handle `BrokenPipe` without a panic. A migration must match its source's output/error/status contract. Return a deliberate exit status and readable stderr; `Result` from `main` prints errors with `Debug`, and `process::exit` skips destructors.
- **Global state:** tests run concurrently. Prefer injected configuration or subprocess tests over mutating environment/current directory in-process. Edition 2024 makes `std::env::set_var`/`remove_var` unsafe; a test mutex alone does not constrain other threads or foreign code.
- **Crates:** use maintained parsers and cryptography rather than inventing them. Common options include `clap`, `serde`, `thiserror`/`anyhow`, `tokio`, `axum`, `reqwest`, `tracing`, and `rayon`; choose only what the product warrants. Enable needed features. Prefer std facilities such as `OnceLock`/`LazyLock` when they cover the need and MSRV.

Before writing a service, async code, or nontrivial multithreading, read [concurrency.md](references/concurrency.md). Choose sync, threads, or async from the workload; specify limits and shutdown/cancellation behavior before spawning work.

Before writing or changing unsafe code or FFI, read [unsafe-ffi.md](references/unsafe-ffi.md). Keep the boundary narrow, document the safety obligations, and use safe alternatives where they meet the requirements.

Before optimizing, benchmarking, or claiming speed/memory improvements, read [performance.md](references/performance.md). Measure a correct optimized artifact against a defined baseline, workload, and acceptance threshold. Streaming and buffer reuse help where input size or profiling justifies them.

## Verify and review

Use the project's checks. For new projects, a useful starting point is:

```sh
cargo fmt --all --check
cargo clippy --workspace --all-targets -- -D warnings
cargo test --workspace
```

Then test supported feature/target combinations; `--all-features` is useful only if that combination is supported. `cargo test --all-targets` skips doctests, so run doctests separately if using it. Exercise release behavior where profiles affect correctness, as well as the installed binary, packaged library with an external consumer, or real service boundary. See [verification.md](references/verification.md) for targeted checks. Add tests that could distinguish a plausible wrong implementation; reproduce a regression without the fix when feasible. Do not add exhaustive machinery for a trivial edit.

For new projects, substantial migrations/features, and materially risky changes, arrange one bounded review after an integrated artifact works. Reserve time for it and corrections within the task allowance. Give a fresh reviewer the request, contract, artifact revision, and build/run commands, without the implementer's verdict. Ask for concrete defects and evidence. Reuse an existing independent review when it covers the final changes; do not create extra reviewers just to satisfy this skill.

Track review as **pending, completed, or unavailable**. Wait for an invoked reviewer; an invitation is not a completed review. Reproduce or refute findings, fix material defects, and rerun affected checks. Review changed areas again when fixes alter the assumptions. If independent review is unavailable within the host or allowance, do a distinct adversarial self-review and label it as such. Do not claim independence or quietly omit an unfinished review. [verification.md](references/verification.md) supplies a compact review brief.

## Resume and deliver

For work that may span contexts, retain only a short private checkpoint: goal and contract, current artifact revision, next step, loaded reference paths, checks with revision/results, review status, and unresolved findings. Use the host's state facility or scratch location outside the deliverable. Do not create instruction files or commit handoff notes to track a task.

After context loss, reread this skill and the references needed for the next step. Reconcile the checkpoint with the actual diff and artifacts. Missing evidence is unverified; stale test/review results do not become current by being copied into a summary. Rerun checks affected by changes, not every unrelated check automatically.

Before delivery, compare the final artifact with the requirement checklist. Run affected final checks and documented commands that apply to this environment. Check install/package contents for scratch files and unintended dependencies. Report what changed, evidence and its revision, review status, unverified requirements, accepted differences, and unresolved findings. Never describe an unbuilt artifact or an unmet performance target as verified.
