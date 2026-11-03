# Rust-in-One

Rust engineering guidance for an agent carrying a request through implementation, verification, and delivery.

This [Agent Skill](https://agentskills.io/specification) prioritizes new Rust CLIs, libraries, and services, then substantial Rust-native migrations, especially from C/C++. It also supports focused fixes, improvements, and reviews of existing Rust code. The skill instructs agents not to select Rust merely because the skill is installed or apply Rust procedures to unrelated languages.

## What it provides

- Concrete Rust guidance on ownership, public APIs, byte/text boundaries, arithmetic, errors, output, and dependencies.
- An early working path through the product's real interface, with verification chosen from the requirements.
- Readability and maintainability guidance: results and control flow that state their meaning, boundaries by responsibility, reuse of library behavior that matches the contract, and restructuring that preserves observable behavior.
- For changes to existing projects: tracing the affected architecture and obligations first, extending existing implementations, and checking the impact on unchanged behavior.
- For reviews of an existing repository or diff: evidence-backed findings, severity and coverage, without changing the reviewed files unless fixes are requested.
- Migration checks against defined source behavior, including errors, exit statuses, and measured performance.
- A bounded independent review for substantial or materially risky work, covering defects and proportionate maintainability findings, with explicit self-review fallback and honest status reporting.
- Short private continuation state that is checked against current artifacts after a context reset.

The process scales down for focused fixes. Existing host or companion-skill planning, checks, and reviews can satisfy the workflow without duplication. Instructions guide behavior; they cannot guarantee that an agent loads references, completes a review, or produces correct software.

## Install

From your target project, use the [Skills CLI](https://github.com/vercel-labs/skills) with Node.js 22.20 or later and Git:

```sh
npx skills@1.7.6 add TKY-27/Rust-in-One --skill rust-in-one
```

Choose the agents you use. Project installation is the default; add `-g` for a personal installation or `--copy` when symlinks are unsuitable. A private repository requires existing access. The installer version is pinned to the version checked for this guide; it does not pin the Skill revision.

Claude Code, Codex, Gemini CLI, Cursor, GitHub Copilot, OpenCode, Amp, Pi, Cline, Roo Code, and other clients are covered in the [installation and compatibility guide](docs/compatibility.md). It includes exact-revision installation, native paths, explicit invocation, updates, removal, and a manual-copy option without Node.js. The complete [`skills/rust-in-one`](skills/rust-in-one) directory is the portable package; retain its references and license.

The installed Skill contains only instructions, references, and a license. It adds no executable hooks or background service. The Skills CLI is a separate third-party installer; manual copying avoids running it. Keep your agent's normal permissions and follow [SECURITY.md](SECURITY.md).

The pinned installer provides 79 agent identifiers. Project installation was checked for all 79 identifiers using an earlier package revision; native agent activation has been tested in Claude Code only. See the guide for the Cline path caveat and the distinction between installation and runtime support.

## Use

In Codex CLI or the IDE extension, mention `$rust-in-one`; in Claude Code, start a message with `/rust-in-one`. Other clients' activation commands are in the compatibility guide. Automatic selection depends on the host and prompt; discovery alone does not prove the body or references were read.

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
| [SKILL.md](skills/rust-in-one/SKILL.md) | Activation, scope, engineering defaults, readability, verification, review, recovery |
| [verification.md](skills/rust-in-one/references/verification.md) | Planning substantial work, product-specific checks, review and delivery |
| [migration.md](skills/rust-in-one/references/migration.md) | Before characterizing and designing a migration |
| [concurrency.md](skills/rust-in-one/references/concurrency.md) | Before services, async, or substantial threading |
| [unsafe-ffi.md](skills/rust-in-one/references/unsafe-ffi.md) | Before changing unsafe code or language boundaries |
| [performance.md](skills/rust-in-one/references/performance.md) | Before measurements, optimization, or performance claims |

## Evidence and limitations

Experimental. The [evaluation notes](docs/evaluation.md) identify the frozen skill snapshot used in the reported trials, together with the models, methods, results, and limitations. Later sections record smaller Haiku generation and in-task review trials, plus a separate readability assessment using the authoring model. That assessment was not performed with Haiku or by a human. Results apply only to the named revisions; the review-only workflow has not yet had a behavioral trial. A passing task or favorable review is not evidence of general effectiveness. Earlier Claude results remain [preliminary reports in history](https://github.com/TKY-27/Rust-in-One/blob/3967848af3fe9bbf03d99c06afa2a473deea4a0a/README.md#status), not independently reproduced measurements.

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
