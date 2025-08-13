---
this_file: REVIEW/TODO-cod.md
title: Repository Improvement Plan (Proposals)
generated_by: codex-cli
generated_reason: repository review and planning
---

# Improvement Plan and Ideas

This plan proposes concrete, example-illustrated enhancements to improve twat-cache’s reliability, developer experience, and documentation. It does not change code yet; it outlines actionable steps to implement next.

## Goals

- Reliability: predictable behavior across engines with graceful fallbacks.
- UX: clear docs, informative logging, simple CLI for common actions.
- Performance: measurable improvements with reproducible benchmarks.
- Maintainability: consistent types, tests, and CI coverage across optional backends.

## High-Impact Proposals

1) Close the Redis Gap (Docs vs Code)

- Problem: README references Redis support, but no `redis.py` engine exists in `src/twat_cache/engines/`.
- Options:
  - A) Remove/adjust Redis docs to avoid promising unsupported features.
  - B) Implement `RedisCacheEngine` with `redis` (sync) and/or `aioredis` (async) as optional extras.
- Proposal: Implement minimal sync Redis engine as optional extra and document it clearly. Provide safe fallbacks.
- Sketch:
  ```python
  # src/twat_cache/engines/redis.py
  from .base import BaseCacheEngineProtocol
  from ..config import CacheConfig
  import redis

  class RedisCacheEngine(BaseCacheEngineProtocol):
      name = "redis"

      @classmethod
      def is_available(cls) -> bool:
          try:
              import redis  # noqa: F401
              return True
          except Exception:
              return False

      def __init__(self, config: CacheConfig):
          self._config = config
          self._client = redis.Redis(host=config.redis_host or "localhost", port=config.redis_port or 6379, db=config.redis_db or 0)

      def cache(self, func):
          def wrapper(*args, **kwargs):
              key = self._make_key(func, args, kwargs)
              val = self._client.get(key)
              if val is not None:
                  return self._deserialize(val)
              res = func(*args, **kwargs)
              self._client.setex(key, self.config.ttl or 0, self._serialize(res))
              return res
          return wrapper
  ```
- Update: add `redis` to `optional-dependencies` extras, extend manager registration, add tests and docs matrix.

2) Add Simple CLI for Cache Ops

- Add an optional CLI entry with commands: `list`, `clear [name]`, `stats`.
- Benefits: quick cache maintenance and demo, helpful in examples/tests.
- Sketch:
  ```python
  # src/twat_cache/__main__.py (extend)
  import fire
  from twat_cache.cache import clear_cache, get_stats

  class CLI:
      def clear(self, name: str | None = None):
          clear_cache(name)
          return {"cleared": name or "all"}

      def stats(self):
          return get_stats()

  if __name__ == "__main__":
      fire.Fire(CLI)
  ```
- Docs: add CLI examples in `src_docs/user-guide/quickstart.md`.

3) Strengthen Configuration and Paths

- Add optional env overrides (e.g., `TWAT_CACHE_DIR`, `TWAT_CACHE_TTL`).
- Standardize cache directories with `platformdirs` everywhere (already listed under `all`).
- Document precedence: explicit args > env > defaults.

4) Improve Logging and Diagnostics

- Use `loguru` consistently with a verbose flag and structured context for engine selection and fallbacks.
- Emit a one-line summary per chosen engine and reason, e.g.:
  "ucache selected DiskCacheEngine (joblib unavailable; folder_name set)".

5) Test Coverage for Optional Backends

- Parametrize tests to run with/without optional extras; ensure graceful fallback when extras missing.
- Add async engine tests for cancellation/timeouts.
- Add property-based tests (hypothesis) for key-generation stability and collision safety.

6) Performance Benchmarks and Guidance

- Stabilize `tests/test_benchmark.py` with fixed data ranges and hist outputs.
- Add a small `examples/benchmark_matrix.py` to compare engines by size/ttl.
- Document results and guidance (which engine for which workload).

7) Documentation Enhancements

- Add an “Engine Matrix” page comparing features and requirements.
- Expand Quickstart with copy-paste minimal examples for each decorator.
- Add “Troubleshooting” with common pitfalls (e.g., unhashable args, serialization, key size).

8) Public API Review and Type Hygiene

- Ensure exported symbols in `__init__.py` match docs; deprecate aliases with warnings.
- Finalize protocols and narrow Any usage in engines.
- Publish `py.typed` consistently (already present) and fix typing gaps.

## Detailed Task Breakdown (with Examples)

- Engine Registration Audit
  - Verify `CacheEngineManager` registers new `RedisCacheEngine` conditionally.
  - Add unit tests: selection with `preferred_engine="redis"` and fallback when unavailable.

- Env-based Config Overrides
  - Example:
    ```python
    # src/twat_cache/config.py
    from os import getenv
    def create_cache_config(**kw):
        ttl = kw.get("ttl") or int(getenv("TWAT_CACHE_TTL", "0") or 0)
        folder = kw.get("folder_name") or getenv("TWAT_CACHE_DIR")
        ...
    ```
  - Tests: set env in pytest with monkeypatch to assert effective config.

- Keying/Serialization Guidance
  - Add docs showing how to use `secure=True` and custom key builders for unhashable args.
  - Example:
    ```python
    from twat_cache import mcache
    @mcache(secure=True)
    def fetch(data: dict) -> int:
        return len(data)
    ```

- CLI Examples in Docs
  - Show `python -m twat_cache clear` and `python -m twat_cache stats` usage.

- Bench Guidance Snippet
  - Example code to compare engines:
    ```python
    from twat_cache import mcache, bcache, fcache
    @mcache(maxsize=1024)
    def hot(x): return x*x
    @bcache(ttl=600)
    def warm(x): return x*x
    @fcache(folder_name="big", compress=True)
    def cold(x): return bytes(x)
    ```

## Phased Roadmap

Phase 1: Correctness and Clarity (1–2 days)

- [ ] Decide Redis path: implement or adjust docs
- [ ] Improve engine selection logs (why/how selected)
- [ ] Add troubleshooting doc section
- [ ] Tighten exported symbols and deprecation notes

Phase 2: UX and Config (2–3 days)

- [ ] Add env overrides and document precedence
- [ ] Standardize platformdirs usage in paths
- [ ] Extend CLI for `clear` and `stats` with tests

Phase 3: Tests and Performance (2–3 days)

- [ ] Parametrize tests for with/without optional extras
- [ ] Add async-specific reliability tests
- [ ] Stabilize and document benchmark scenarios

Phase 4: Optional Engines and Docs (2–4 days)

- [ ] Implement `RedisCacheEngine` (if chosen)
- [ ] Add engine matrix doc page
- [ ] Add more examples to `examples/` and user-guide

## Risks and Mitigations

- Optional deps drift: Pin minimal versions in extras and CI matrix; detect at import with helpful messages.
- Cross-platform path issues: Rely on `platformdirs`; add tests for Windows/macOS/Linux.
- Async nuances: Use asyncio timeouts and cancellation-safe patterns; document clearly.

## Success Criteria

- Tests pass across base and “all” extras matrix.
- Clear, actionable logs for engine selection and fallbacks.
- Users can perform basic cache ops via CLI.
- Docs accurately reflect supported engines and provide guidance per workload.

