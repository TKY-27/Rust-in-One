# Rust-in-One

From one request to a complete Rust project.

Rust-in-One is an [Agent Skill](https://agentskills.io/specification) for developing Rust software with attention to correctness, security, performance, and maintainability. Its first priority is building new projects from a user's goal. It also provides a starting point for improving existing projects and migrating software to Rust.

The name describes one delegated task, including the implementation, verification, review, and corrections needed to finish it.

## Status

This is an early foundation: a short core workflow and two focused references. The structure and wording are open to improvement through practical use. Cross-harness behavior and improvements in project quality have not yet been measured.

## Use

Install the complete [skills/rust-in-one](skills/rust-in-one) directory using your coding agent's skill installation mechanism. Keep the directory named `rust-in-one` and preserve its `references` directory. Follow your harness's documentation for discovery paths and explicit invocation syntax.

The skill uses standard `SKILL.md` metadata and relative references. It has no required plugin, hook, MCP server, model, or companion skill. Automatic selection depends on the host; confirm that the skill is visible before relying on it.

Example requests:

- Build a Rust CLI that indexes a directory and searches its contents.
- Finish this Rust library, including its external API and installation checks.
- Migrate this C++ component to Rust while preserving its protocol and performance requirements.

For a first local check, confirm discovery, try a bounded Rust task, and inspect the resulting behavior and verification evidence. Also try an unrelated task in a mixed repository to check that the skill does not take over work outside its scope.

## Contents

| File | Purpose |
| --- | --- |
| [SKILL.md](skills/rust-in-one/SKILL.md) | Scope, engineering workflow, and completion responsibilities |
| [verification.md](skills/rust-in-one/references/verification.md) | Selecting checks, independent review, and delivery |
| [migration.md](skills/rust-in-one/references/migration.md) | Compatibility and Rust-native migration decisions |

## Contributing

Prefer changes tied to a concrete engineering failure or a useful task. Keep the core short, read additional guidance only when relevant, and reuse good existing knowledge. New abstractions, dependencies, and procedures should solve an observed problem. Keep harness-specific integration optional.

When reporting behavior, include the skill revision, harness/model, relevant configuration, task, and observed result. Distinguish format validation, manual trials, and comparative evidence. Avoid effectiveness claims based only on successful invocation or favorable model reviews.

## License

[MIT](LICENSE). Preserve the license notice when redistributing the skill.
