---
name: rust-in-one
description: Develop and finish Rust projects through architecture, implementation, verification, and review. Use when creating a Rust project, extending or repairing a Rust codebase, migrating software to Rust, or resuming substantial Rust work. Applies before Cargo files exist and to Rust components in mixed repositories. Do not select Rust for a language-undecided request merely because this skill is available, or apply its full workflow to unrelated work.
---

# Rust-in-One

Own the engineering needed to complete the user's Rust task. Scale the process to the work: a small fix needs a focused correction and relevant checks; a new project needs a coherent usable result.

## Establish the task

Read the request, applicable repository instructions, existing implementation, and tests before choosing a design. Identify the principal use case, supported environments, observable requirements, and important constraints. For substantial work, choose milestones and integration points that keep progress verifiable.

Resolve ordinary technical choices yourself. Ask only when an unanswered product question materially changes the result or an action exceeds existing authorization. State consequential assumptions. Preserve the agreed scope through implementation and review.

## Make the main use case work

Build an early path through a real boundary: a CLI invocation, an external library consumer, or a service request. Check expensive assumptions before expanding the implementation. Include meaningful failure behavior as the path develops.

Choose modules, types, and dependencies for present needs. Make ownership and state transitions clear. Use borrowing, owned values, shared state, traits, and async boundaries deliberately. Define public errors and panic behavior for callers. Add unsafe code or complex optimization only for a concrete requirement, and explain the relevant obligations.

Use compatible dependency versions and their actual documentation. Respect the project's supported toolchain, platforms, features, and API commitments. Prefer direct readable code over speculative frameworks, redundant comments, and unnecessary public APIs.

For a migration, read [migration.md](references/migration.md) before deciding replacement boundaries or claiming compatibility.

## Verify and correct

Choose checks from the product's requirements and likely failure modes. Cover the main use case and important adverse paths. Use formatting, linting, builds, and tests as a baseline; add properties, fuzzing, concurrency checks, or benchmarks where they address a concrete risk.

Read [verification.md](references/verification.md) when planning verification for substantial work, preparing an independent review, or deciding whether the result is ready to deliver. Correct causes, then verify the integrated result. Passing tests and positive AI reviews are evidence with limits.

## Work with the surrounding agent

Follow the host's permissions and instruction hierarchy. Use its existing planning and delegation facilities. Cooperate with relevant skills, reuse valid evidence, and avoid repeating work merely to satisfy this workflow. Do not assume a particular reviewer model, command, plugin, or background service exists.

For work spanning context changes, keep a concise continuation note or reuse the project's equivalent. Record the goal, important invariants, current state, unresolved findings, evidence locations, and next action. Use an authorized recovery route supported by the host, preserving existing instruction loading. On resumption, reconcile the note with the actual repository before editing; its existence alone does not ensure it was read. Keep independent reviewers free of the author's self-assessment.

## Deliver the agreed result

Check the artifact users will receive, including applicable installation, packaging, configuration, and examples. Reconcile it with the original requirements and accepted changes. Resolve known High/Critical findings before calling the result release-ready; do not silently downgrade or omit unresolved concerns.

Remove or exclude task-only notes, temporary recovery pointers, and scratch artifacts from delivery. Preserve useful project documentation and existing instructions. Inspect the delivered file set after cleanup.

Report what works, what was verified, and any material limitation. If scope or necessary verification remains incomplete, say so and identify the remaining work. Do not present a reduced implementation, temporary bridge, or unverified claim as completion.
