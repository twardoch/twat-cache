---
# this_file: src_docs/user-guide/caching-strategies.md
title: Caching Strategies — TWAT-Cache
description: When to use each caching strategy and which decorator or backend to reach for
---

# Caching Strategies

TWAT-Cache ships five decorators backed by several storage engines. This page
explains **what each strategy is**, **what it costs**, and **when to prefer
it**. Pick based on your data, not your instinct.

---

## Quick Decision Table

| I need … | Use |
|---|---|
| Fast, temporary in-memory results | `ucache()` or `mcache()` |
| Results that survive process restart | `bcache()` |
| NumPy arrays or large objects | `fcache()` |
| Results from async coroutines | `acache()` |
| One decorator, auto-picked backend | `ucache()` |

---

## Strategy 1 — `ucache` (Universal, recommended default)

```python
from twat_cache import ucache

@ucache(maxsize=256, ttl=300)
def get_user(user_id: int) -> dict:
    return db.fetch_user(user_id)
```

**What it does.**  
Selects the fastest available in-memory backend at decoration time:
`cachebox` (Rust) › `cachetools` › `functools`.  When `folder_name` is set,
the config accepts it but still picks a memory backend unless you choose an
explicit `preferred_engine`.

**When to use it.**  
The right answer for the vast majority of cases.  If you are unsure, start
here and only switch to a specialised decorator once you hit a concrete limit.

**Limits.**  
- In-memory only by default — results are lost on process exit.  
- Arguments must be hashable (tuples, strings, numbers).  Lists cause a
  `TypeError` at key-computation time; `ucache` catches it and falls back to
  a direct call rather than crashing.  
- Exceptions are **not** cached — a failing call never stores an entry, so
  the function is invoked again on the next call with the same arguments.

**Key options.**

| Parameter | Effect |
|---|---|
| `maxsize` | Maximum number of entries (LRU eviction when full) |
| `ttl` | Seconds before an entry expires (`None` = forever) |
| `policy` | `"lru"` (default), `"lfu"`, `"rr"` |
| `preferred_engine` | Force a specific backend by name |
| `secure` | Use secure key generation for edge-case types |

---

## Strategy 2 — `bcache` (Disk, persistent)

```python
from twat_cache.decorators import bcache

@bcache(folder_name="user_cache", ttl=3600)
def expensive_report(report_id: str) -> dict:
    return analytics.run(report_id)
```

**What it does.**  
Stores results on disk via `diskcache` (SQLite-backed) with an optional
`klepto` fallback.  Data persists across process restarts and can be shared
between multiple workers pointing at the same directory.

**When to use it.**  
- Results take seconds or minutes to compute and you want them to survive
  a restart or deployment.  
- You are running multiple processes (worker pool, multi-process server) and
  want a shared result layer.  
- CI pipelines where identical work is repeated across runs.

**Limits.**  
- Slower than memory for hot paths (SQLite I/O).  
- Values must be picklable.  
- The `size_limit` in `diskcache` is expressed in **bytes** (not item count);
  the library default (1 GB) is used unless you configure it explicitly through
  `create_cache_config`.

---

## Strategy 3 — `fcache` (File / Joblib, large objects)

```python
from twat_cache.decorators import fcache

@fcache(folder_name="model_cache", compress=True)
def load_embeddings(model_name: str):
    return model.encode_all(texts)
```

**What it does.**  
Uses `joblib`'s memory-mapped file cache for efficient serialisation of large
objects like NumPy arrays, pandas DataFrames, and scikit-learn models.  Falls
back to `klepto` if `joblib` is absent.

**When to use it.**  
- The function returns large numerical arrays or DataFrames.  
- You want compression without writing custom pickling logic.  
- You are building a machine-learning pipeline with expensive feature
  extraction.

**Limits.**  
- Requires `joblib` (`pip install twat-cache[joblib]`).  
- Objects must be picklable/serialisable by joblib.  
- Disk-bound; not suitable for sub-millisecond hot paths.

---

## Strategy 4 — `acache` (Async)

```python
from twat_cache import acache

@acache(maxsize=128, ttl=60)
async def fetch_weather(city: str) -> dict:
    async with httpx.AsyncClient() as client:
        r = await client.get(f"https://api.weather.example/{city}")
        return r.json()
```

**What it does.**  
Wraps `async def` functions.  When `aiocache` is installed it delegates to
that library for native async-safe caching.  Without `aiocache`, a
thread-safe dict-based fallback is used that caches **awaited results** (not
coroutine objects), so cache hits never replay a coroutine.

**When to use it.**  
Any time you are caching an `async def` function.  Using `ucache` on a
coroutine wraps it synchronously and loses async benefits.

**Concurrent-request deduplication.**  
`acache` with the fallback backend cannot deduplicate *concurrent* requests
for the same key (two coroutines already in-flight both compute and store).
Install `aiocache` for proper async-safe deduplication:

```
pip install twat-cache[aiocache]
```

**Limits.**  
- Without `aiocache`, concurrent calls for the same key are *not*
  deduplicated (though the result is still cached after the first completes).  
- Arguments must be hashable.

---

## Strategy 5 — `mcache` (Memory, explicit control)

```python
from twat_cache.decorators import mcache

@mcache(maxsize=512, policy="lfu")
def score(text: str) -> float:
    return nlp_model.predict(text)
```

**What it does.**  
Same as `ucache` but with explicit backend priority: `cachebox` › `cachetools`
› `functools`.  Exposes `policy` choices directly without the auto-detection
overhead of `ucache`.

**When to use it.**  
When you want a named memory strategy (`lru`, `lfu`, `rr`) and you do not
need the universal fallback logic of `ucache`.

---

## Choosing a TTL

| Data changes | Recommended TTL |
|---|---|
| Never (config, enums) | `None` (no expiry) |
| Minutes (weather, prices) | `60`–`300` |
| Hours (user profiles) | `3600` |
| Days (static reports) | `86400` |
| Per request (per-session) | Short TTL + `maxsize` eviction |

TTL is measured in **seconds** across all decorators.  Set `ttl=None` (the
default) to cache indefinitely until eviction by `maxsize`.

---

## Choosing a `maxsize`

`maxsize` limits the number of **entries** (not bytes) in memory caches.
When the limit is reached, the oldest/least-used entry is evicted according
to `policy`.

- `None` — unbounded; suitable only when the key space is finite and small.
- `128`–`1024` — typical web handler or CLI tool.
- Larger values trade memory for fewer recomputes; profile before tuning.

---

## Eviction Policies

| `policy` | Algorithm | Best for |
|---|---|---|
| `"lru"` | Least Recently Used (default) | General; temporal locality |
| `"lfu"` | Least Frequently Used | Hot keys change slowly |
| `"rr"` | Random Replacement | Low overhead, unpredictable access |

Only `cachetools` and `cachebox` backends support all three policies.
`functools` always uses LRU regardless of the `policy` setting.

---

## Backend Availability Summary

| Backend | Package | Memory | Disk | Async | Notes |
|---|---|---|---|---|---|
| `functools` | stdlib | ✓ | — | — | Always available; LRU only |
| `cachetools` | `cachetools` | ✓ | — | — | LRU / LFU / RR |
| `cachebox` | `cachebox` | ✓ | — | — | Fastest (Rust) |
| `diskcache` | `diskcache` | — | ✓ | — | SQLite-backed |
| `joblib` | `joblib` | — | ✓ | — | Optimised for arrays |
| `klepto` | `klepto` | ✓ | ✓ | — | SQL or file |
| `aiocache` | `aiocache` | ✓ | — | ✓ | Native async |

Install optional backends:

```bash
pip install twat-cache[diskcache,cachetools,joblib,aiocache]
```
