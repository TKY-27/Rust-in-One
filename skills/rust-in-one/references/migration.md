# Migrating to Rust

## Define what must remain compatible

Pin the source revision. Identify the behaviors, formats, protocols, assets, targets, public interfaces, and performance requirements that matter to users. Clarify which foreign components, if any, may remain in the delivered system.

Separate intended behavior from source defects, undefined behavior, and nondeterminism. Record accepted differences. Do not silently discard difficult features or treat translated line counts as completion.

## Choose a Rust-native design

Understand the source's data model, ownership, state transitions, and integration boundaries before translating it. Choose whole replacement, incremental FFI, or another transition strategy according to coupling and available verification.

Check arithmetic and representation assumptions, layout, ownership across FFI, unwinding, shared-state lifetimes, and platform-specific optimized paths. Preserve necessary invariants while choosing clear Rust types and APIs. Do not replace every shared structure with a lock or assume an atomic type substitution preserves the original algorithm.

Keep temporary bridges explicit. A wrapper or residual dependency on the old implementation does not satisfy a requirement to replace it.

## Establish equivalence and finish

Use differential tests against defined source behavior, independent models or properties, and real integration paths. Investigate disagreements rather than copying potentially incorrect source output into expected answers.

Measure required performance on representative workloads with comparable build settings and hardware. For statistical comparisons, declare acceptable margins and stopping rules before interpreting results. Preserve result quality as well as speed; inconclusive results remain inconclusive.

Validate the integrated product and its distribution. Report covered requirements, accepted differences, remaining foreign components, and material verification gaps. Apply the core skill's completion and review responsibilities to the whole migration.
