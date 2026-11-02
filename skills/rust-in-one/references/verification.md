# Verification and review

## Choose checks from requirements

For each important behavior, choose evidence that could reveal a plausible wrong implementation. Reuse existing checks when they still apply. Match additional verification to the product:

| Product concern | Useful checks |
| --- | --- |
| CLI behavior | Real process execution, output and exit status, malformed input, interrupted work |
| Library/API | An external consumer, examples, error behavior, supported features and targets |
| Service or concurrent work | Cancellation, shutdown, bounded resources, failure propagation, relevant interleavings |
| Persistence | Partial writes, recovery, and durability expectations on the intended platform |
| Performance | Representative release workloads, result quality, latency, throughput, and memory |

Select Cargo targets and features intentionally. Exercise eligible doctests separately where the chosen test command omits them; `--all-targets` does not include doctests. Compilation across features does not establish their behavior. See the [Cargo test documentation](https://doc.rust-lang.org/cargo/commands/cargo-test.html).

For unsafe code, examine validity, aliasing, lifetimes, synchronization, and obligations exposed to callers. Prefer a requirement-preserving safe alternative when it resolves uncertainty at reasonable cost. A smaller unsafe block is not necessarily a smaller safety obligation. Use tools such as [Miri](https://github.com/rust-lang/miri) where applicable, while retaining source-level reasoning about untested inputs and executions.

## Review independently

For substantial or risky work, give an independent reviewer the requirements and a fixed artifact, without treating the author's conclusions as an answer key. Use fresh review context where available. Prevent author-specific continuation instructions from automatically directing the review; a separate worktree alone does not reset shared host state.

Prefer a reproducer, but also accept a concrete source-level counterexample or violated invariant. Close findings with evidence that the cause was corrected or the premise was false. Escalate unresolved material disputes when needed; additional favorable votes do not resolve them. Recheck relevant risks after integrating corrections.

## Check delivery

Test from the actual package, clean consumer, or distributable binary rather than relying solely on the development tree. Verify included files, required assets, configuration, and necessary usage instructions.

Record significant checks and their results against the delivered revision. Keep unrun checks and unresolved findings visible. Preserve useful diagnostics outside the shipped artifact when appropriate. Do not turn evidence collection into a second documentation project.
