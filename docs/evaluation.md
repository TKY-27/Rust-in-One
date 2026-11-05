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

## Readability and change-impact pilot (2026-11-03)

This pilot tested the revision that added readability, change-impact, and maintainability-review guidance. The frozen candidate Skill tree is the one in commit `64ff545`; it was frozen before generation in an unpublished local commit. Its Skill-tree SHA-256 is `abfdee3cae52053ed235227ac7c1ed3670894827c2ec0cad3e417985554911e5`, computed with the same method as above. The baseline arm had no Skill. The results attach only to that candidate. They are not a comparison with `4d76cb1`.

### Method

The host was Claude Code CLI 2.1.317, run headless with `--model claude-haiku-5-5 --effort medium`. Opus, Sonnet, Haiku, and subagent model aliases were all pinned to `claude-haiku-5-5`. Both arms had the same tools: Bash, file tools, the subagent tool, and Skill. MCP and web tools were not available, and `--max-budget-usd 3` applied to each job, with a 1,800-second timeout. Each job had a fresh configuration directory and Cargo home, and project settings only. Each ran in its own mount and PID namespaces. `/tmp`, the repository, the author's session data, other jobs, graders, and expected results were hidden. Network access to crates.io was allowed in both arms.

Both arms received the same prompt, plus one neutral sentence asking the agent to use a relevant skill if available. The enabled arm had the Skill installed at `.claude/skills/rust-in-one/`. In every enabled job the host listed it, and the Skill body appeared in the transcript. In T2 maintenance it was read with `cat` rather than through the Skill tool.

Prompts, maintenance requests, and deterministic graders were hashed before generation. Each maintenance request was applied in a fresh context to that arm's own frozen initial artifact. Artifacts were graded as frozen and were not repaired. One sample was run per cell.

Tasks:

| Task | Request | Frozen checks |
| --- | --- | --- |
| T1, focused change | Add column ranges to an existing multi-file Rust CLI without changing other behavior | 25 differential regression checks against the original build, and 32 feature checks |
| T2, greenfield | Multi-file inventory-ledger CLI from a written contract; maintenance adds a signed `adjust` kind, a new column, and `--sku` filtering | 42 contract checks, 9 I/O checks, and 24 maintenance checks |
| T3, C migration | Port a three-file C tool to native Rust as a Linux drop-in; maintenance adds `-m` and `-o FILE` | 51 differential checks and 5 process checks against the C build (including SIGPIPE, `/dev/full`, and a 2× runtime bound), 13 maintenance checks, and 2 exploratory closed-descriptor checks |

### Results

| Job | Enabled | Disabled |
| --- | --- | --- |
| T1 | 57/57; Skill invoked, no reference opened, review **not performed** (focused change) | 57/57 |
| T2 initial | 51/51; no reference opened, review **not performed** despite a new project | 51/51 |
| T2 maintenance | 75/75 | 75/75 |
| T3 initial | 58/58 including exploratory; `migration.md` opened; independent Haiku review completed | 58/58 including exploratory |
| T3 maintenance | 71/71 | 66/71: all five failures are the updated usage line, which the report disclosed as an intentional difference from C |

Deterministic checks did not separate the arms, except for one T3 maintenance choice that is arguable: updating the usage text versus keeping the C tool's stderr exactly. Both T3 arms chose `#![no_main]` and raw descriptors to match the C tool's closed-descriptor behavior on Linux, so this pilot does not show that the expanded closed-descriptor note in `migration.md` changed behavior.

A separate post-hoc probe found that the disabled T2 artifacts panic on a non-UTF-8 file-name argument (`std::env::args`), in both the initial and maintained versions; the enabled artifacts handle it. This was not a frozen check, and the relevant `Path`/`OsStr` guidance predates this revision.

The enabled T3 reviewer brief asked for maintainability findings, but it also listed areas "already checked", which the Skill tells implementers not to provide. As in earlier audits, Haiku used reference files and independent review less often than the Skill directs.

### Readability assessment

A blinded evaluator using the authoring model, outside the trial roles, compared the artifacts under X/Y labels. The mapping was kept separately and opened only afterwards. The evaluator named specific code for each finding and gave no aggregate score.

- **T1:** mostly no material difference. The enabled arm had more consistent error naming and a test that pins partial output exactly. The disabled arm's descending-range iteration was slightly simpler.
- **T2:** the enabled arm was rated better on names and return values (a named `ApplyError` enum rather than `String`), on responsibility-based modules (CLI, input, record, summary, render, rather than a single 473-line `lib.rs`), on library use (`args_os`), and on how locally the maintenance change landed. The disabled maintenance version derived `on_hand` through `i128` arithmetic ending in `expect`. The evaluator rated that panic as practically unreachable, but it is not documented. Both arms duplicated the output field list between the text and JSON renderers.
- **T3:** the enabled arm was rated better on named outcome types, control flow, and narrow, `SAFETY`-documented unsafe code through `libc`. The disabled arm had hand-typed FFI and an unconditional SIGPIPE reset, where the C tool keeps the inherited disposition. The disabled arm had a better file split and better initial tests. Maintenance accommodation showed no material difference.

These are qualitative judgments from one evaluator on one sample per cell. They are observations, not an effectiveness estimate.

### Consumption

Costs are the CLI's `total_cost_usd` at list price, not billing records. Token figures are cumulative `modelUsage` totals. Every request recorded for the ten generation and maintenance jobs and their subagents used `claude-haiku-5-5`, including the T3 reviewer subagent. Jobs ran concurrently on four CPUs, so wall times are only indicative.

| Arm (5 jobs) | Cost (USD) | Output tokens | Cache read | Cache write | Uncached input | Wall time |
| --- | --- | --- | --- | --- | --- | --- |
| Enabled | 0.2020 | 183,166 | 4,884,397 | 329,471 | 198 | 1,504 s |
| Disabled | 0.1663 | 156,289 | 3,932,332 | 244,035 | 168 | 918 s |

Most of the enabled arm's extra time came from the T3 migration: 1,057 s versus 480 s, including the review. There were no retries or regenerations. Infrastructure probes cost under $0.01 in total. Authoring and the readability assessment used a different model and are not included.

**Consumption reconciliation:** applying the earlier audit's quoted rates and one-hour cache-write assumption to this pilot's token counts yields $0.20634097 enabled and $0.16629162 disabled. The enabled estimate differs from the reported $0.2020. Different cache durations or pricing may explain it, but request-level telemetry is unavailable here. Preserve the reported figures and treat cost comparisons as provisional.

### Limits

- Small pilot: one sample per cell, one generation model, one host, Linux only.
- The tasks were bounded multi-file programs, not large migrations or long-running projects.
- The deterministic checks could not separate the arms, and the readability comparison depends on a single evaluator.
- The readability assessment used the authoring model rather than Haiku; its exact model identifier and usage are not recorded here. This departed from the intended all-Haiku evaluation constraint. The trial-job model and cost tables exclude that assessment, and blinded labels do not establish independence from the authoring model's preferences.
- The five diagnostic source files that motivated this revision were not available in the authoring environment, so the revision relied on their written review. The closed-descriptor behavior was checked against Rust 1.97.0 std source and by execution on Linux x86_64 with glibc 2.39. Other targets were not executed.
- Raw prompts, transcripts, artifacts, graders, the blind mapping, and the assessment are kept outside this repository; their continued availability is not guaranteed.

## Greenfield verification revision (2026-11-04)

The forward-check candidate is identified by Skill Git tree `c34e4a333b27021c3ecd80349b45ad8b71652839`. These are Git trees for `skills/rust-in-one`, not repository roots or commits; compare with `git rev-parse <revision>:skills/rust-in-one`. The revision adds explicit completion decisions for brief requests, selection of tests by input/path/prior state/observable result, and independent expectations for central calculations where useful. It retains the existing readability, migration, concurrency, unsafe, performance, and review guidance. Final tree `b63cd65b311f821db2bf2b3e275908697f6a6229` differs only by a delivery-check clarification from independent instruction review: retain intentional test fixtures and regression corpora when removing task scratch data. Package and all-agent installation checks were rerun on that final tree; generation was not repeated for this wording correction.

### Human feedback and directed diagnostics

In a maintainer-supplied human comparison, the Skill-disabled new project was narrowly preferred for its failure tests; the enabled project was better structured, and both implementations were considered good. The enabled C++ migration was preferred for separation of responsibilities and an independent algorithm used to verify results. These are qualitative judgments on two examples. The generation traces and exact Skill revision for that comparison were not available in this audit, so these observations are not attributed to the revised package.

Two test-gap hypotheses in the supplied enabled new-project artifact were checked by execution on Linux x86_64 with Rust 1.99.1. Each change below was made separately in a disposable copy; the original artifact and its test suite were preserved.

| Deliberate defect | Original suite after mutation | Additional real-binary check |
| --- | --- | --- |
| Remove only the normal-processing `BufWriter::flush`, retaining the help-path flush | All 13 tests and one doctest passed | `list` writing to `/dev/full` returned success instead of the original exit status 2 |
| Replace only the end-time field's strict digit parser with `str::parse` into `u64` | All 13 tests and one doctest passed | An end-time token `+2` was accepted instead of returning the original syntax error |

The unmodified program passed both additional checks. This demonstrates missing test discrimination, not two defects in the original implementation. It motivates checking each independently handled input and the actual path responsible for an error. It does not show that the new Skill text improves generation. Diagnostic source copies and command output remain outside the repository.

### Candidate instruction and implementation check

One fresh `gpt-6.1-sol` subagent, with high reasoning and no inherited conversation, received a brief request for a standard-library-only persistent named-counter CLI supporting `add`, `set`, `get`, and `list`. The candidate Skill was explicitly selected. The request and evaluator's checking plan were frozen before generation; the solver did not receive the checking plan. Delegation and publication were disabled for this probe. There was no disabled arm, repeat, or selection among alternative generations.

The solver completed an installable program with a documented contract, checked arithmetic, serialized updates, temporary-file replacement, and error handling. It reported passing debug/release tests, formatting, Clippy, installation, and package verification. The evaluator froze the completed source without repairing it, built it in a separate target directory, and reran all two unit and twelve CLI integration tests successfully. Additional real-binary checks passed for the documented workflow across processes, rejected requests after successful updates, overflow, corrupt data, output failure after a committed update, and a write failure after 1,024 bytes of temporary-file output followed by recovery. These checks ran on Linux x86_64 with Rust 1.99.1.

This shows that the candidate could be used to complete this bounded task; it does not isolate a Skill effect. Native discovery, automatic activation, independent-review completion, other operating systems, and large-project behavior were not tested. The solver reported review as unavailable under the explicit no-delegation constraint and performed self-review instead. Shared-filesystem access was restricted by task instructions, not a filesystem sandbox. Raw model/billing telemetry was unavailable; no cost comparison is claimed. The frozen generated project and evaluator results remain outside this repository.

## Fresh paired examples for human review (2026-11-04)

Four fresh `gpt-6.1-sol` subagents, with high reasoning and no inherited conversation, generated one new Rust CLI and one C++-to-Rust port in each condition. The enabled condition received the explicitly selected package at commit `61dde733f8efa8eefa30117c3bcb22a9ade10b0f`, Skill Git tree `b63cd65b311f821db2bf2b3e275908697f6a6229`. The disabled condition received no copy. There was one generation per task and condition, with no replacement or best-of-N selection.

Task files were byte-identical within each pair. Both conditions had the same toolchain and tool access, separate working directories, and instructions not to inspect other jobs or evaluator material. These boundaries were instructions on a shared filesystem, not operating-system isolation. Delegation was prohibited in both conditions, so this comparison does not test independent-review orchestration. Workers could develop and test their own programs until delivery; the evaluator preserved each first delivered source without repairs.

The new task was a worklog CLI: validate dated, tab-separated project/minute records, continue after invalid records, and produce sorted project totals. The migration task was a weighted-interval-scheduling CLI with a 100,000-job limit, preserving the supplied C++ program's outputs, errors, and exit statuses. Each Rust deliverable contains its implementation and tests in one standard-library-only file; this was a packaging constraint, with no line-count cap. Tests ran on Linux x86_64 with Rust 1.99.1, edition 2024.

The task descriptions and checking plan were frozen before generation. The executable external checker was written afterwards, before inspecting delivered Rust source. Before port generation, the C++ source passed 107 cases, including 71 small job sets checked against exhaustive subset enumeration. The same frozen cases were then applied to both ports. New-project checks covered valid and invalid records, calendar boundaries, Unicode, continued processing, overflow, help, input failures, and ordinary output failures. Migration checks also covered token boundaries, exact diagnostics and statuses, broken pipes, and the full input limit.

| Check | Enabled | Disabled |
| --- | --- | --- |
| New CLI: external behavioral cases | 36/36 | 36/36 |
| New CLI: embedded tests | 15/15 | 11/11 |
| C++ port: external behavioral cases | 107/107 | 107/107 |
| C++ port: embedded tests | 9/9 | 12/12 |

All four programs passed production and test compilation with warnings denied, formatting checks, and compilation under renamed filenames. Embedded test counts describe the artifacts; they are not quality scores. No external-check failures, grader repairs, or post-delivery source edits occurred. These checks did not distinguish the conditions. Human review of these new artifacts was pending when this record was written.

The four original Rust files and the original C++ source were delivered separately as a five-file ZIP; generated programs and raw trial material are not tracked here. The ZIP's SHA-256 is `0a7d6066836c68a71f8f6f1a99b5d5b5702ebf561d43d1180b2996d67b51ab42`. Artifact filenames were assigned A/B labels before generation, with the condition key kept outside the ZIP. This record does not include full generation traces or a publicly archived reproducer. Native activation, context recovery, maintenance changes, large projects, other platforms, and repeated sampling were not exercised. Billing and token telemetry were unavailable; no resource-equivalence or general-effectiveness claim is made.

## Intent, completion, and correction checks (2026-11-05)

The candidate adds routine decisions from brief requests, a requirements checklist distinguishing implemented from verified behavior, and an implementation/check/correction loop. It also clarifies resource growth, compatibility decisions, integration obligations, and host continuation. Its installable Skill Git tree is `c6f5f91bf5176c2960f486a1320ce32d1aee1a56`. That package was frozen before generation and remained unchanged through the trials and corrections. Independent instruction review found no actionable introduced issue in the core, references, and public guidance.

### Method

These are candidate-only forward checks, not a comparison with the old Skill or no Skill. Three fresh `gpt-6.1-sol` contexts performed initial development, maintenance on that exact initial artifact, and a native C++ migration. Two earlier authoring-model starts were interrupted before either wrote a product file; neither partial artifacts nor private state were passed to Sol. There was no selection among completed alternative implementations.

The host was the built-in subagent interface, with explicit Skill selection, normal delegation capabilities, separate product directories and Cargo homes, and no source line/file limit. Fresh contexts did not inherit the authoring conversation or checking material. Filesystem boundaries were instructions on a shared host, not OS isolation. Effective reasoning settings and backend snapshots were not exposed; no explicit reasoning override was supplied. Billing and token totals were unavailable. Completed tools ran on Linux x86_64 with Rust 1.99.1 and the available C++17 compiler.

Requests and written checking plans were frozen before the corresponding generator. The new-project corpus and migration checker were also prepared before Sol generation, without reading generated Rust; the CLI adapter was written from delivered usage documentation afterwards. The C++ fixture and its plan were prepared separately without reading the candidate Skill. Representative source results were checked independently before treating that build as an oracle. Each delivered artifact was copied and hashed before external checks. The maintenance context received its own initial source without authoring notes or grader feedback. Corrections after external feedback were preserved as a later artifact, not substituted for the initial result.

### Tasks and observations

| Task | External checks on the preserved artifact | Review |
| --- | --- | --- |
| Brief new request: recursively list duplicate file contents, without deleting files, suitable for larger folders | 14/14: exact groups, same-size different content, binary data, empty files, Unicode paths, deterministic output, unchanged inputs, symlink policy, input/output failures, and usable invocation. The larger fixture contained 803 files, including three 64 MiB files. | Independent review completed; the generator fixed a missing root-path diagnostic and documented stable-input assumptions. The final diagnostic recheck was self-review. |
| Fresh maintenance request: add empty-file exclusion and JSON output, preserving defaults | 14/14 original checks and 20/20 feature/preservation checks. Default output and relevant error observations matched the initial artifact byte-for-byte; JSON was parsed with Python and compared with independently determined groups. | Self-review; independent review reported as not performed for this bounded change. |
| Native migration of a three-source-file C++ byte-key ledger | Initial artifact matched 39/41 differential cases. The two mismatches are explained below. | Independent review completed and had already found a separate closed-stdout startup difference, corrected before initial delivery. |
| Migration correction after external feedback | 41/41 original differential cases and the additional exploratory directory-as-stdin case matched the source. The 200,000-record workload also matched separately computed counts and totals. | Independent review found a flaw in the first correction and verified the revised boundary. |

Formatting, Clippy with warnings denied, included tests, and separate release builds passed for each preserved artifact. The new tool used size filtering, streaming fingerprints, and exact byte comparison; source inspection confirmed fixed per-file content buffers rather than whole-file collection. This is not a numeric peak-memory result. The maintenance change retained the existing traversal and grouping implementation. Test counts and structure alone were not used as quality scores.

### The migration mismatch and correction

With a nonblocking stdin pipe whose writer remained open, the C++ build treated the underlying `EAGAIN` as EOF: empty input succeeded, and an unterminated final record was accepted. The initial Rust build reported a read error and discarded that partial record. Rust followed the source README's general error description, but differed from the source's observable behavior. An exploratory directory-as-stdin case reproduced the same class of discrepancy; it was not an original scored case.

The generator reproduced the discrepancy and inspected the installed libstdc++ boundary. For this runtime, the C `FILE*` reported an error while the synchronized C++ stdin stream reported EOF. The correction preserved that characterized behavior in a concrete Linux stdin adapter and documented the exception. Ordinary file inputs and generic injected readers retained their error handling. Independent review caught a first correction that could read again after processing the partial final record; the final adapter retained EOF state, with a regression that fails on an extra read. The evaluator then rebuilt the corrected source and reran the original checks unchanged.

This exposes a compatibility gap missed by initial implementation and review. The later pass demonstrates a bounded correction after external evidence; it does not make the initial delivery fully compatible or show that the Skill completes every task correctly in one attempt. The Skill text was not expanded with these fixture-specific cases.

### Limits

There was one completed generation per task, one host, and one platform, with no disabled arm or repeated sampling. The programs were bounded CLIs, not large production migrations. Automatic activation, natural context compaction/resume, services, libraries, Miri, sanitizers, other platforms, and arbitrary sparse requests were not exercised here. Permission-denial probes requiring a lower-privilege child were unavailable in this environment; a chmod-only probe as root was not counted as coverage. The port contains a narrow Linux startup FFI boundary and Linux-specific stdin compatibility behavior; other targets remain unverified. No numeric peak-memory, general speedup, cost-effectiveness, or causal Skill-effect claim is made. Raw artifacts, reports, and checking scripts remain outside this repository in the temporary authoring environment; there is no complete public reproducer for these trials.
