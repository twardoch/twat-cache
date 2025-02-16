---
this_file: TODO.md
---

# twat_cache TODO List

## Core Goals

1. Provide simple, easy-to-use caching decorators:
   - `mcache`: Memory-based caching (using FASTEST available backend but allowing fallback)

   - `bcache`: database caching (using MOST SUITABLE backend)
   - `fcache`: Persistent filesystem cachine using joblib, allowing fallback — the point being that it should be easy to actually access the cached files
   - `ucache`: Universal caching with automatic fallback

2. Minimize our own code:
   - Let 3rd party packages do the heavy lifting
   - Don't reinvent caching mechanisms
   - Provide simple passthrough to underlying functionality
   - Focus on ease of use over feature completeness

3. Implement seamless fallback:
   - If preferred backend isn't available, fall back gracefully
   - Use simple warning logs to inform about fallbacks
   - Always have functools.lru_cache as final fallback

4. Analyze and ingest the project @README.md that details the current state, and ingest @VARIA.md that details some observations. 

5. Then analyze the existing codebase, and review the previous Implementation Tasks below. 

6. TASK: Adjust the plan below, write a DETAILED PLAN including sketching out new code structures. Write snippets and pseudocode for the core functionality. 

## Implementation Tasks

### Phase 1: Core Functionality

* **1.1. Simplify Decorators:**
  - [ ] Implement `mcache` 
  - [ ] Implement `bcache` 
  - [ ] Implement `fcache` 
  - [ ] Implement `ucache` 

* **1.2. Streamline Backend Integration:**
  - [ ] Remove complex abstraction layers
  - [ ] Simplify backend detection
  - [ ] Implement basic logging for fallbacks
  - [ ] Add simple passthrough to backend features

* **1.3. Fix Configuration:**
  - [ ] Remove complex config system
  - [ ] Use simple kwargs for decorator options
  - [ ] Add basic path management for disk caches
  - [ ] Implement minimal validation

### Phase 2: Testing and Documentation

* **2.1. Improve Test Suite:**
  - [ ] Add basic decorator tests
  - [ ] Test fallback mechanisms
  - [ ] Verify backend detection
  - [ ] Add simple performance tests

* **2.2. Update Documentation:**
  - [ ] Add clear usage examples
  - [ ] Document fallback behavior
  - [ ] Add backend-specific notes
  - [ ] Update installation guide

### Phase 3: Polish and Release

* **3.1. Final Touches:**
  - [ ] Clean up dependencies
  - [ ] Verify type hints
  - [ ] Add proper error messages
  - [ ] Update package metadata

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
   - Minimize abstraction layers
   - Use direct backend calls where possible
   - Don't try to normalize all backends

2. Focus on User Experience:
   - Make decorators intuitive to use
   - Provide sensible defaults
   - Keep configuration minimal

3. Efficient Fallbacks:
   - Try preferred backend first
   - Fall back gracefully with warning
   - Always have functools.lru_cache as backup

