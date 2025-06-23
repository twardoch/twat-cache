# this_file: tests/test_constants.py
"""Constants used in test files to avoid magic numbers."""

# Cache sizes
SMALL_CACHE_SIZE = 10
DEFAULT_CACHE_SIZE = 100
LARGE_CACHE_SIZE = 1000
CACHE_SIZE = DEFAULT_CACHE_SIZE # Alias for common use

# TTL values (in seconds)
SHORT_TTL = 0.1
DEFAULT_TTL = 60 # Keeping this one as 60s, as 3600 might be too long for many tests
LONG_TTL = 3600
CACHE_TTL = DEFAULT_TTL # Alias for tests expecting CACHE_TTL

# Test values
TEST_KEY = "test_key" # From second block
TEST_VALUE = 42       # From second block
TEST_RESULT = 84      # From second block (TEST_VALUE * 2)

SQUARE_INPUT = 5 # Used in test_cache.py, keeping from first block's TEST_VALUE for this
SQUARE_RESULT = SQUARE_INPUT * SQUARE_INPUT # Used in test_cache.py

# File permissions
DIR_PERMISSIONS = 0o700
FILE_PERMISSIONS = 0o600
TEST_PERMISSIONS = 0o700 # From first block, seems same as DIR_PERMISSIONS

# Compression levels
MIN_COMPRESSION = 0
DEFAULT_COMPRESSION = 6
MAX_COMPRESSION = 9
NO_COMPRESSION = 0 # Same as MIN_COMPRESSION

# Cache stats
INITIAL_HITS = 0
INITIAL_MISSES = 0
INITIAL_SIZE = 0 # From second block

# Test data sizes (using the KB/MB style from the first block for clarity if no conflict)
SMALL_DATA_SIZE = 1024  # 1KB
DEFAULT_DATA_SIZE = 1024 * 1024  # 1MB
LARGE_DATA_SIZE = 10 * 1024 * 1024  # 10MB
MEDIUM_DATA_SIZE = 100000 # From second block if different scale needed

# Timeouts
SHORT_TIMEOUT = 0.1
DEFAULT_TIMEOUT = 1.0
LONG_TIMEOUT = 5.0

# File paths
TEST_FOLDER = "test_cache" # From first block
TEST_FILE = "test_data.cache" # From first block
TEST_DB = "test_cache.db" # From first block

TEST_CACHE_DIR = "test_cache" # From second block (same as TEST_FOLDER)
TEST_DB_FILE = "test.db" # From second block (seems more generic than TEST_DB)
TEST_ARRAY_FILE = "test_array.npy" # From second block

# Test data
TEST_LIST = [1, 2, 3, 4, 5] # Same in both
TEST_LIST_SUM = 15          # Same in both

TEST_BOOL = True    # From both
TEST_INT = 123      # From both

# Call counts
TEST_CALL_COUNT = 2 # From first block
EXPECTED_CALLS_SINGLE = 1
EXPECTED_CALLS_DOUBLE = 2
EXPECTED_CALLS_TRIPLE = 3
EXPECTED_CALLS_QUAD = 4 # From second block

# For test_cache.py that uses these specific constants
# These were not in the original test_constants.py but were defined locally in test_cache.py
TEST_INPUT = 5
TEST_INPUT_2 = 6
EXPECTED_CALL_COUNT_CACHE_TEST = 2 # Renamed from EXPECTED_CALL_COUNT to avoid clash
MIN_STATS_COUNT = 2
TTL_DURATION = 0.5
