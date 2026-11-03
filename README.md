# Rust-in-One

Rust engineering guidance for an agent carrying a request through implementation, verification, and delivery.

This [Agent Skill](https://agentskills.io/specification) prioritizes new Rust CLIs, libraries, and services, then substantial Rust-native migrations, especially from C/C++. It also supports focused fixes and improvements to existing Rust code. It does not select Rust merely because the skill is installed, or apply Rust procedures to unrelated languages.

## What it provides

- Concrete Rust guidance on ownership, public APIs, byte/text boundaries, arithmetic, errors, output, and dependencies.
- An early working path through the product's real interface, with verification chosen from the requirements.
- Migration checks against defined source behavior, including errors, exit statuses, and measured performance.
- A bounded independent review for substantial or materially risky work, with explicit self-review fallback and honest status reporting.
- Short private continuation state that is checked against current artifacts after a context reset.

The process scales down for focused fixes. Existing host or companion-skill planning, checks, and reviews can satisfy the workflow without duplication. Instructions guide behavior; they cannot guarantee that an agent loads references, completes a review, or produces correct software.

## Install and use

Copy the **whole** [`skills/rust-in-one`](skills/rust-in-one) directory from the revision you intend to use, including `references/` and `LICENSE.txt`:

| Client | Project location | Personal location |
| --- | --- | --- |
| [Codex](https://learn.chatgpt.com/docs/build-skills) | `.agents/skills/rust-in-one/` | `~/.agents/skills/rust-in-one/` |
| [Claude Code](https://code.claude.com/docs/en/skills) | `.claude/skills/rust-in-one/` | `~/.claude/skills/rust-in-one/` |
| Other [Agent Skills clients](https://agentskills.io/clients) | Consult that client's documentation | Consult that client's documentation |

For example, from this checkout, install for one Codex project:

```sh
mkdir -p /path/to/project/.agents/skills
cp -R skills/rust-in-one /path/to/project/.agents/skills/
```

Use your actual project path. When updating, replace the installed skill after preserving any local customizations; merging copies can leave obsolete files. Confirm discovery in the client, then explicitly invoke `$rust-in-one` in Codex or `/rust-in-one` in Claude Code to check loading. Automatic selection depends on the host and prompt; discovery alone does not prove the body or references were read.

Example requests:

- “Build a Rust CLI that summarizes access logs, with JSON output.”
- “Port this C tool to native Rust, preserving its CLI behavior and meeting the current throughput.”
- “Finish this library's public API and verify it from a separate consumer.”
- “Fix the parser's handling of negative coordinates without changing its public API.”

Only standard skill frontmatter and relative file links are required. No particular model, plugin, hook, MCP server, or companion skill is required. Execution checks need the applicable Rust toolchain; optional tools are used only when available or justified. Harness integration remains optional.

## Contents

| File | When needed |
| --- | --- |
| [SKILL.md](skills/rust-in-one/SKILL.md) | Activation, scope, engineering defaults, verification, review, recovery |
| [verification.md](skills/rust-in-one/references/verification.md) | Planning substantial work, product-specific checks, review and delivery |
| [migration.md](skills/rust-in-one/references/migration.md) | Before characterizing and designing a migration |
| [concurrency.md](skills/rust-in-one/references/concurrency.md) | Before services, async, or substantial threading |
| [unsafe-ffi.md](skills/rust-in-one/references/unsafe-ffi.md) | Before changing unsafe code or language boundaries |
| [performance.md](skills/rust-in-one/references/performance.md) | Before measurements, optimization, or performance claims |

## Evidence and limitations

Experimental. See [evaluation notes](docs/evaluation.md) for the tested revisions, models, methods, results, and limitations. A passing task or favorable review is not evidence of general effectiveness. Earlier Claude results remain [preliminary reports in history](https://github.com/TKY-27/Rust-in-One/blob/3967848af3fe9bbf03d99c06afa2a473deea4a0a/README.md#status), not independently reproduced measurements.

## Contributing and validation

Tie guidance to a technical error or a transferable observed failure. Prefer a small core with specialized references linked at the decision point. Avoid mandatory tools or procedures that add overhead without product value.

Validate frontmatter with the [reference implementation](https://github.com/agentskills/agentskills/tree/main/skills-ref). The `skills-ref` 0.1.1 distribution installs the `agentskills` command:

```sh
python -m pip install skills-ref==0.1.1
agentskills validate skills/rust-in-one
python scripts/check-package.py
```

The last command checks local file links, a standalone installation copy, and matching MIT notices; it is not a substitute for schema validation and does not verify remote URLs or anchors. Keep generated trial projects, raw logs, hidden checks, and task/handoff notes outside this repository. Report model/settings, skill revision, checks actually run, failures, resource limits, and missing measurements when contributing evaluation results.

## License

[MIT](LICENSE). The installable directory includes [LICENSE.txt](skills/rust-in-one/LICENSE.txt) so the notice travels with copied installations.
