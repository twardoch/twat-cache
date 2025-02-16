## SpecStory

## Untitled (16/02/2025, 06:57:40)

_**User**_

Read @T@TODO.md ODO.md from 2.1.4. onwards. Rewrite that section, mark what's done, update @LOG.md 

As you develop, run 

```
uv venv; source .venv/bin/activate; uv pip install -e .[all,dev,test]; hatch run lint:fix; hatch test;
```

then continue on what's still TODO


---

_**Assistant**_

Let me help you update the TODO list and LOG based on the current state. First, I'll check the project status.

---

_****_

```bash
uv venv; source .venv/bin/activate; uv pip install -e .[all,dev,test]; hatch run lint:fix; hatch test
```

```
Using CPython 3.12.8 interpreter at: /usr/local/bin/python3.12
Creating virtual environment at: .venv
Activate with: source .venv/bin/activate
zsh: no matches found: .[all,dev,test]
warning: The top-level linter settings are deprecated in favour of their c
ounterparts in the `lint` section. Please update the following options in `pypro
ject.toml`:                                                           - 'per-fil
e-ignores' -> 'lint.per-file-ignores'
src/twat_cache/config.py:165:26: PLR2004 Magic value used in comparison, c
onsider replacing `9` with a constant variable                                |
163 |     def validate_compression_level(self, v: int) -> int:
164 |         """Validate compression level."""
165 |         if not 1 <= v <= 9:
    |                          ^ PLR2004
166 |             msg = "compression_level must be between 1 and 9"
167 |             raise ValueError(msg)
    |

src/twat_cache/config.py:222:30: T201 `print` found
    |
220 |         level = "DEBUG" if self.debug else "INFO"
221 |         logger.add(
222 |             sink=lambda msg: print(msg, end=""),
    |                              ^^^^^ T201
223 |             level=level,
224 |             format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
    |
    = help: Remove `print`

src/twat_cache/decorators.py:19:5: FBT001 Boolean-typed positional argumen
t in function definition                                                     |
17 |     maxsize: int | None = None,
18 |     folder_name: str | None = None,
19 |     use_sql: bool = False,
   |     ^^^^^^^ FBT001
20 |     preferred_engine: str | None = None,
21 |     cache_type: str | None = None,
   |

src/twat_cache/decorators.py:19:5: FBT002 Boolean default positional argum
ent in function definition                                                   |
17 |     maxsize: int | None = None,
18 |     folder_name: str | None = None,
19 |     use_sql: bool = False,
   |     ^^^^^^^ FBT002
20 |     preferred_engine: str | None = None,
21 |     cache_type: str | None = None,
   |

src/twat_cache/engines/functools.py:1:1: A005 Module `functools` shadows a
 Python standard-library module                                           src/tw
at_cache/engines/joblib.py:49:33: ARG002 Unused method argument: `ke
y`                                                                           |
47 |         )
48 |
49 |     def _get_cached_value(self, key: CacheKey) -> R | None:
   |                                 ^^^ ARG002
50 |         """Retrieve a value from the cache.
   |

src/twat_cache/engines/klepto.py:20:34: ARG005 Unused lambda argument: `ar
gs`                                                                          |
18 |     HAS_KLEPTO = False
19 |     dir_archive = type("dir_archive", (), {})  # type: ignore
20 |     keymap = picklemap = lambda *args, **kwargs: lambda f: f  # type:
 ignore                                                                      |
                                ^^^^ ARG005
   |

src/twat_cache/engines/klepto.py:20:42: ARG005 Unused lambda argument: `kw
args`                                                                        |
18 |     HAS_KLEPTO = False
19 |     dir_archive = type("dir_archive", (), {})  # type: ignore
20 |     keymap = picklemap = lambda *args, **kwargs: lambda f: f  # type:
 ignore                                                                      |
                                        ^^^^^^ ARG005
   |

src/twat_cache/paths.py:100:5: C901 `clear_cache` is too complex (11 > 10)
    |
100 | def clear_cache(folder_name: str | None = None) -> None:
    |     ^^^^^^^^^^^ C901
101 |     """
102 |     Clear the cache directory for the given folder name.
    |

src/twat_cache/types.py:1:1: A005 Module `types` shadows a Python standard
-library module                                                           tests/
test_cache.py:20:7: F811 Redefinition of unused `CacheConfig` from l
ine 17                                                                       |
20 | class CacheConfig(TypedDict, total=False):
   |       ^^^^^^^^^^^ F811
21 |     """Type definition for cache configuration."""
   |
   = help: Remove definition: `CacheConfig`

tests/test_cache.py:185:34: PLR2004 Magic value used in comparison, consid
er replacing `15` with a constant variable                                    |
183 |     result2 = process_list(test_list)
184 |
185 |     assert result1 == result2 == 15
    |                                  ^^ PLR2004
    |

tests/test_config.py:114:38: PLR2004 Magic value used in comparison, consi
der replacing `500` with a constant variable                                  |
113 |     # Check values
114 |     assert config.default_maxsize == 500
    |                                      ^^^ PLR2004
115 |     assert config.default_use_sql is True
116 |     assert config.default_engine == "disk"
    |

tests/test_config.py:135:36: PLR2004 Magic value used in comparison, consi
der replacing `200` with a constant variable                                  |
133 |         folder_name="test_cache",
134 |     )
135 |     assert cache_config.maxsize == 200
    |                                    ^^^ PLR2004
136 |     assert cache_config.folder_name == "test_cache"
137 |     assert cache_config.use_sql == global_config.default_use_sql
    |

tests/test_config.py:147:36: PLR2004 Magic value used in comparison, consi
der replacing `300` with a constant variable                                  |
145 |         preferred_engine="disk",
146 |     )
147 |     assert cache_config.maxsize == 300
    |                                    ^^^ PLR2004
148 |     assert cache_config.folder_name == "custom_cache"
149 |     assert cache_config.use_sql is True
    |

tests/test_engines.py:145:28: PLR2004 Magic value used in comparison, cons
ider replacing `10` with a constant variable                                  |
144 |     # First call should compute
145 |     assert test_func(5) == 10
    |                            ^^ PLR2004
146 |     assert call_count == 1
147 |     assert test_engine.stats["hits"] == 0
    |

tests/test_engines.py:151:28: PLR2004 Magic value used in comparison, cons
ider replacing `10` with a constant variable                                  |
150 |     # Second call should use cache
151 |     assert test_func(5) == 10
    |                            ^^ PLR2004
152 |     assert call_count == 1
153 |     assert test_engine.stats["hits"] == 1
    |

tests/test_engines.py:157:29: PLR2004 Magic value used in comparison, cons
ider replacing `20` with a constant variable                                  |
156 |     # Different arg should compute
157 |     assert test_func(10) == 20
    |                             ^^ PLR2004
158 |     assert call_count == 2
159 |     assert test_engine.stats["hits"] == 1
    |

tests/test_engines.py:158:26: PLR2004 Magic value used in comparison, cons
ider replacing `2` with a constant variable                                   |
156 |     # Different arg should compute
157 |     assert test_func(10) == 20
158 |     assert call_count == 2
    |                          ^ PLR2004
159 |     assert test_engine.stats["hits"] == 1
160 |     assert test_engine.stats["misses"] == 2
    |

tests/test_engines.py:160:43: PLR2004 Magic value used in comparison, cons
ider replacing `2` with a constant variable                                   |
158 |     assert call_count == 2
159 |     assert test_engine.stats["hits"] == 1
160 |     assert test_engine.stats["misses"] == 2
    |                                           ^ PLR2004
    |

tests/test_engines.py:190:38: PLR2004 Magic value used in comparison, cons
ider replacing `10` with a constant variable                                  |
188 |         lru_engine._set_cached_value(("key", i), i)
189 |
190 |     assert len(lru_engine._cache) == 10
    |                                      ^^ PLR2004
191 |
192 |     # Add one more, should evict oldest
    |

tests/test_engines.py:194:38: PLR2004 Magic value used in comparison, cons
ider replacing `10` with a constant variable                                  |
192 |     # Add one more, should evict oldest
193 |     lru_engine._set_cached_value(("key", 10), 10)
194 |     assert len(lru_engine._cache) == 10
    |                                      ^^ PLR2004
195 |     assert ("key", 0) not in lru_engine._cache  # First item should 
be evicted                                                                196 |
    assert ("key", 10) in lru_engine._cache  # New item should be pr
esent                                                                         |

tests/test_engines.py:205:38: PLR2004 Magic value used in comparison, cons
ider replacing `5` with a constant variable                                   |
203 |         lru_engine._set_cached_value(("key", i), i)
204 |
205 |     assert len(lru_engine._cache) == 5
    |                                      ^ PLR2004
206 |
207 |     # Clear cache
    |

tests/test_engines.py:248:29: PLR2004 Magic value used in comparison, cons
ider replacing `2` with a constant variable                                   |
247 |     stats = lru_engine.stats
248 |     assert stats["hits"] == 2
    |                             ^ PLR2004
249 |     assert stats["misses"] == 2
250 |     assert stats["size"] == 2
    |

tests/test_engines.py:249:31: PLR2004 Magic value used in comparison, cons
ider replacing `2` with a constant variable                                   |
247 |     stats = lru_engine.stats
248 |     assert stats["hits"] == 2
249 |     assert stats["misses"] == 2
    |                               ^ PLR2004
250 |     assert stats["size"] == 2
251 |     assert stats["current_size"] == 2
    |

tests/test_engines.py:250:29: PLR2004 Magic value used in comparison, cons
ider replacing `2` with a constant variable                                   |
248 |     assert stats["hits"] == 2
249 |     assert stats["misses"] == 2
250 |     assert stats["size"] == 2
    |                             ^ PLR2004
251 |     assert stats["current_size"] == 2
    |

tests/test_engines.py:251:37: PLR2004 Magic value used in comparison, cons
ider replacing `2` with a constant variable                                   |
249 |     assert stats["misses"] == 2
250 |     assert stats["size"] == 2
251 |     assert stats["current_size"] == 2
    |                                     ^ PLR2004
    |

Found 37 errors (10 fixed, 27 remaining).
========================== test session starts ===========================
platform darwin -- Python 3.12.8, pytest-8.3.4, pluggy-1.5.0 -- /Users/ada
m/Library/Application Support/hatch/env/virtual/twat-cache/ivvP1xkE/hatch-test.p
y3.12/bin/python3                                                   cachedir: .p
ytest_cache
rootdir: /Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good
/twat/plugins/repos/twat_cache                                            config
file: pyproject.toml
plugins: rerunfailures-14.0, mock-3.14.0, xdist-3.6.1
collected 0 items / 4 errors                                             

================================= ERRORS =================================
__________________ ERROR collecting tests/test_cache.py __________________
tests/test_cache.py:15: in <module>
    from twat_cache.cache import clear_cache, get_stats
src/twat_cache/__init__.py:5: in <module>
    from twat_cache.cache import clear_cache, get_stats
src/twat_cache/cache.py:20: in <module>
    from .config import CacheConfig
src/twat_cache/config.py:32: in <module>
    class CacheConfig(BaseModel, CacheConfigBase):
src/twat_cache/config.py:67: in CacheConfig
    @field_validator("maxsize")
/Users/adam/Library/Application Support/hatch/env/virtual/twat-cache/ivvP1
xkE/hatch-test.py3.12/lib/python3.12/site-packages/pydantic/functional_validator
s.py:501: in dec                                                        raise Py
danticUserError(
E   pydantic.errors.PydanticUserError: `@field_validator` cannot be applie
d to instance methods                                                     E   
E   For further information visit https://errors.pydantic.dev/2.10/u/valid
ator-instance-method                                                      ______
___________ ERROR collecting tests/test_config.py __________________
tests/test_config.py:19: in <module>
    from twat_cache.config import CacheConfig, GlobalConfig
src/twat_cache/__init__.py:5: in <module>
    from twat_cache.cache import clear_cache, get_stats
src/twat_cache/cache.py:20: in <module>
    from .config import CacheConfig
src/twat_cache/config.py:32: in <module>
    class CacheConfig(BaseModel, CacheConfigBase):
src/twat_cache/config.py:67: in CacheConfig
    @field_validator("maxsize")
/Users/adam/Library/Application Support/hatch/env/virtual/twat-cache/ivvP1
xkE/hatch-test.py3.12/lib/python3.12/site-packages/pydantic/functional_validator
s.py:501: in dec                                                        raise Py
danticUserError(
E   pydantic.errors.PydanticUserError: `@field_validator` cannot be applie
d to instance methods                                                     E   
E   For further information visit https://errors.pydantic.dev/2.10/u/valid
ator-instance-method                                                      ______
___________ ERROR collecting tests/test_engines.py _________________
tests/test_engines.py:24: in <module>
    from twat_cache.engines.base import BaseCacheEngine
src/twat_cache/__init__.py:5: in <module>
    from twat_cache.cache import clear_cache, get_stats
src/twat_cache/cache.py:20: in <module>
    from .config import CacheConfig
src/twat_cache/config.py:32: in <module>
    class CacheConfig(BaseModel, CacheConfigBase):
src/twat_cache/config.py:67: in CacheConfig
    @field_validator("maxsize")
/Users/adam/Library/Application Support/hatch/env/virtual/twat-cache/ivvP1
xkE/hatch-test.py3.12/lib/python3.12/site-packages/pydantic/functional_validator
s.py:501: in dec                                                        raise Py
danticUserError(
E   pydantic.errors.PydanticUserError: `@field_validator` cannot be applie
d to instance methods                                                     E   
E   For further information visit https://errors.pydantic.dev/2.10/u/valid
ator-instance-method                                                      ______
_________ ERROR collecting tests/test_twat_cache.py ________________
tests/test_twat_cache.py:20: in <module>
    from twat_cache.engines.functools import FunctoolsCacheEngine
src/twat_cache/__init__.py:5: in <module>
    from twat_cache.cache import clear_cache, get_stats
src/twat_cache/cache.py:20: in <module>
    from .config import CacheConfig
src/twat_cache/config.py:32: in <module>
    class CacheConfig(BaseModel, CacheConfigBase):
src/twat_cache/config.py:67: in CacheConfig
    @field_validator("maxsize")
/Users/adam/Library/Application Support/hatch/env/virtual/twat-cache/ivvP1
xkE/hatch-test.py3.12/lib/python3.12/site-packages/pydantic/functional_validator
s.py:501: in dec                                                        raise Py
danticUserError(
E   pydantic.errors.PydanticUserError: `@field_validator` cannot be applie
d to instance methods                                                     E   
E   For further information visit https://errors.pydantic.dev/2.10/u/valid
ator-instance-method                                                      ======
================== short test summary info =========================
ERROR tests/test_cache.py - pydantic.errors.PydanticUserError: `@field_val
idator` cannot be appli...                                                ERROR
tests/test_config.py - pydantic.errors.PydanticUserError: `@field_va
lidator` cannot be appli...                                               ERROR
tests/test_engines.py - pydantic.errors.PydanticUserError: `@field_v
alidator` cannot be appli...                                              ERROR
tests/test_twat_cache.py - pydantic.errors.PydanticUserError: `@fiel
d_validator` cannot be appli...                                           !!!!!!
!!!!!!!!!! Interrupted: 4 errors during collection !!!!!!!!!!!!!!!!!
=========================== 4 errors in 0.37s ============================

```

---

_****_



I see there are some issues with the tests and linting that need to be addressed. Let me first update the TODO.md and LOG.md with the current status and then we can work on fixing these issues.

---

_****_



---

_****_



---



---

