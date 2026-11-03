# Verification, review, and delivery

Read the relevant sections while planning substantial work, before its first public boundary is designed. Return to them for review and delivery. The table is a menu of product risks, not a requirement to run every check on every task.

## Map requirements to evidence

For each item on the requirements checklist, pick evidence that would fail if the implementation were plausibly wrong. A test that only exercises the happy path of the code you just wrote is weak evidence. Reuse existing checks where they still apply.

| Product | Checks that usually matter |
| --- | --- |
| CLI | Run the built binary: stdout and stderr kept separate, exit codes, stdin and `-`, `tool \| head -1` without a panic, missing and unreadable files, a directory passed as a file, empty and non-UTF-8 input, large input (time and peak memory, streaming rather than loading), `--help` matching the README |
| Library | Integration tests in `tests/` that use only the public API; examples that compile and run; doctests; error types satisfy the caller's required bounds (often `Send + Sync + 'static`); public types have the intended `Send`/`Sync`; feature combinations; documentation builds without warnings |
| Service | Real requests to a server bound to `127.0.0.1:0`: malformed and oversized requests, request size limits and timeouts, peers that stop reading responses, recovery of saturated worker capacity, dependency failures, graceful shutdown with in-flight requests, configuration errors at startup |
| Concurrent code | Shutdown and cancellation paths, error propagation from tasks and threads, bounded queues under load, repeated runs to expose flakiness; `loom` for custom lock-free or atomic protocols |
| Persistence | Interrupted writes (same-filesystem temporary file, flush/sync as required, atomic rename where supported, and parent-directory sync for crash durability on platforms that require it), recovery on restart, behavior when the file is from an older or newer version, concurrent access if possible |
| Parsers and decoders of untrusted input | Property tests (`proptest`) for round trips and invariants; fuzzing (`cargo fuzz`, nightly) for crash-freedom; explicit tests for limits on nesting, length, and allocation |
| Performance requirements | See [performance.md](performance.md) |

## Commands worth knowing

```sh
cargo test --workspace --all-features            # includes doctests
cargo test --doc                                 # doctests only; --all-targets skips them
cargo test --no-default-features                 # when the crate supports it
RUSTDOCFLAGS="-D warnings" cargo doc --no-deps   # broken intra-doc links, missing docs if linted
cargo build --release && ./target/release/<bin>  # the artifact users run
cargo install --path . --root "$(mktemp -d)"     # install as a user would, then run it from there
cargo package --list                             # files a published crate will contain
cargo package                                    # builds the crate from its packaged contents
cargo tree --duplicates                          # duplicate dependency versions
```

Use optional tools when they are installed or the project already uses them, and do not report them as run otherwise: `cargo semver-checks` before releasing a library, `cargo audit` or `cargo deny` for advisories and licenses, `cargo +nightly miri test` for unsafe code (see [unsafe-ffi.md](unsafe-ffi.md)), `cargo hack --feature-powerset check` for feature combinations, and `cargo msrv verify` or `cargo +<msrv> check` for a declared `rust-version`.

Compiling across feature combinations does not test their behavior. A passing `cargo check` on another target does not show the program works there.

## Test design notes

- Put unit tests next to the code (`#[cfg(test)] mod tests`) for internal logic and integration tests in `tests/` for the public surface. Integration tests compile as separate crates and see only public items.
- Use isolated temporary directories for filesystem tests (`tempfile::TempDir` is convenient). Do not mutate source fixtures or depend on an incidental current directory.
- For complex textual output, golden files or snapshot tests (`insta`) catch regressions. Review every snapshot update rather than accepting it blindly.
- For isolated async timer logic, use `#[tokio::test(start_paused = true)]` with Tokio's `test-util` feature and current-thread runtime. Real transport tests still need bounded real deadlines.
- A passing test can be evidence even if it never failed. For a regression test, confirm it fails without the fix when feasible; this checks that it detects the actual defect.

## Independent review

Give the reviewer:
- the user's original request and the requirements checklist, including accepted assumptions;
- the artifact: repository path and commit, or the diff, plus build and run commands;
- the risk areas of the product, such as untrusted input, unsafe code, concurrency, and compatibility commitments. These describe the product, not your conclusions about it.

Do not give the reviewer your own verdict, your summary of which tests pass as a reason to trust the code, continuation notes, or a list of areas already checked. Ask for findings in this form:

```text
[severity: critical/high/medium/low] <title>
Where: <file:line or component>
Requirement or invariant violated: <...>
Evidence: <reproducer, failing input, or concrete code path>
Suggested direction: <optional>
```

Close each finding with evidence: a test that failed before the fix and passes after it, or a demonstration that the premise is false. If you and the reviewer still disagree about a material finding, report both positions to the user. After fixes, rerun checks affected by the change and recheck the integrated artifact. Repeat wider checks when integration risk or repository policy warrants it.

## Delivery checks

- The requirements checklist is satisfied, or each gap is stated.
- Final checks pass on the final revision. Rerun affected checks after the last edit, including doctests when examples change.
- The delivered artifact works from a clean location: installed binary, packaged crate (`cargo package`), or container/service configuration.
- Applicable README commands and examples were run; platform-specific or unavailable deployment steps are clearly marked unverified.
- `git status` and `cargo package --list` (for crates) show no scratch files, notes, logs, generated test data, or secrets.
- The report distinguishes checks that ran from checks that were not possible here, such as missing tools, platforms, or credentials.
