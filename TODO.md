---
this_file: TODO.md
---

# twat_cache TODO List

## Core Goals

1. Provide simple, easy-to-use caching decorators with seamless fallback:
   - `mcache`: Memory-based caching using fastest available backend (with fallback to functools)
     - Primary: cachetools.LRUCache
     - Fallback: functools.lru_cache
   - `bcache`: Basic disk caching using diskcache (with fallback to memory)
     - Primary: diskcache.Cache
     - Fallback: mcache
   - `fcache`: Fast file-based caching using joblib (with fallback to memory)
     - Primary: joblib.Memory
     - Fallback: mcache
   - `ucache`: Universal caching that automatically selects best available backend
     - Ordered preference: cachebox > klepto > diskcache > joblib > cachetools > functools
     - Async support via aiocache when explicitly requested

2. Minimize code complexity:
   - Let 3rd party packages do the heavy lifting
   - Don't reinvent caching mechanisms
   - Provide simple passthrough to underlying functionality
   - Focus on ease of use over feature completeness

3. Implement seamless fallback:
   - If preferred backend isn't available, fall back gracefully
   - Use simple warning logs to inform about fallbacks
   - Always have functools.lru_cache as final fallback

4. Keep it simple:
   - Remove complex abstraction layers
   - Minimize our own code
   - Provide direct access to underlying cache objects
   - Use simple kwargs for configuration

5. Analyze and ingest the project @README.md that details the current state, and ingest @VARIA.md that details some observations. 

6. Then analyze the existing codebase, and review the previous Implementation Tasks below. 

7. TASK: Adjust the plan below, write a DETAILED PLAN including sketching out new code structures. Write snippets and pseudocode for the core functionality. 

## Implementation Tasks

### Phase 1: Core Functionality

* **1.1. Simplify Decorators:**
  - [x] Implement `mcache` using functools.lru_cache
  - [x] Implement `bcache` using diskcache with fallback
  - [x] Implement `fcache` using joblib with fallback
  - [x] Implement `ucache` with smart backend selection
  - [ ] Add explicit backend selection to `ucache`
  - [ ] Add async support via aiocache

* **1.2. Streamline Backend Integration:**
  - [x] Remove complex abstraction layers
  - [x] Implement simple fallback mechanism
  - [x] Add basic logging for fallbacks
  - [x] Provide direct access to cache objects
  - [ ] Implement consistent API across all backends
  - [ ] Add backend-specific optimizations

* **1.3. Fix Configuration:**
  - [x] Remove complex config system
  - [x] Use simple kwargs for options
  - [x] Add basic path validation
  - [x] Implement minimal error handling
  - [ ] Add backend-specific config options
  - [ ] Implement config validation per backend

* **1.4. Cleanup:**
  - [ ] Remove unused code:
    - [ ] Remove engine abstraction layer
    - [ ] Remove complex configuration
    - [ ] Remove stats tracking
  - [ ] Fix remaining linting errors
  - [ ] Update documentation
  - [ ] Update dependencies

### Phase 2: Testing and Documentation

* **2.1. Improve Test Suite:**
  - [x] Simplify test cases
  - [x] Add fallback tests
  - [x] Remove complex test scenarios
  - [x] Focus on core functionality
  - [ ] Add backend-specific tests
  - [ ] Test async functionality
  - [ ] Test explicit backend selection

* **2.2. Update Documentation:**
  - [ ] Add clear usage examples
  - [ ] Document fallback behavior
  - [ ] Remove complex configuration docs
  - [ ] Update installation guide
  - [ ] Document backend selection
  - [ ] Add async usage examples

### Phase 3: Polish and Release

* **3.1. Final Touches:**
  - [ ] Clean up dependencies
  - [ ] Verify type hints
  - [ ] Add proper error messages
  - [ ] Update package metadata
  - [ ] Optimize imports
  - [ ] Add performance benchmarks

* **3.2. Release Preparation:**
  - [ ] Run final test suite
  - [ ] Update version numbers
  - [ ] Prepare release notes
  - [ ] Publish to PyPI

## Development Notes

Remember to run:
```bash
uv venv; source .venv/bin/activate; uv pip install -e .[all,dev,test]; hatch run lint:fix; hatch test;
```

## Implementation Guidelines

1. Keep It Simple:
   - Use direct backend calls
   - Minimize abstraction layers
   - Focus on ease of use

2. Focus on User Experience:
   - Make decorators intuitive
   - Provide sensible defaults
   - Keep configuration minimal

3. Efficient Fallbacks:
   - Try preferred backend first
   - Fall back gracefully with warning
   - Always have functools.lru_cache as backup

4. Backend Selection:
   - Allow explicit backend choice in `ucache`
   - Provide optimized defaults per use case
   - Support async when needed

5. Performance Considerations:
   - Use fastest available backend
   - Minimize serialization overhead
   - Provide direct cache access

