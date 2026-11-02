# Concurrency, async, and services

Read this before writing a network service, async code, or nontrivial multithreaded code.

## Choose the model

- **Synchronous code**: CLIs and batch tools that read files, plus most libraries. Simplest to test and reason about.
- **Threads**: a few long-lived workers or blocking work. Use `std::thread::scope` to borrow data without `Arc`, and `rayon` for data-parallel loops over collections. Accumulate results per thread and merge them, rather than sharing a locked accumulator.
- **Async (`tokio`)**: many concurrent sockets, servers, clients issuing parallel requests, or timers. Async does not make CPU work faster.

Libraries should not force a runtime on callers. Expose a synchronous API, or `async fn`s that run on the caller's runtime, and never create a runtime inside a library function. Calling `Runtime::block_on` or `Handle::block_on` from inside an async context panics.

## Async rules

- **Never block the executor.** `std::fs`, `std::thread::sleep`, synchronous HTTP or database clients, heavy computation, and long-held `std::sync::Mutex` locks stall every task on that worker. Use async equivalents, or move the work to `tokio::task::spawn_blocking` (a CPU-heavy batch can go to `rayon` instead).
- **Locks and `.await`.** A `std::sync::Mutex` is fine for short critical sections, but never hold its guard across `.await`: scope the guard in a block. Use `tokio::sync::Mutex` only when a lock must be held across an await point. Never hold any lock while doing network I/O.
- **Backpressure and limits.** Use bounded channels (`mpsc::channel(n)`). Limit fan-out with `Semaphore`, `JoinSet` plus a cap, or `buffer_unordered(n)`. Unbounded channels, unbounded spawning, and in-memory queues grow until the process dies under load.
- **Timeouts everywhere a peer can stall.** `reqwest` sets no request timeout by default, so set one on the client. Servers need request timeouts and body-size limits (`tower_http::timeout::TimeoutLayer`, `axum::extract::DefaultBodyLimit` or `RequestBodyLimitLayer`). Outbound connections need connect and read timeouts.
- **Cancellation.** A future can be dropped at any `.await`, which is what `select!`, `timeout`, and client disconnects do. Keep state consistent across await points. In `tokio::select!` loops, use only cancellation-safe operations, as stated in each method's "Cancel safety" docs (`mpsc::Receiver::recv` is cancellation safe; `AsyncReadExt::read_exact` is not), or keep the in-progress future outside the loop and poll it by reference.
- **Task failures.** A spawned task's panic or error surfaces only through its `JoinHandle`. Join tasks (`JoinSet`), propagate or log their errors, and do not leak detached tasks that outlive shutdown.
- **Graceful shutdown.** Handle `tokio::signal::ctrl_c()` and, on Unix, SIGTERM (`tokio::signal::unix`). Stop accepting work, let in-flight work finish within a deadline (`axum::serve(...).with_graceful_shutdown(...)`), propagate cancellation to background tasks (`tokio_util::sync::CancellationToken`), then flush logs and state.

## Shared state

- Prefer ownership transfer (channels, one task owning a resource and serving requests) over shared mutable state.
- For a service's shared state, use `Arc<AppState>` with fine-grained interior locks or atomics for the parts that change. Keep critical sections short and acquire multiple locks in one consistent order.
- Use atomics only for simple counters and flags, unless you can state the ordering argument. `Relaxed` is fine for independent statistics counters. Publishing data to another thread needs `Release`/`Acquire` or a lock. Custom lock-free structures need `loom` tests and review.
- `Rc`, `RefCell`, and `Cell` are single-threaded; the compiler enforces this through `Send`/`Sync`. Do not wrap things in `unsafe impl Send` to silence it.

## Service checklist

- Configuration comes from flags, environment, or files, is validated at startup, and errors exit with a clear message rather than a panic.
- Structured logs (`tracing`) include request identifiers and avoid secrets.
- Health and readiness endpoints reflect dependency state where the deployment uses them.
- Input validation, size limits, and timeouts apply on every route that accepts external input.
- Tests start the real server on `127.0.0.1:0` and issue real requests, including malformed ones and shutdown during a request.

## Testing concurrent code

- `#[tokio::test]` uses a current-thread runtime by default. Use `flavor = "multi_thread"` when the behavior under test depends on parallelism.
- Use `start_paused = true` and `tokio::time::advance` for timer logic instead of real sleeps.
- Run concurrency tests repeatedly; a single pass proves little. Use `loom` for custom synchronization primitives, and ThreadSanitizer (nightly, `-Zsanitizer=thread`) where available.
