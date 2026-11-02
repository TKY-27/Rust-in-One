# Rust-in-One

From one request to a complete Rust project.

Rust-in-One is an [Agent Skill](https://agentskills.io/specification) that helps a coding agent deliver complete, verified Rust software from a short request, including when the person asking is not a Rust expert. It covers, in order of priority:

1. building new Rust projects from scratch;
2. improving, fixing, and finishing existing Rust codebases;
3. migrating existing software, especially C and C++, to Rust with faithful behavior and good performance.

"One request" means one delegated task, including the implementation, testing, review, and corrections needed to finish it.

## What the skill provides

- **Process scaled to the task.** A small fix gets a focused correction and the project's checks. A new project or migration gets requirements, an early end-to-end path, verification against those requirements, and an independent review.
- **Concrete Rust engineering defaults.** These cover project setup, ownership and data modeling, error handling, dependencies, and when to use async or unsafe code. They include the gotchas that commonly produce wrong programs: `HashMap` order leaking into output, non-UTF-8 input aborting a run, release-mode integer wrapping, broken-pipe panics, and lost buffered output.
- **Verification of the delivered artifact**, not just `cargo test`: running the real binary, packaged crate, or service the way users will.
- **Independent review that is actually independent.** The reviewer gets the requirements and the artifact, not the implementer's self-assessment.
- **Continuation state for long tasks**, kept out of the deliverable and away from reviewers, and reconciled against the repository after a context reset.
- **An honest delivery report**: what was verified, what was not, and what remains.

It does not choose Rust for requests whose language is undecided, and it does not apply to the non-Rust parts of mixed-language repositories.

## Install

Copy the whole [`skills/rust-in-one`](skills/rust-in-one) directory, keeping its name and its `references/` directory, into a skills location your agent scans:

| Agent | Project skills | Personal skills |
| --- | --- | --- |
| [Claude Code](https://code.claude.com/docs/en/skills) | `.claude/skills/rust-in-one/` | `~/.claude/skills/rust-in-one/` |
| [Gemini CLI](https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/skills.md) | `.gemini/skills/rust-in-one/` or `.agents/skills/rust-in-one/` | `~/.gemini/skills/rust-in-one/` or `~/.agents/skills/rust-in-one/` |
| Other [Agent Skills clients](https://agentskills.io/clients) | See the client's documentation | See the client's documentation |

For example, for all Claude Code projects on one machine:

```bash
git clone https://github.com/TKY-27/Rust-in-One.git
```

```bash
mkdir -p ~/.claude/skills && cp -R Rust-in-One/skills/rust-in-one ~/.claude/skills/
```

Then confirm the agent can see the skill (`/skills` in Claude Code, `/skills list` in Gemini CLI). The skill uses only standard `SKILL.md` frontmatter and relative links. It needs no plugin, hook, MCP server, specific model, or companion skill. Its checks use the Rust toolchain (`cargo`, `rustfmt`, `clippy`); optional tools such as Miri or `cargo-fuzz` are used only when present.

## Use

Ask for the work in plain terms. In the trials below, Claude Code loaded the skill on its own for Rust tasks and left it unused for non-Rust tasks; other agents' selection behavior has not been checked. You can also invoke it explicitly, for example `/rust-in-one` in Claude Code.

- "Build a Rust CLI that summarizes nginx access logs, with JSON output."
- "Finish this Rust library: make the public API consistent, document it, and make sure it packages."
- "Port this C tool to Rust as a drop-in replacement that is at least as fast."
- "The parser in `crates/geo` rejects negative coordinates; fix it."

## Contents

| File | Read by the agent |
| --- | --- |
| [SKILL.md](skills/rust-in-one/SKILL.md) | On activation: scope, scaling, engineering defaults, verification, review, continuation, delivery |
| [references/verification.md](skills/rust-in-one/references/verification.md) | For substantial work: checks by product type, useful commands, review brief, delivery checks |
| [references/migration.md](skills/rust-in-one/references/migration.md) | For migrations: contract inventory, differential testing, C/C++ semantic traps, transition strategy |
| [references/concurrency.md](skills/rust-in-one/references/concurrency.md) | For services, async, or multithreaded code |
| [references/unsafe-ffi.md](skills/rust-in-one/references/unsafe-ffi.md) | Before writing `unsafe` or FFI code |
| [references/performance.md](skills/rust-in-one/references/performance.md) | Before benchmarking, optimizing, or making performance claims |

## Status

Early. The skill has been exercised in one harness on a handful of tasks, as described below. Treat it as a starting point that needs broader trials.

**Format.** The frontmatter follows the [Agent Skills specification](https://agentskills.io/specification), checked with a local re-implementation of the `skills-ref` 0.1.1 rules (the validator itself was not run), and all relative links resolve.

**Manual trials** (2026-11-02, Claude Code 2.1.316, headless `claude -p`):
- Each run used a fresh directory with project settings only, no MCP servers, and the skill installed as a project skill, or absent for the "without" column.
- Results were checked with tests kept outside the trial directories, against copies of the delivered code. Run times are relative to the C original on a 143 MB corpus, measured on an idle machine.
- Costs are the CLI's reported session totals, including subagents.
- There was one run per cell, so these are observations, not measurements.
- Model `claude-opus-5-5` unless noted. Haiku run 3 used the current skill text, except for one duplicate sentence removed from `migration.md` afterwards. The other runs used earlier drafts, which lacked the SIGPIPE, migration, performance, and review wording revised after Haiku runs 1 and 2, and a few additions for existing projects.

| Task | With the skill | Without the skill |
| --- | --- | --- |
| New CLI: nginx/Apache log summarizer | Its review found 11 issues, 9 fixed, including nginx `000` status lines rejected as malformed; hidden checks passed; $2.65 | Hidden checks passed except the same `000` defect; $1.05 |
| New CLI: rename photos by EXIF date (no language given) | Both arms chose Rust; the skill loaded only after that choice. Its review found 6 defects, all fixed; it completed every rename when output was cut off; $2.33 | Panicked after renaming 3 of 300 photos when output went to `head`; accepted Feb 31; $0.29 |
| Port a 200-line C tool as a drop-in replacement | 0 of 30 hidden differential checks failed; 0.55× C run time; its review found 5 issues, all fixed; $4.67 | 0 of 30 failed; 0.66×; $1.74 |
| Same port, `claude-haiku-5-5` | Three runs, 0 of 30 failed in each. Run 1 left SIGPIPE and closed-stdin exit statuses different from C (0.77×, $0.47). After revising `SKILL.md`, SIGPIPE matched in runs 2 and 3. Run 2 was 1.07× C while claiming a speedup ($0.17); run 3 was 0.80× ($0.36). Runs 2 and 3 skipped the independent review and said so | 0 of 30 failed; matched C on both statuses; 0.75×; $0.45 |
| Python-only bug in a mixed Rust/Python repository | Skill not invoked, as intended; focused fix; $0.11 | — |
| Small Rust bug fix | Focused fix and regression test, no review or notes; $0.23 | — |
| "Quick script" to find duplicate files (no language given) | Skill not invoked; wrote Python; $0.13 | Wrote Python; $0.11 |

What these runs suggest:
- The review step caught real defects in new projects, at about 2.5–8× the cost of the run without it.
- The strong model handled most Rust gotchas on its own.
- The smaller model followed guidance in `SKILL.md` but opened a reference file only once its pointer was placed at the point of use.

**Not yet tested:** other harnesses (Codex, Gemini CLI, Copilot, Cursor, and others), other model families, libraries, services, unsafe/FFI work, continuation after context compaction or across sessions, and repeated runs.

## Contributing

Tie changes to a concrete engineering failure or a useful task. A good change is a gotcha the agent demonstrably gets wrong, or guidance that changed an observed outcome. Keep `SKILL.md` well under 5,000 tokens and put the most important guidance first; Claude Code, for example, re-attaches only the first 5,000 tokens of an invoked skill after context compaction. Put specialized material in a reference, linked from the point in `SKILL.md` where it is needed. New dependencies, abstractions, and procedures should solve an observed problem. Harness-specific integration stays optional.

Before submitting, validate the format with the [reference validator](https://github.com/agentskills/agentskills/tree/main/skills-ref). The specification calls it `skills-ref validate`; version 0.1.1 of the `skills-ref` package on PyPI installs the command as `agentskills`:

```bash
pip install skills-ref
```

```bash
agentskills validate skills/rust-in-one
```

Also check that relative links resolve. When reporting behavior, include the skill revision, harness and version, model, configuration, the task, and the observed result. Keep format validation, manual trials, and comparative evidence distinct, and do not claim effectiveness from successful invocation or favorable model reviews alone.

## License

[MIT](LICENSE). The skill directory carries its own copy ([LICENSE.txt](skills/rust-in-one/LICENSE.txt)) so the notice travels with installed copies.
