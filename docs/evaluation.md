# Bounded evaluation of the refinement

These are small engineering trials, not a general benchmark or proof that the skill improves every model. The refinement evaluated here started from `3967848af3fe9bbf03d99c06afa2a473deea4a0a` on `claude/laughing-noether-a5y1fn`; it did not start from the then-current `main`. Earlier Claude results are preliminary reports and were not independently reproduced.

The paired runs compare skill-enabled and skill-disabled conditions. They are not matched comparisons of Claude's starting revision with the refined revision.

## Method and limits

Trials ran on 2026-11-03, Linux x86_64, Rust/Cargo 1.99.1 and GCC/G++ 14.2.0. The primary generator was **`gpt-6-luna`, medium reasoning**, in fresh `fork_turns=none` subagent contexts. The additional comparison used **`gpt-6.1-sol`, medium reasoning**. A separate content review used `gpt-6.1-sol`, high reasoning. These are the configured model IDs accepted by the harness; backend snapshot IDs, sampling parameters, token usage, and billing totals were not exposed. No model substitution was recorded.

The standalone Codex CLI 0.163.0 could not reach its model endpoint under the environment's network policy. Two failed launches were retained as infrastructure attempts. The working harness was the built-in subagent interface, **not a successful Codex CLI evaluation**.

Each pair received the same product request, background guidance, tool catalog, fresh product directory, and nominal four-minute solving allowance, including retries, failed attempts, and serial reviewer work. Fresh contexts reset conversation state; generated build directories were not reused between arms. Only the enabled directory contained the skill. No implementation delegates were allowed; one fresh reviewer context could be used and revisited within the allowance. Reviews used the generator's model/settings. Timings are approximate dispatch-to-report wall time, not token-matched or dollar-matched consumption.

The generators shared a host filesystem and inherited host tooling; they were instructed to stay within their own trial directories. This is weaker isolation than separate machines/configuration homes. Private grading code and expected answers were kept in orchestrator memory during generation. Local skill selection was supplied through a common catalog instruction, so these trials **do not validate automatic host discovery or routing**. File-access observations and read receipts were assessed separately from compliance and product correctness; a file read does not prove its guidance was applied.

Initial product checks were fixed before generation. Artifacts were copied and hashed before grading; the evaluator did not repair them. Clean builds and executable checks ran with the rest of the workspace hidden by a filesystem/PID sandbox. Submitted hooks and build configuration were not executed; the bounded tasks required the standard library only. Library behavior was checked from a separate consumer, and migrated binaries were checked against the original C/C++ builds for output, errors, exit statuses, and performance. Independent source review found additional failures beyond the initial tests. Those exploratory checks are identified below; the repeat probes were fixed before final generation. A grader mountpoint error was corrected without changing artifacts or acceptance criteria. A final harness hardening added external-consumer completion checks and moved Python expected-output comparison outside the submitted process; affected frozen artifacts were rerun with unchanged cases and results.

Performance numbers are five-run alternating median ratios against the original, on one host with warm input. They include sandbox/process startup and pipe copying. The limit was 2× the original runtime, not a claim of superiority; microbenchmark significance and other platforms were not established.

## Development observations

The first library pair used Claude's exact skill. Other development pairs used the first refinement draft. The core was then shortened from 2,316 to 1,459 whitespace-delimited words, and factual corrections and targeted failure guidance were applied.

| Task | Enabled | Disabled |
| --- | --- | --- |
| New CLI, byte records and checked aggregation | 9/9 initial checks; completed review | 9/9; no review |
| Library with external consumer | 5/5; completed review | 5/5; completed review, reviewer could not run Cargo |
| Concurrent TCP service | 9/9 initial checks; source review and saturation probe found unbounded response writes despite completed review | Same initial checks and response-write defect; no review |
| Focused existing fix | 4/4; focused checks without review | 4/4; focused checks without review |
| Native C migration | 15/15 including SIGPIPE; completed review caught buffered output lost on an error path | 14/15: SIGPIPE status mismatch; no review |
| Native C++ migration | 18/18 initial checks, but exploratory checks found whitespace and small failed-output differences; completed review | 17/18: SIGPIPE mismatch; exploratory whitespace check passed, small failed-output status differed; no review |

The C++ whitespace result is a regression, not a win for the skill. Both migration arms met the runtime limit. For the C migration, independent ratios were 1.04× enabled and 0.96× disabled; the generator's own faster enabled timing was not reproduced by this measurement method.

Failures led to general guidance about both read and write deadlines, recovery of worker capacity, source parser character classes, small/large buffered-output failures, and reassessing reference needs when the design gains a new boundary. No case-specific expected answers were added to the skill.

## Evaluated frozen revision

The installable skill tree used for the repeat and fresh-task runs was frozen before generation and is preserved at [commit `e2e1979`](https://github.com/TKY-27/Rust-in-One/tree/e2e19793b2c652f416e6e58fee10801460e070bf/skills/rust-in-one). Its aggregate SHA-256 over the sorted path-to-file-hash mapping is `cd6f6819515024b6dfaf7125665c8eb895db8ce01caa19783df59353492d242b`. The results below refer to that snapshot. Subsequent editorial revisions have not been rerun in these trials.

| Final task | Enabled | Disabled |
| --- | --- | --- |
| Luna: repeated service | 9/9 initial checks; 3-second saturation probe still failed; counter lock held during ADD response | Same initial count and saturation failure; same lock scope defect |
| Luna: repeated C++ migration | 18/18 initial + whitespace check passed; small failed-output status still wrong | 17/18 initial (SIGPIPE wrong); whitespace passed; small failed-output status still wrong |
| Luna: fresh CLI holdout | 9/9 initial; source-review output-flush reproducer passed | 9/9 initial; silently returned success after decoded-output flush failed |
| Luna: fresh library holdout | 5/5, external consumer/package; no material source finding | 5/5; no material source finding |
| Luna: synthetic continuation | 4/4; reconciled stale note with actual code | 4/4; also corrected the stale state |
| Python-only and language-undecided routing | Both stayed in Python; Rust file unchanged in mixed project | Same outcomes |

The C++ repeat repaired the enabled draft's lexical regression, but did not achieve full source equivalence. Independent final timing was 0.33× the original in both arms, meeting the 2× bound. In a **post-hoc ten-second** service probe, the enabled arm recovered capacity while the disabled arm remained saturated. The original three-second result remains a failure; queued requests make that probe an imperfect measure of the per-I/O deadline. The lock held across response I/O remains an independent source finding.

The fresh CLI holdout provides limited favorable evidence for explicit flushing. The library, routing, and synthetic recovery cases were neutral. The enabled fresh CLI holdout run did not invoke an independent reviewer despite available time/tools; its report called review unavailable/not performed, without evidence of a host refusal. Reference use also remained incomplete: the final C++ run recorded core, migration, and verification reads, but omitted performance/FFI references despite benchmarking and adding FFI. No favorable review or read receipt was counted as a correctness pass.

The `gpt-6.1-sol` pair (medium reasoning) passed 9/9 initial service checks in both arms and both completed independent review. Source review found bounded reads/writes and atomics without the Luna artifacts' lock-across-I/O defect. In the three-second saturation probe, the enabled arm failed and the disabled arm passed; both arms recovered in the exploratory ten-second probe. These results do not establish that the refinement improves outcomes for `gpt-6.1-sol` or other models. The enabled generator also disclosed a scope mistake: its first discovery command listed sibling filenames. No sibling contents or expected answers were reported read. This reinforces the shared-filesystem isolation limitation.

## Consumption, review, and claims

There were **28 generation sessions: 26 Luna and 2 `gpt-6.1-sol` sessions**, plus **11 trial reviewer contexts**, some revisited after fixes. Approximate serial solving wall time totaled **51 minutes** across the runs, including the requested serial review waits, retries, and failed attempts. Each run had the same four-minute allowance; all finished within it. Across the nine substantial Luna pairs, enabled totaled about **21.8 minutes** versus **13.9 minutes** disabled (1.56×). This aggregate includes development and frozen-revision runs. The `gpt-6.1-sol` pair took about 3.1 and 3.0 minutes. This measures elapsed solving time, not complete billed computation: token and dollar totals, reviewer-internal usage, and precise overlapping tool timing were unavailable. Two failed standalone CLI launches and a separate skill-content review were additional authoring/infrastructure work, not successful generation trials.

All invoked trial reviewers completed. Reviews found real issues in some enabled artifacts, but did not close the evaluator's later findings. The enabled fresh CLI holdout run skipped review; focused fixes appropriately avoided it. Reported successful checks were not found to be fabricated, but completion statements sometimes exceeded the evidence: for example, disabled C error/status parity was contradicted by SIGPIPE, and passing service checks did not establish stalled-peer safety. No unverified platform, sanitizer, or timing run was credited as performed.

## What remains unproven

The bounded standard-library tasks do not cover substantial production-sized migrations, dependency selection in real ecosystems, Tokio/HTTP frameworks, cross-platform behavior, Miri, sanitizers, natural context compaction, or real release/deployment pipelines. A synthetic fresh-session stale-checkpoint test is distinct from natural compaction. Neither instructions nor independent review eliminate residual defects. Reference access remained incomplete in some enabled runs even with explicit point-of-use links; adding more mandatory procedure was not treated as a demonstrated solution.

## Reproduction and package validation

The local evidence bundle contains requests, source baselines, skill snapshots, file hashes, generated artifacts, available command logs, review/report records, graders, and measured results. It remains outside this OSS repository, as do private acceptance details and task notes. Full model transcripts and billing telemetry were not available through the subagent interface, so exact stochastic replay or dollar-cost reproduction is not claimed.

**Evidence availability:** raw trial artifacts, graders, and logs were retained outside this repository in temporary authoring environments, including the later Haiku audit. Their continued availability is not guaranteed. This repository preserves the reports and evaluated Skill revisions, but does not provide a complete independently rerunnable evaluation bundle.

`skills-ref` 0.1.1's actual `agentskills validate` command passed. The repository's `scripts/check-package.py` separately checks local file links, standalone copy contents, and MIT notice equality. This was not merely a local reimplementation of the schema validator. Installation paths and skill lifecycle claims were checked against the current [Agent Skills specification](https://agentskills.io/specification), [OpenAI guidance](https://learn.chatgpt.com/docs/build-skills), and [Claude Code documentation](https://code.claude.com/docs/en/skills).

## Haiku-only audit trials (2026-11-03)

This later, separate audit started from `632e0a6`. Its results attach only to the revisions named here and do not change the results above. All trial roles that used a model used **`claude-haiku-5-5`**: generation, retries, subagents, and reviewers. Every request reported in the CLI's `modelUsage` was `claude-haiku-5-5`, including subagents. No LLM grading was used.

| Revision | Skill change | Skill-tree SHA-256 (same method as above) | Trial jobs |
| --- | --- | --- | --- |
| `63ea268` (candidate 1) | `cargo install --locked` in the delivery check | `e8b69eff96006b4bf529027c0aa9d896e7ec890191fa3b962bc7d8977bb70546` | 12 (one pair per task) |
| `5b3469e` (candidate 2) | Reference files must be opened; migration step explicit | `5ef446994ae3a104fc7f2f1aae6fb359b16a59cc89b299ffa0711034c6400b38` | 4 (two repeat pairs) |

### Method

Claude Code CLI 2.1.317 ran headless (`-p`) with `--effort medium` and the same tools in both arms: Bash, file tools, the subagent tool, and Skill. Web tools and MCP were disabled. The model aliases and the subagent model were pinned to Haiku. The enabled arm installed the skill at the project's `.claude/skills/rust-in-one/`, and the host's own skill list confirmed discovery. The disabled arm had no copy. Each job had a fresh configuration directory with project-only settings and account skill sync disabled. Bundled host skills were identical in both arms.

Generators ran in private mount and PID namespaces as uid 0 with no capabilities. `/tmp`, other runs, the repository, and graders were hidden. The host's model-authentication directory stayed visible. Prompts, limits, and checks were fixed before generation: $2 per job, 1,500 seconds per job, at most 16 jobs, and $20 in total. Artifacts were frozen and then graded by an unprivileged user. Dependencies were fetched first, and grading then ran offline in fresh network, mount, and PID namespaces. Checks were deterministic: behavioral checks, external-consumer tests, and differential runs against the original C build. Three grader bugs were corrected without changing artifacts or criteria, and every affected run was regraded:
- a module-import error in the Python task, found before generation;
- a wrong expected value and a debug-build overflow in the library tests, which had failed both arms identically;
- a pattern that mistook a doc comment for C build integration, which only narrowed that check.

### Results

| Task | Enabled | Disabled |
| --- | --- | --- |
| New CLI (`key=value` diff) | 27/27; skill invoked, no reference opened, no review (reported "not performed") | 27/27 |
| Library with external consumer | 21/21; skill listed but not invoked | 21/21 |
| Concurrent HTTP service | 24/24; not invoked | 23/24: replied 413 with `Connection: close` but held the socket until the 5 s read timeout |
| C migration (46 differential checks, 2× runtime bound) | 46/46, 0.40× C runtime; invoked, `migration.md` not opened, no review or review status | 46/46, 0.40× |
| Focused Rust fix with unrelated user edits | 11/11; not invoked | 11/11 |
| Python change in a mixed repository | 10/10; not invoked, Rust untouched | 10/10 |
| Candidate 2 repeat: new CLI | 27/27; invoked, no reference opened; review completed, and the agent reported fixing one finding | 27/27 |
| Candidate 2 repeat: C migration | 46/46, 0.34×; invoked, `migration.md` opened; review completed; reported residual closed-descriptor and inherited-SIGPIPE differences (not graded) | 46/46, 0.34× |

Both arms reached or nearly reached every acceptance check, so these tasks did not separate the conditions. The only failed check was in a disabled artifact. Activation with Haiku was partial: the skill was invoked in 2 of 5 Rust tasks for candidate 1, and correctly not invoked for the Python task. With candidate 1, an invoked skill opened no reference file. Candidate 2 was followed by `migration.md` being read in its one migration repeat. One run cannot attribute that change to the edit, because review use also changed between same-text CLI runs. Independent review ran only in the two candidate 2 repeats. Briefs contained the request, files, and commands without the implementer's verdict. Reports named review status when they mentioned review. The candidate 1 migration report omitted it.

### Consumption

All costs are the CLI's `total_cost_usd`, computed at list price. They are not billing records. Token counts are cumulative `modelUsage` totals, including subagents. Pricing was taken from [Anthropic's pricing page](https://platform.claude.com/docs/en/about-claude/pricing) on 2026-11-03: Haiku 5.5 prompts up to 100K tokens cost $0.10/MTok for input, $0.50/MTok for output, $0.01/MTok for cache hits, and $0.20/MTok for 1-hour cache writes. Wall time is dispatch to exit, including waits for subagents. Four jobs ran concurrently on four CPUs. Runtime ratios were measured afterwards with five alternating runs and no other jobs.

| Jobs | Cost (USD) | Output tokens | Cache read | Cache write | Uncached input | Wall time |
| --- | --- | --- | --- | --- | --- | --- |
| Candidate 1 enabled (6) | 0.1021 | 101,789 | 1,753,166 | 167,407 | 122 | 633 s |
| Candidate 1 disabled (6) | 0.1303 | 137,479 | 2,194,432 | 197,457 | 132 | 716 s |
| Candidate 2 enabled (2) | 0.1187 | 107,286 | 3,039,443 | 198,784 | 132 | 696 s |
| Candidate 2 disabled (2) | 0.0586 | 65,449 | 782,007 | 89,852 | 44 | 388 s |
| **Total (16)** | **0.4093** | 412,003 | 7,769,048 | 653,500 | 430 | 2,433 s |

**Reconciliation note (2026-11-03):** the historical cost figures above are preserved as reported, but they do not reconcile. The displayed rows sum to $0.4097 rather than the reported $0.4093 total. Applying the stated rates and the one-hour cache-write assumption to the token totals yields $0.41443498. Per-request cache durations, pricing tiers, and raw telemetry are not available in this repository, so the discrepancy cannot be resolved here. Do not use these figures for cost comparisons or budgeting.

There were no retries. Infrastructure probes added about $0.0067. Audit and authoring work used a different model and is not included; its usage was not available.

### Limits of this audit

There was one sample per cell, small tasks, one model, one host, and one platform. The results do not show general benefit, guaranteed correctness, or readiness for large migrations. Activation through native discovery was observed in Claude Code only; other clients were not tested. A fresh session started without context loss, so recovery after compaction was not exercised. Miri, sanitizers, dependency-heavy migrations, and cross-platform behavior were not exercised. Package checks for this revision are described in the following paragraph. Codex install paths were checked against the `openai/codex` source, because the Codex documentation hosts and agentskills.io were unreachable from the audit environment.

`agentskills validate` (skills-ref 0.1.1) and `scripts/check-package.py` passed on the final revision.
