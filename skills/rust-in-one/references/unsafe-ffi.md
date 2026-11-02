# Unsafe code and FFI

Read this before writing or changing `unsafe` code, `extern` declarations, or anything that crosses a language boundary.

## When unsafe is justified

Use it for FFI, for a safe abstraction that neither std nor a maintained crate provides, or for a measured performance need that safe code cannot meet. Check the safe options first: iterators and slice patterns often remove bounds checks, and `bytemuck` or `zerocopy` cover most byte reinterpretation. If unsafe stays, wrap it in a small module whose public API is safe for every possible input.

## Writing it

- The safety boundary is the module, not the block. Any code that can modify the fields an `unsafe` block relies on is part of the safety argument, so keep those fields private.
- Give every `unsafe` block a `// SAFETY:` comment naming the invariants it relies on and why they hold here. Give every `unsafe fn` and `unsafe trait` a `# Safety` section stating the caller's obligations. Enable `clippy::undocumented_unsafe_blocks`. Edition 2024 already warns on unsafe operations inside `unsafe fn` without an inner `unsafe` block.
- Common sources of undefined behavior:
  - creating a reference (`&`/`&mut`) to uninitialized, misaligned, or dangling memory. Use `MaybeUninit`, raw pointers, `&raw const` / `&raw mut`, and `read_unaligned` instead;
  - aliasing violations: a `&mut` coexisting with any other live reference or with use of a pointer derived from one;
  - invalid values: a `bool` other than 0 or 1, an out-of-range `char`, an enum with an unlisted discriminant, a null reference or `NonNull`. Never transmute integers from outside into such types;
  - `slice::from_raw_parts` with a null or misaligned pointer, even for length 0 (use `NonNull::dangling()`), or with a total size above `isize::MAX` bytes;
  - `Vec::set_len` over uninitialized elements; lifetimes extended through raw pointers; data races through shared raw pointers.

## FFI boundaries

- Calling C: generate declarations with `bindgen`, in `build.rs` or pre-generated and committed, and compile bundled C/C++ with the `cc` crate. Exposing Rust to C: `extern "C"` functions with `#[unsafe(no_mangle)]` and headers from `cbindgen`. C++: prefer `cxx` for the types it supports over hand-written `extern "C"` shims.
- Edition 2024 syntax: `unsafe extern "C" { ... }`; items inside may be declared `safe fn` when calling them is always sound.
- Types: `#[repr(C)]` on shared structs; `std::ffi::{c_int, c_char, c_void, CStr, CString}`. Receive C enums as integers and convert with `TryFrom`, never as Rust enums. Use `bool` only where the C side uses `bool`/`_Bool`.
- Strings: `CString::new(s)?.as_ptr()` passed directly to a call is fine only if nothing keeps the pointer afterwards; storing it creates a dangling pointer as soon as the temporary drops. Bind the `CString` to a variable that outlives every use. `CStr::from_ptr` requires a valid NUL-terminated string that lives as long as the borrow.
- Ownership: memory is freed by the allocator that allocated it. Rust-allocated objects handed to C need an exported `*_free` function (`Box::into_raw` / `Box::from_raw`). Document who owns every pointer, and check incoming pointers for null.
- Panics: since Rust 1.81, a panic unwinding out of an `extern "C"` function aborts the process. At every exported entry point, wrap the body in `std::panic::catch_unwind` and convert failures to error codes. Use `extern "C-unwind"` only when both sides are designed for unwinding.
- Threads and callbacks: find out whether the foreign library is thread-safe and reentrant. Encode the answer in `Send`/`Sync` (raw pointers make a wrapper `!Send`/`!Sync` by default; add `unsafe impl` only with a documented reason). Callbacks use `extern "C" fn` trampolines with a `*mut c_void` context whose lifetime covers every possible invocation.

## Verifying it

- Run Miri on the pure-Rust unsafe code: `cargo +nightly miri test`, which needs the nightly toolchain with the `miri` component. Miri cannot execute foreign calls, so isolate the logic so it can be tested without them.
- For FFI code, run the tests under AddressSanitizer (nightly `-Zsanitizer=address`; see the rustc unstable book for current flags) or Valgrind on the built test binary.
- Fuzz or property-test the safe API around the unsafe core with adversarial inputs, since the safe API must be sound for all of them.
- In review, check every `SAFETY:` comment against the code. A missing or vague justification is a finding.
