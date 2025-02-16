## SpecStory

## Untitled (16/02/2025, 16:49:50)

_**User**_

 Read @README.md to understand the project. Read @LOG.md to see what has been done. Read @TODO.md to see what you should do, and then: proceed with the TODO

---

_**Assistant**_

I'll help you proceed with the TODO list based on the project understanding from README.md, LOG.md, and TODO.md. Let me analyze the current state and plan the next steps.

Key Points from Analysis:
1. This is a flexible caching utility package providing unified interface for various backends
2. Currently at version 1.7.9 with critical issues to fix
3. Main decorators planned: `mcache`, `bcache`, `fcache`, `acache`, `ucache`
4. Most urgent issues are with CacheConfig and engine implementations

Critical Issues to Address First:
1. CacheEngine import failing in test_engines.py
2. CacheConfig initialization broken
3. Cache stats tracking not working
4. Cache maxsize enforcement issues

Let me start by examining the current state of the core files to determine the best next step.

---

_****_

<details>
            <summary>Listed directory src/twat_cache • **14** results</summary>
        
| Name |
|-------|
| 📄 `__version__.py` |
| 📄 `decorators.py` |
| 📄 `engines` |
| 📄 `__pycache__` |
| 📄 `py.typed` |
| 📄 `config.py` |
| 📄 `utils.py` |
| 📄 `cache.py` |
| 📄 `types` |
| 📄 `.DS_Store` |
| 📄 `type_defs.py` |
| 📄 `__init__.py` |
| 📄 `paths.py` |
| 📄 `__main__.py` |

</details>

---

_****_



First, let's check the current state of the CacheConfig implementation since that's a critical issue:

---

_****_

Read file: src/twat_cache/config.py

---

_****_



I see the issue - the current CacheConfig is using dataclasses but according to the TODO and LOG, it should be using Pydantic. Let's fix this first. I'll update the config.py file to use Pydantic with proper field validation:

---

_****_

```diff
  # dependencies = [
  #   "loguru",
+ #   "pydantic",
  # ]
  # ///
  """Simple configuration for twat_cache."""
  
- from dataclasses import dataclass
- from typing import Any
- from collections.abc import Callable
- 
- 
- @dataclass
- class CacheConfig:
-     """Basic cache configuration."""
+ from typing import Any, Callable, Literal, Optional
+ from pydantic import BaseModel, Field, field_validator, model_validator
+ 
+ CacheType = Literal["memory", "disk", "file", "async"]
+ EvictionPolicy = Literal["lru", "lfu", "fifo", "rr", "ttl"]
+ 
+ 
+ class CacheConfig(BaseModel):
+     """Cache configuration using Pydantic for validation."""
  
-     maxsize: int | None = None
-     folder_name: str | None = None
-     preferred_engine: str | None = None
-     serializer: Callable[[Any], str] | None = None
-     use_sql: bool = False
-     cache_type: str | None = None
- 
-     def get_maxsize(self) -> int | None:
-         """Get the maxsize value."""
-         return self.maxsize
- 
-     def get_folder_name(self) -> str | None:
-         """Get the folder name."""
-         return self.folder_name
- 
-     def get_use_sql(self) -> bool:
-         """Get the use_sql value."""
-         return self.use_sql
- 
-     def get_preferred_engine(self) -> str | None:
-         """Get the preferred engine."""
-         return self.preferred_engine
- 
-     def get_cache_type(self) -> str | None:
-         """Get the cache type."""
-         return self.cache_type
- 
-     def validate(self) -> None:
-         """Validate the configuration."""
-         if self.maxsize is not None and self.maxsize <= 0:
-             msg = "maxsize must be positive or None"
-             raise ValueError(msg)
-         if self.folder_name is not None and not isinstance(self.folder_name, str):
-             msg = "folder_name must be a string or None"
-             raise ValueError(msg)
- 
-     def model_dump(self) -> dict[str, Any]:
-         """Convert the model to a dictionary."""
-         return {
-             "maxsize": self.maxsize,
-             "folder_name": self.folder_name,
-             "preferred_engine": self.preferred_engine,
-             "use_sql": self.use_sql,
-             "cache_type": self.cache_type,
-         }
- 
+     maxsize: Optional[int] = Field(
+         default=None, description="Maximum cache size (None for unlimited)", ge=1
+     )
+     folder_name: Optional[str] = Field(default=None, description="Cache directory name")
+     preferred_engine: Optional[str] = Field(
+         default=None, description="Preferred caching backend"
+     )
+     serializer: Optional[Callable[[Any], str]] = Field(
+         default=None, description="Function to serialize non-JSON-serializable objects"
+     )
+     use_sql: bool = Field(
+         default=False, description="Whether to use SQL-based disk cache"
+     )
+     cache_type: Optional[CacheType] = Field(
+         default=None, description="Type of cache to use"
+     )
+     ttl: Optional[float] = Field(
+         default=None, description="Time-to-live in seconds", ge=0
+     )
+     policy: EvictionPolicy = Field(default="lru", description="Cache eviction policy")
+     compress: bool = Field(default=False, description="Whether to compress cached data")
+     secure: bool = Field(
+         default=True,
+         description="Whether to use secure file permissions for disk cache",
+     )
+ 
+     model_config = {
+         "arbitrary_types_allowed": True,
+         "validate_assignment": True,
+         "extra": "forbid",
+     }
+ 
+     @field_validator("folder_name")
+     @classmethod
+     def validate_folder_name(cls, v: Optional[str]) -> Optional[str]:
+         """Validate folder name if provided."""
+         if v is not None and not isinstance(v, str):
+             raise ValueError("folder_name must be a string or None")
+         return v
+ 
+     @field_validator("preferred_engine")
      @classmethod
-     def from_dict(cls, data: dict[str, Any]) -> "CacheConfig":
-         """Create a config from a dictionary."""
-         return cls(**data)
+     def validate_preferred_engine(cls, v: Optional[str]) -> Optional[str]:
+         """Validate preferred engine if provided."""
+         valid_engines = {
+             "cachebox",
+             "cachetools",
+             "diskcache",
+             "joblib",
+             "klepto",
+             "functools",
+             "aiocache",
+         }
+         if v is not None and v not in valid_engines:
+             raise ValueError(f"preferred_engine must be one of {valid_engines}")
+         return v
+ 
+     @model_validator(mode="after")
+     def validate_ttl_policy(self) -> "CacheConfig":
+         """Validate TTL and policy compatibility."""
+         if self.ttl is not None and self.policy != "ttl":
+             self.policy = "ttl"
+         return self
  
  
  def create_cache_config(
-     maxsize: int | None = None,
-     folder_name: str | None = None,
-     preferred_engine: str | None = None,
-     serializer: Callable[[Any], str] | None = None,
+     maxsize: Optional[int] = None,
+     folder_name: Optional[str] = None,
+     preferred_engine: Optional[str] = None,
+     serializer: Optional[Callable[[Any], str]] = None,
      use_sql: bool = False,
-     cache_type: str | None = None,
-     cache_dir: str | None = None,  # For backward compatibility
+     cache_type: Optional[CacheType] = None,
+     ttl: Optional[float] = None,
+     policy: EvictionPolicy = "lru",
+     compress: bool = False,
+     secure: bool = True,
+     cache_dir: Optional[str] = None,  # For backward compatibility
  ) -> CacheConfig:
      """
-     Create a cache configuration.
+     Create a validated cache configuration.
  
      Args:
          maxsize: Maximum cache size (None for unlimited)
          folder_name: Cache directory name
-         preferred_engine: Preferred caching backend ('memory', 'disk', or 'file')
-         serializer: Optional function to serialize non-JSON-serializable objects
+         preferred_engine: Preferred caching backend
+         serializer: Function to serialize non-JSON-serializable objects
          use_sql: Whether to use SQL-based disk cache
          cache_type: Type of cache to use
+         ttl: Time-to-live in seconds
+         policy: Cache eviction policy
+         compress: Whether to compress cached data
+         secure: Whether to use secure file permissions
          cache_dir: Alias for folder_name (for backward compatibility)
  
      Returns:
-         A validated cache configuration
+         A validated CacheConfig instance
      """
      # Handle backward compatibility
      if cache_dir is not None:
          folder_name = cache_dir
  
-     config = CacheConfig(
+     return CacheConfig(
          maxsize=maxsize,
          folder_name=folder_name,
          use_sql=use_sql,
          cache_type=cache_type,
+         ttl=ttl,
+         policy=policy,
+         compress=compress,
+         secure=secure,
      )
-     config.validate()
-     return config
  
```

---

_****_



Now that we've updated the CacheConfig to use Pydantic with proper validation, let's check the base cache engine implementation since that's another critical issue:

---

_****_

Read file: src/twat_cache/engines/base.py

---

_****_



I see several issues in the base engine implementation that need to be fixed:

1. The import of CacheConfig from type_defs.py is incorrect - we just moved it to config.py
2. The concrete CacheEngine implementation is incomplete
3. The key generation could be improved

Let me fix these issues:

---



---

