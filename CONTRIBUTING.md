# Contributing

Rust-in-One is a portable Agent Skill for delivering maintainable Rust software. Contributions should improve engineering decisions and their verification while keeping the instructions small and usable across hosts.

## Propose a focused change

- Explain the concrete error, ambiguity, compatibility issue, or transferable failure the change addresses. Link technical claims to primary sources.
- Keep common decisions in `skills/rust-in-one/SKILL.md`; put specialized detail in a reference linked where it is needed. Avoid repeating existing guidance or adding mandatory ceremony to small fixes.
- Preserve the standard directory format and the complete installed package. Host-specific installation advice belongs in [compatibility.md](docs/compatibility.md), not in duplicate Skill bodies or compulsory hooks.
- Keep generated projects, raw model logs, private acceptance checks, temporary state, and agent handoff prompts outside this repository. Remove credentials and personal information from examples.

For bugs, include the Skill commit, client and version, model/settings when relevant, a minimal request or reproduction, and expected versus observed behavior. Use [SECURITY.md](SECURITY.md) for sensitive reports. Be respectful; critique the work and evidence, not the contributor.

## Validate locally

Use Python 3.10 or later in a virtual environment. From the repository root:

```sh
python -m pip install -r requirements-dev.txt
agentskills validate skills/rust-in-one
python scripts/check-package.py
git diff --check
```

The schema validator checks the Agent Skills format. The package check verifies local Markdown file links, a standalone copy, and matching MIT notices. Neither validates external URLs or heading anchors. The [CI workflow](.github/workflows/validate.yml) runs package checks on Linux, macOS, and Windows; it does not call a model or measure Skill effectiveness.

For installer changes, use a disposable target project and the pinned command in the [compatibility guide](docs/compatibility.md). Check the installed body, references, and license. Directory installation, native discovery, actual loading, and instruction following are separate observations.

## Report evaluation evidence

State the exact Skill revision, host, model, reasoning setting, task, sample count, resource limits, and checks actually run. Preserve failures and ties. Distinguish planned checks from completed ones and price estimates from bills. State where reproduction material is available and whether it will persist. A model's favorable review is not a correctness result.

For paired trials, freeze the request and acceptance criteria first, give both conditions the same tools and limits, use fresh isolated contexts, and disclose accidental contamination or repairs to the evaluator. Do not select examples only because the Skill wins. Small demonstrations should be described as examples, not evidence of general effectiveness.

Include brief new-project requests when evaluating autonomous development: a fully specified task already supplies some decisions the Skill is meant to help make. Keep regression tasks and unseen tasks separate, repeat comparisons before claiming an effect, and assess correctness, failure handling, readability, maintenance changes, and resource use together. Test count and code length are not quality scores. Record actual Skill/reference loading and reviewer inputs when available; a final report alone does not establish that the instructions were followed.

## Before a release

Review the exact commit, require passing validation, check the installation instructions against current primary sources, and keep the evidence limitations accurate. Describe supported installation paths and observed behavior precisely; do not treat package validation as proof of better generated software. The maintainer chooses the version tag and publication time; CI does not publish automatically. If enabling public vulnerability reporting, confirm that the channel actually works before advertising it.

Contributions are provided under the repository's [MIT license](LICENSE). Keep the root license and the installed `LICENSE.txt` identical.
