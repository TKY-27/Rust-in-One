# Rust-in-One

A portable Agent Skill for carrying even a brief Rust request through design, implementation, verification, and delivery.

This [Agent Skill](https://agentskills.io/specification) prioritizes new Rust CLIs, libraries, and services, then substantial Rust-native migrations, especially from C/C++. It also supports focused fixes, improvements, and reviews of existing Rust code. The skill instructs agents not to select Rust merely because the skill is installed or apply Rust procedures to unrelated languages.

## What it provides

- Concrete Rust guidance on ownership, public APIs, byte/text boundaries, arithmetic, errors, output, and dependencies.
- Intent and completion conditions derived from the request and project context, with routine product and technical decisions handled by the agent.
- An implementation and verification loop driven by unmet requirements, concrete defects, and important unverified assumptions, keeping implemented work distinct from verified behavior.
- Verification of input boundaries, actual execution paths, failure after progress, and observable state and output, with independent checks for central algorithms where useful.
- Readability and maintainability guidance: results and control flow that state their meaning, boundaries by responsibility, reuse of library behavior that matches the contract, and restructuring that preserves observable behavior.
- For changes to existing projects: tracing the affected architecture and obligations first, extending existing implementations, and checking the impact on unchanged behavior.
- For reviews of an existing repository or diff: evidence-backed findings, severity and coverage, without changing the reviewed files unless fixes are requested.
- Migration checks against defined source behavior, including errors, exit statuses, and measured performance, separating required compatibility from internal improvements and deliberate behavior changes.
- A bounded independent review for substantial or materially risky work, covering defects and proportionate maintainability findings, with explicit self-review fallback and honest status reporting.
- Short private continuation state that is checked against current artifacts after a context reset.

The default for implementation requests is to finish the usable result, including checks and corrections, without requiring the user to specify every engineering step. A short prompt does not lower the quality bar. The process scales down for focused fixes and respects requests for planning or review only. Existing host or companion-skill planning, checks, and reviews can satisfy the workflow without duplication. Material assumptions and genuine blockers remain visible.

## Install

From your target project, use the [Skills CLI](https://github.com/vercel-labs/skills) with Node.js 22.20 or later and Git:

```sh
npx skills@1.7.6 add TKY-27/Rust-in-One --skill rust-in-one
```

Choose the agents you use. Project installation is the default; add `-g` for a personal installation or `--copy` when symlinks are unsuitable. A private repository requires existing access. The installer version is pinned to the version checked for this guide; it does not pin the Skill revision.

Claude Code, Codex, Gemini CLI, Cursor, GitHub Copilot, OpenCode, Amp, Pi, Cline, Roo Code, and other clients are covered in the [installation and compatibility guide](docs/compatibility.md). It includes exact-revision installation, native paths, explicit invocation, updates, removal, and a manual-copy option without Node.js. The complete [`skills/rust-in-one`](skills/rust-in-one) directory is the portable package; retain its references and license.

The installed Skill contains only instructions, references, and a license. It adds no executable hooks or background service. The Skills CLI is a separate third-party installer; manual copying avoids running it. Keep your agent's normal permissions and follow [SECURITY.md](SECURITY.md).

The pinned installer provides 79 agent identifiers. Project installation was checked for all 79 identifiers using the package snapshot identified in the compatibility guide; native agent activation has been tested in Claude Code only. See the guide for the Cline path caveat and the distinction between installation and runtime support.

## Use

In Codex CLI or the IDE extension, mention `$rust-in-one`; in Claude Code, start a message with `/rust-in-one`. Other clients' activation commands are in the compatibility guide. Automatic selection depends on the host and prompt; discovery alone does not prove the body or references were read.

For a first run, explicitly select the Skill and give it the task, for example:

```text
$rust-in-one Make a Rust CLI for finding duplicate files in a folder. Finish it so I can use it.
```

Use `/rust-in-one` in place of `$rust-in-one` for Claude Code. Check the client's trace or activity view for the Skill read and any references required by the task. Installation does not make it an always-running plugin.

Example requests:

- “Build a Rust CLI that summarizes access logs, with JSON output.”
- “Port this C tool to native Rust, preserving its CLI behavior and meeting the current throughput.”
- “Finish this library's public API and verify it from a separate consumer.”
- “Fix the parser's handling of negative coordinates without changing its public API.”
- “Review this Rust repository for correctness, security, and maintainability without changing files. Prioritize actionable findings and state what you checked.”
- “Review the diff against main, including effects on callers and public APIs. Do not edit the code.”

The skill uses standard frontmatter and relative file links. No particular model, plugin, hook, MCP server, or companion skill is required. Execution checks need the applicable Rust toolchain; optional tools are used only when available and applicable to the task. Harness integration remains optional.

## Contents

| File | When needed |
| --- | --- |
| [SKILL.md](skills/rust-in-one/SKILL.md) | Intent, completion conditions, implementation loop, Rust decisions, review, recovery |
| [verification.md](skills/rust-in-one/references/verification.md) | Planning substantial work, product-specific checks, review and delivery |
| [migration.md](skills/rust-in-one/references/migration.md) | Before characterizing and designing a migration |
| [concurrency.md](skills/rust-in-one/references/concurrency.md) | Before services, async, or substantial threading |
| [unsafe-ffi.md](skills/rust-in-one/references/unsafe-ffi.md) | Before changing unsafe code or language boundaries |
| [performance.md](skills/rust-in-one/references/performance.md) | Before measurements, optimization, or performance claims |

## Evidence and limitations

The [evaluation notes](docs/evaluation.md) record the exact Skill snapshots, models, methods, results, and limitations of the reported trials. Those small trials include improvements, ties, and unresolved failures; they do not establish a general advantage or reliability on large projects. Later Haiku trials include a separate readability assessment by the authoring model, not Haiku or a human. Results belong to the named revisions and do not automatically carry over to the current text. Earlier Claude results remain [preliminary reports in history](https://github.com/TKY-27/Rust-in-One/blob/3967848af3fe9bbf03d99c06afa2a473deea4a0a/README.md#status).

Package validation, installation, native activation, and software quality are separate checks. The [compatibility guide](docs/compatibility.md) states which have been exercised for each host. Instructions cannot guarantee that an agent loads a reference, completes an independent review, or produces correct software; inspect the delivered evidence and remaining gaps.

## Contributing and validation

See [CONTRIBUTING.md](CONTRIBUTING.md) for focused changes, bug reports, validation, and evidence standards. For sensitive reports, follow [SECURITY.md](SECURITY.md).

Validate frontmatter with the [reference implementation](https://github.com/agentskills/agentskills/tree/main/skills-ref). The `skills-ref` 0.1.1 distribution installs the `agentskills` command:

```sh
python -m pip install -r requirements-dev.txt
agentskills validate skills/rust-in-one
python scripts/check-package.py
```

Use Python 3.10 or later. The last command checks local Markdown file links, a standalone installation copy, and matching MIT notices; it is not a substitute for schema validation and does not verify remote URLs or anchors. [CI](.github/workflows/validate.yml) runs package validation on Linux, macOS, and Windows without model calls. Generated trial projects, raw logs, hidden checks, and task/handoff notes stay outside this repository.

## License

[MIT](LICENSE). The installable directory includes [LICENSE.txt](skills/rust-in-one/LICENSE.txt) so the notice travels with copied installations.
