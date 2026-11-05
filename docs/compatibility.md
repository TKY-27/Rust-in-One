# Installation and compatibility

Rust-in-One is one standard [Agent Skills](https://agentskills.io/specification) directory. The installed package is [`skills/rust-in-one`](../skills/rust-in-one): `SKILL.md`, five reference files, and `LICENSE.txt`. It has no executable hooks, required MCP servers, model-specific settings, or companion-skill dependency.

## Install with the Skills CLI

Use [Vercel's Skills CLI](https://github.com/vercel-labs/skills) with Node.js 22.20 or later and Git. The examples pin the installer to **1.7.6**; package installation was rechecked on **2026-11-04**. Run from the project where the agent will work:

```sh
npx skills@1.7.6 add TKY-27/Rust-in-One --skill rust-in-one
```

Choose the agents you use. For an explicit selection:

```sh
npx skills@1.7.6 add TKY-27/Rust-in-One --skill rust-in-one --agent codex --agent claude-code
```

Project scope is the default. Add `-g` for a personal installation, or `--copy` for independent copies instead of symlinks. Private repositories require existing Git, GitHub CLI, or SSH access. See the installer's [source formats and authentication](https://github.com/vercel-labs/skills/blob/7a5e920bead4b1039a6d6df5d7e1163b7b09423a/docs/commands.md) documentation; do not put credentials in install commands.

For an exact Skill revision, check out that commit locally and pass the checkout's absolute path instead of `TKY-27/Rust-in-One`. Pinning the installer version alone does not pin the Skill revision. The [upstream agent catalog](https://github.com/vercel-labs/skills/blob/7a5e920bead4b1039a6d6df5d7e1163b7b09423a/docs/agents.md) covers 79 identifiers, including `universal`, and additional clients beyond the table below. Select the clients you need; installing to every destination is unnecessary for normal use.

## Native locations and activation

These are documented **manual-copy locations**, checked against each linked primary source on 2026-11-03. Append `rust-in-one/` to a directory in the table and copy the complete package. The installer may choose a different supported alias. `~` means your home directory; configuration overrides and remote environments can change the effective location.

| Harness | Installer identifier | Project directory | Personal directory | Explicit use or discovery check |
| --- | --- | --- | --- | --- |
| [Claude Code](https://code.claude.com/docs/en/skills) | `claude-code` | `.claude/skills/` | `~/.claude/skills/` | Start a message with `/rust-in-one` |
| [Codex CLI / IDE](https://learn.chatgpt.com/docs/build-skills) | `codex` | `.agents/skills/` | `~/.agents/skills/` | Mention `$rust-in-one`; inspect `/skills` |
| [Gemini CLI](https://geminicli.com/docs/cli/skills/) | `gemini-cli` | `.gemini/skills/` or `.agents/skills/` | `~/.gemini/skills/` or `~/.agents/skills/` | `/skills list`, `/skills reload`; ask to use `rust-in-one` |
| [Cursor](https://cursor.com/docs/skills) | `cursor` | `.cursor/skills/` or `.agents/skills/` | `~/.cursor/skills/` or `~/.agents/skills/` | Type `/` and select the Skill |
| [GitHub Copilot](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/add-skills) | `github-copilot` | `.github/skills/`, `.claude/skills/`, or `.agents/skills/` | `~/.copilot/skills/` or `~/.agents/skills/` | Ask to use `rust-in-one`; controls vary by Copilot surface |
| [OpenCode](https://docs.opencode.ai/docs/skills/) | `opencode` | `.opencode/skills/` or `.agents/skills/` | `~/.config/opencode/skills/` or `~/.agents/skills/` | Ask to load `rust-in-one` with the native `skill` tool |
| [Amp](https://ampcode.com/docs/customize/skills) | `amp` | `.agents/skills/` | `~/.config/agents/skills/` or `~/.agents/skills/` | `amp skills list`; ask to load `rust-in-one` |
| [Pi](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/skills.md) | `pi` | `.agents/skills/` | `~/.agents/skills/` | `/skill:rust-in-one`; `/reload` after changes |
| [Cline](https://docs.cline.bot/customization/skills) | `cline` | `.cline/skills/` | `~/.cline/skills/` | Type `/` and select the Skill; inspect the Skills menu |
| [Roo Code](https://roocodeinc.github.io/Roo-Code/features/skills/) | `roo` | `.roo/skills/` or `.agents/skills/` | `~/.roo/skills/` or `~/.agents/skills/` | Ask to use `rust-in-one` |

**Cline:** the pinned installer targets `.agents/skills/`, while the linked Cline Skills page documents `.cline/skills/`. If discovery fails, use the documented manual-copy path. Installation success alone does not resolve this documentation difference.

For example, from a checkout of this repository, install manually for one Codex project:

```sh
mkdir -p /path/to/project/.agents/skills
cp -R skills/rust-in-one /path/to/project/.agents/skills/
```

On Windows, copy the directory with your file manager or PowerShell to the equivalent project location. You do not need Node.js or Python for a manual installation. The target Rust project still needs its applicable toolchain and execution environment.

Install where the agent actually runs. Personal files on a laptop may not reach a cloud session, remote worker, or container. Follow the client's workspace trust and activation-consent flow. Avoid duplicate same-named copies in multiple searched directories; host precedence rules differ.

## Confirm that it is used

Check the client's Skill list, explicitly invoke or request `rust-in-one`, and confirm that the body is loaded. On a migration request, inspect the available trace for a read of `references/migration.md`. A discovery entry is not evidence that either the body or its references were read. Automatic selection is host- and prompt-dependent; explicit invocation is useful when predictable activation matters.

For older clients with file access but no native Skills support, ask the agent to read the local `skills/rust-in-one/SKILL.md` and the references required by the task. This is manual use, not native integration. Do not work around a host's permission restrictions.

## Autonomous work across hosts

The Skill guides work from a brief request through implementation, checks, review, and corrections. The host supplies execution and continuation. Reuse its existing task and review facilities; no particular orchestration plugin is required.

| Capability | Use when available | If unavailable |
| --- | --- | --- |
| Build and execution tools | Run the applicable Rust checks and exercise the delivered interface | Report the specific unverified requirement; instructions do not make an unexecuted check pass |
| Private state and continuation | Retain the task contract, next obligation, artifact revision, evidence, and checkpoint location; reconcile them with the files on resume | Preserve a resumable checkpoint where possible and identify the limitation; the package cannot restart a stopped host |
| Independent review | Give a fresh reviewer the request and artifact, excluding implementer verdicts and continuation notes | Perform a distinct self-review and report the missing independent review accurately |

These are capability requirements, not additional claims of runtime testing for every client. Keep task state outside the delivered product and its repository instruction files. Host-specific automation may help preserve or resume work, but it must respect the host's permissions and the user's task scope. It is not installed by this package.

## Update or remove

For a Skills CLI installation:

```sh
npx skills@1.7.6 list
npx skills@1.7.6 check
npx skills@1.7.6 update rust-in-one -p
npx skills@1.7.6 remove rust-in-one
```

Use `list -g`, `update rust-in-one -g`, or `remove rust-in-one -g` for personal installations. Review changes before updating. Several clients share `.agents/skills/`; removing a shared installation can affect all of them.

For a manual copy, preserve local customizations, replace the installed directory with the complete new copy, and confirm discovery again. Merging directories can leave obsolete reference files. To uninstall, remove only the `rust-in-one` directory you installed, then refresh the client's Skill list.

## What has been verified

| Layer | Evidence | Limit |
| --- | --- | --- |
| Package format | `skills-ref` 0.1.1 schema validation and the repository package check | Does not measure agent behavior |
| Installer destinations | Skills CLI 1.7.6 installed the package snapshot below for all 79 identifiers on 2026-11-04, producing 53 distinct project locations on Linux | No native host execution in this check |
| Copied contents | All seven files present at every destination; 52 copies byte-identical; Eve's copy reformatted frontmatter with equal parsed metadata and an unchanged Markdown body apart from leading whitespace | Installer-specific transformations may change in later versions |
| Default installation mode | Codex, Claude Code, Cursor, Gemini CLI, Copilot, and OpenCode selected together; shared `.agents/skills/` copy and Claude Code symlink verified against all seven source files | Linux project installation only; personal installations were not exercised |
| Native activation and task behavior | Claude Code trials recorded in [evaluation.md](evaluation.md) | Partial activation; small tasks and limited models/revisions |
| Other native hosts | Primary-source installation paths and commands above | Native activation and behavior have not been exercised here |

The all-agent copy check used Skill Git tree `b63cd65b311f821db2bf2b3e275908697f6a6229` with Node.js 24.22.1. Compare a checkout's package with `git rev-parse HEAD:skills/rust-in-one`. The default-mode symlink check used the earlier `3ed7139` package. The complete installer registry and its release source are pinned at [`7a5e920`](https://github.com/vercel-labs/skills/tree/7a5e920bead4b1039a6d6df5d7e1163b7b09423a). For a disposable packaging check, run the following from an empty temporary project and compare the installed files with the source package:

```sh
npx skills@1.7.6 add /absolute/path/to/Rust-in-One --skill rust-in-one --agent '*' --copy --yes
```

This broad installation coverage is not a claim that every harness or model has been tested, or that all agents follow the instructions equally well.
