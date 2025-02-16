Some caching solutions for Python are simple and fail when trying to serialize a more complex Python object. 

What are Python libraries that allow very robust serialization and deserialization, so that upon failure, I could call the extra serialization and try to cache that?


----



For robust serialization and deserialization of complex Python objects for caching, you can consider the following Python libraries. These libraries offer different levels of robustness and handle various types of complex objects effectively.

*   **Pickle:** This is Python's built-in serialization library and is often a good starting point due to its simplicity and ability to handle a wide range of Python objects.

    *   **Robustness:** Pickle can serialize most Python data types, including custom classes, functions, and even code. It is designed to handle complex object relationships, including circular references and deep nesting.
    *   **Use Case:**  It's suitable for general Python object serialization and is often used in caching scenarios. You can try Pickle as your initial, simpler serialization method.
    *   **Fallback:** If Pickle fails (though it's quite robust within Python), you can consider more specialized libraries.
    *   **Reference:**  [Serialize Your Data With Python - Real Python](https://realpython.com/python-serialize-data/)

*   **Dill:**  The `dill` library expands upon `pickle` to serialize a wider range of Python objects, including those that `pickle` might fail to handle, such as lambda expressions and interactively defined classes.

    *   **Robustness:** `dill` is designed to be more robust than `pickle` for complex and unconventional Python objects. It aims to serialize almost anything in Python.
    *   **Use Case:** If you encounter issues with `pickle` when serializing very complex objects (e.g., objects with intricate dependencies, closures, or objects defined in interactive sessions), `dill` is an excellent fallback. It's essentially a drop-in replacement for `pickle`.
    *   **Fallback:** `dill` is often considered one of the most robust Python serialization libraries. If `dill` fails, it might indicate a truly exceptional case or a fundamental limitation in serialization itself for the object in question.
    *   **Reference:** [Serialize Your Data With Python - Real Python](https://realpython.com/python-serialize-data/) (mentions `dill` as a more robust alternative to `pickle`)

*   **Marshmallow:** While primarily a data validation and schema library, Marshmallow also provides robust serialization and deserialization capabilities, particularly for complex data structures and custom objects.

    *   **Robustness:** Marshmallow uses schemas to define the structure of your data, which can make serialization and deserialization more predictable and less error-prone, especially when dealing with complex, nested data. It also handles data validation, ensuring data integrity.
    *   **Use Case:** If your caching involves structured data that needs validation or if you want a schema-based approach to serialization, Marshmallow is a strong option. It might be more overhead than `pickle` or `dill` for simple caching, but it adds robustness through structure definition and validation.
    *   **Fallback:** If you need even more control over the serialization process or need to handle very specific data formats, you might explore lower-level serialization libraries or custom serialization logic after trying Marshmallow.
    *   **Reference:** [MarshMallow: The Sweetest Python Library for Data Serialization and Validation - KDnuggets](https://www.kdnuggets.com/marshmallow-the-sweetest-python-library-for-data-serialization-and-validation)

**Simplified Approach for Caching with Fallback:**

1.  **Initial Simple Serialization (e.g., `pickle`):**  Attempt to serialize your Python object using `pickle.dumps()`. This is generally fast and works for many common objects.
2.  **Cache Attempt with Simple Serialization:** Try to cache the pickled object.
3.  **Deserialization and Failure Handling:** When retrieving from the cache, attempt `pickle.loads()`. If this fails (e.g., `pickle.PicklingError` or `pickle.UnpicklingError`), it indicates a problem with the simple serialization for this specific object type in your context.
4.  **Robust Fallback Serialization (e.g., `dill`):** In the failure scenario, implement a fallback mechanism using `dill.dumps()` to serialize the object.
5.  **Cache with Robust Serialization:**  Cache the dill-serialized object.
6.  **Robust Deserialization:**  When retrieving a dill-serialized object from the cache, use `dill.loads()`.

**Example (Conceptual):**

```python
import pickle
import dill
import cachelib  # Example caching library

cache = cachelib.SimpleCache() # Or your preferred caching solution

def robust_cache_set(key, obj):
    try:
        serialized_obj = pickle.dumps(obj)
        cache.set(key, serialized_obj)
    except pickle.PicklingError: # Or exceptions you observe with simple serialization
        serialized_obj = dill.dumps(obj)
        cache.set(key, serialized_obj, serialize=False) # Assuming cachelib allows bypassing its default serializer

def robust_cache_get(key):
    cached_data = cache.get(key)
    if cached_data:
        try:
            return pickle.loads(cached_data) # Attempt simple deserialization first
        except pickle.PicklingError: # Or related exceptions
            return dill.loads(cached_data) # Fallback to robust deserialization
    return None # Or handle cache miss

# Example Usage
complex_object = ... # Your complex Python object

robust_cache_set('my_complex_object', complex_object)
retrieved_object = robust_cache_get('my_complex_object')

```

**Note:**

*   The `cachelib` example is illustrative. Adapt the caching and serialization/deserialization logic to your specific caching library. Some caching libraries might have built-in serialization mechanisms or allow you to configure custom serializers.
*   Consider the performance implications of robust serialization. Libraries like `dill`, while more robust, might have a slight performance overhead compared to simpler methods. Choose the library that balances robustness and performance for your specific caching needs.
*   For extremely complex scenarios or cross-language compatibility, you might need to explore even more specialized serialization formats like Protocol Buffers or MessagePack, but for most Python-centric caching use cases, `pickle` and `dill` (possibly with Marshmallow for structured data) should provide sufficient robustness.



Below is an example answer formatted in Markdown:

---

### Answer

When it comes to caching, the default serialization (like that used by simple caching solutions) may fail on more complex Python objects. For more robust serialization and deserialization—especially when you need to fall back to an “extra” serializer—the following libraries are popular choices:

- **dill**  
  Dill extends Python’s built-in `pickle` module by supporting a wider array of Python constructs—including lambdas, nested functions, closures, and even modules—making it very useful when handling complex objects. You can serialize almost any Python object with dill.

- **jsonpickle**  
  jsonpickle is great for cases where you’d like to convert your complex Python objects into JSON. It extends the standard `json` module by handling custom classes and more complex data structures. Its output is human-readable, which is useful if you need interoperability between systems.

- **cloudpickle**  
  Like dill, cloudpickle is designed to serialize a wide variety of Python objects, including dynamic objects, functions, and even interactively defined functions. It is used internally by many distributed computing frameworks and can serve as an excellent fallback if the default serializer fails.

### Usage Examples

#### Using dill
```python
import dill

# Suppose you have a complex object, like a lambda function:
square = lambda x: x ** 2

# Serialization
with open('function.pkl', 'wb') as f:
    dill.dump(square, f)

# Deserialization
with open('function.pkl', 'rb') as f:
    loaded_square = dill.load(f)

print(loaded_square(5))  # Output: 25
```

#### Using jsonpickle
```python
import jsonpickle

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

person = Person("Alice", 30)

# Serialization
json_data = jsonpickle.encode(person)
with open('person.json', 'w') as f:
    f.write(json_data)

# Deserialization
with open('person.json', 'r') as f:
    loaded_person = jsonpickle.decode(f.read())

print(loaded_person.name, loaded_person.age)  # Output: Alice 30
```

#### Using cloudpickle
```python
import cloudpickle

def greet(name):
    return f"Hello, {name}!"

# Serialization
with open('greet.pkl', 'wb') as f:
    cloudpickle.dump(greet, f)

# Deserialization
with open('greet.pkl', 'rb') as f:
    loaded_greet = cloudpickle.load(f)

print(loaded_greet("World"))  # Output: Hello, World!
```

### Summary

If a simple caching solution fails to serialize a complex object, you can use libraries like **dill**, **jsonpickle**, or **cloudpickle**. They offer more robust and flexible serialization methods that cover scenarios where the standard serialization (e.g., using `pickle`) may fall short. This extra layer of serialization can be integrated into your caching strategy as a fallback to ensure that even with non-standard or dynamic types, your data is correctly saved and restored.

---

When dealing with complex Python objects that standard serialization methods struggle to handle, consider the following robust serialization libraries:

1. **Dill**: Extends Python's `pickle` module to support a wider range of Python objects, including lambdas and closures.

2. **Cloudpickle**: Similar to `dill`, it can serialize complex objects like functions and classes, making it suitable for distributed computing scenarios.

3. **Jsonpickle**: Builds upon the `json` module to handle more complex data structures by recursively serializing objects into JSON.

To implement a fallback mechanism in your caching solution, you can attempt serialization with a primary method and, upon failure, switch to an alternative serializer. Here's an example using `pickle` as the primary serializer and `dill` as the fallback:

```python
import pickle
import dill

def robust_serialize(obj):
    try:
        # Attempt to serialize with pickle
        return pickle.dumps(obj)
    except (pickle.PicklingError, TypeError):
        # Fallback to dill if pickle fails
        return dill.dumps(obj)

def robust_deserialize(serialized_obj):
    try:
        # Attempt to deserialize with pickle
        return pickle.loads(serialized_obj)
    except (pickle.UnpicklingError, TypeError):
        # Fallback to dill if pickle fails
        return dill.loads(serialized_obj)
```

In this setup, `robust_serialize` first tries to serialize the object using `pickle`. If it encounters an error, it falls back to `dill` for serialization. Similarly, `robust_deserialize` attempts deserialization with `pickle` first and uses `dill` as a fallback in case of failure.

This approach ensures that your caching mechanism can handle a broader spectrum of Python objects, enhancing robustness and reliability. 

Based on the research reports and analysis provided, I can offer a comprehensive overview of robust Python serialization and caching solutions for complex objects, focusing on their features, performance, and fallback mechanisms.

## Overview

When dealing with complex objects in Python, efficient serialization and caching are crucial for optimizing performance and ensuring data integrity. This analysis combines findings on both caching libraries and serialization techniques to provide a holistic view of the available solutions.

## Caching Libraries

Four main caching libraries were investigated: DiskCache, Joblib, Klepto, and Functools. Each offers unique features and trade-offs, as visualized in the feature comparison heatmap:

![fig](https://ydcusercontenteast.blob.core.windows.net/user-content-youagent-output/ee450a81-9877-445a-9ae3-db27cdfecdf0.png)

### DiskCache

DiskCache emerges as a robust, disk-backed cache library with extensive features:

- Customizable serialization
- Thread-safe and process-safe operations
- Multiple eviction policies (LRU, LFU)
- Django compatibility
- Disk-based caching

These features make DiskCache particularly suitable for web applications and scenarios where leveraging disk space for caching is advantageous.

### Joblib

Joblib is well-suited for working with large datasets and complex objects:

- Efficient serialization of large numpy arrays and complex objects
- Support for both memory and disk caching
- Fallback mechanisms (e.g., switching to disk caching if memory is insufficient)

Joblib's ability to handle large datasets efficiently makes it a strong choice for data-intensive applications.

### Klepto

Klepto extends Python's `functools.lru_cache` with additional features:

- Support for multiple caching algorithms (LRU, LFU, MRU)
- Customizable serialization
- Dictionary-style interface

Klepto's flexibility makes it suitable for specialized caching needs.

### Functools

While simpler than the other options, Functools' `lru_cache` decorator provides basic caching functionality and can be extended with custom serialization methods for handling complex objects.

## Serialization Libraries

The research also covered four main serialization libraries: Pickle, JSON, MessagePack, and Protocol Buffers. Their performance characteristics are visualized in the bar chart:

![fig](https://ydcusercontenteast.blob.core.windows.net/user-content-youagent-output/ee450a81-9877-445a-9ae3-db27cdfecdf0.png)

### Pickle

Pickle is a built-in Python library that can serialize a wide variety of Python objects:

- Pros: Versatile, supports complex Python objects, binary format
- Cons: Potential security risks with untrusted sources, version compatibility issues
- Fallback mechanisms: Custom reduction functions, exception handling for `PicklingError` and `UnpicklingError`

### JSON

JSON is a lightweight, text-based serialization format:

- Pros: Text-based, language-independent, widely supported
- Cons: Limited to simple data types, potentially larger data size due to delimiters

### MessagePack

MessagePack offers a binary serialization format that is more efficient than JSON:

- Pros: Efficient binary format, supports complex data structures
- Cons: Requires additional library installation, less human-readable than JSON

### Protocol Buffers

Developed by Google, Protocol Buffers is a language-neutral, platform-neutral serialization mechanism:

- Pros: Efficient, supports complex data structures, language-neutral
- Cons: Requires defining data structure in a .proto file, additional library installation
- Fallback mechanisms: Default values for fields, backward compatibility support

## Synthesis and Recommendations

For robust Python serialization and caching of complex objects, the following recommendations can be made:

1. **Caching**: 
   - For web applications with disk space availability, DiskCache is an excellent choice due to its comprehensive feature set and Django compatibility.
   - For data-intensive applications dealing with large datasets, Joblib provides efficient serialization and fallback mechanisms.
   - For specialized caching needs with custom algorithms, Klepto offers flexibility and a simple interface.

2. **Serialization**:
   - For Python-specific applications dealing with complex objects, Pickle provides versatility but should be used cautiously due to security concerns.
   - For cross-language compatibility and simple data structures, JSON remains a solid choice.
   - For efficient binary serialization of complex structures, MessagePack offers a good balance of performance and ease of use.
   - For high-performance, language-neutral serialization with strong backward compatibility, Protocol Buffers is recommended.

When implementing these solutions, it's crucial to consider the specific requirements of your application, including performance needs, data complexity, and cross-language compatibility. Proper implementation of fallback mechanisms, such as custom reduction functions for Pickle or default values in Protocol Buffers, can significantly enhance the robustness of your serialization and caching solutions.

By carefully selecting and combining the appropriate caching library with a suitable serialization technique, developers can create robust, efficient systems capable of handling complex objects while ensuring data integrity and optimal performance.

For robust serialization and deserialization of complex Python objects, consider the following libraries:

*   **orjson**: A fast and correct JSON library for Python that can serialize dataclass, datetime, NumPy, and UUID instances natively[8]. It also has a `default` parameter that allows the caller to specify how to serialize arbitrary types[8].

*   **Serialite**: A library for serializing and deserializing arbitrarily complex objects in Python[3]. You apply the `@serializable` decorator to a dataclass to automatically create `to_data` and `from_data` methods using the type annotations[3].

*   **Marshmallow**: A library for converting complex datatypes (like objects) to and from native Python datatypes[7]. Marshmallow uses schemas to dictate how objects should be serialized and deserialized, providing flexibility and control over the serialization process[7].

*   **Custom JSONEncoder**: You can define a custom encoder inheriting from `json.JSONEncoder` to handle non-serializable types by implementing the `default()` method[7].

*   **Pickle**: A module that serializes Python object structures into byte streams[2]. Unlike JSON, pickle can handle a wide variety of Python objects, including custom classes[2]. However, it is also the most dangerous, and you should never unpickle data from untrusted sources[2].

*   **pywise**: Offers robust serialization support for NamedTuple and `@dataclass`[6]. It also allows custom serialization for third-party libraries or custom-defined classes that are not decorated with `@dataclass` or derive from NamedTuple by supplying a `CustomFormat`[6].

*   **tblib**: A serialization library for Exceptions and Tracebacks[5]. It allows you to pickle tracebacks and raise exceptions with pickled tracebacks in different processes[5].

Citations:
[1] https://stackoverflow.com/questions/75787023/library-for-json-serialization-deserialization-of-objects-in-python
[2] https://arjancodes.com/blog/comparison-of-the-best-python-serialization-modules/
[3] https://github.com/drhagen/serialite
[4] https://hynek.me/articles/serialization/
[5] https://github.com/ionelmc/python-tblib
[6] https://github.com/malcolmgreaves/pywise
[7] https://blog.finxter.com/5-best-ways-to-serialize-complex-objects-to-json-in-python/
[8] https://pypi.org/project/orjson/
[9] https://stackoverflow.com/questions/46163212/serialize-complex-python-objects-with-multiple-classes-and-lists-to-json
[10] https://dev.to/jvaughn619/python-recursion-errors-serializer-2kh8
[11] https://www.datacamp.com/tutorial/pickle-python-tutorial
[12] https://scribbler.live/2023/05/27/Serialization-in-Python-JavaScript.html
[13] https://www.reddit.com/r/Python/comments/30c8g9/json_serialization_both_ways_for_complex_objects/
[14] https://code.likeagirl.io/serialization-errors-in-python-prevention-and-resolution-232fd45c2e3d
[15] https://www.kdnuggets.com/marshmallow-the-sweetest-python-library-for-data-serialization-and-validation
[16] https://docs.python.org/3/library/pickle.html
[17] https://dev.to/taipy/python-libraries-you-need-to-know-in-2024-37ka
[18] https://github.com/marshmallow-code/marshmallow
[19] https://www.edureka.co/blog/python-libraries/
[20] https://www.reddit.com/r/Python/comments/wzcqln/for_fun_i_created_a_library_to_serialize/
[21] https://realpython.com/python-serialize-data/
[22] https://tryolabs.com/blog/top-python-libraries-2024
[23] https://drlee.io/a-practical-guide-to-serialization-in-python-bring-your-data-to-life-c0646ffe9458
[24] https://www.reddit.com/r/Python/comments/x6wugh/yet_another_object_serialization_framework/
[25] https://github.com/grundic/awesome-python-models
[26] https://www.reddit.com/r/learnpython/comments/16nq0zp/any_reason_to_not_use_repr_and_astliteral_eval_to/
[27] https://github.com/tbebekis/Python-Json
[28] https://stackoverflow.com/questions/75787023/library-for-json-serialization-deserialization-of-objects-in-python
[29] https://stackoverflow.com/questions/36464326/need-a-robust-efficient-python-serializer
[30] https://techvidvan.com/tutorials/serialization-in-python/
[31] https://learnpython.com/blog/object-serialization-in-python/
[32] https://www.linkedin.com/advice/0/how-do-you-handle-data-serialization-effectively-evnuc
[33] https://grimoire.carcano.ch/blog/python-serialization-as-json-or-yaml-exploiting-yaml-tags/
[34] https://jsonpickle.readthedocs.io
[35] https://github.com/MasoniteFramework/exceptionite
[36] https://en.wikipedia.org/wiki/Comparison_of_data-serialization_formats
[37] https://stackoverflow.com/questions/61112983/why-is-python-json-serialization-so-involved-compared-to-some-other-languages
[38] https://www.reddit.com/r/Python/comments/1ah4d2t/my_first_ever_article_finding_the_fastest_python/
[39] https://blog.mbedded.ninja/programming/serialization-formats/a-comparison-of-serialization-formats/
[40] https://www.machinelearningmastery.com/a-gentle-introduction-to-serialization-for-python/
[41] https://voidfiles.github.io/python-serialization-benchmark/
[42] https://github.com/explosion/srsly
[43] https://docs.python-guide.org/scenarios/serialization/
[44] https://www.tutorialspoint.com/python/python_serialization.htm
[45] https://arjancodes.com/blog/comparison-of-the-best-python-serialization-modules/

---
Answer from Perplexity: pplx.ai/share




https://github.com/drhagen/serialite

Token Usage:
GitHub Tokens: 36944
LLM Input Tokens: 0
LLM Output Tokens: 0
Total Tokens: 36944

FileTree:
.github/workflows/ci.yml
.github/workflows/release.yml
.gitignore
README.md
noxfile.py
pyproject.toml
src/serialite/__init__.py
src/serialite/_base.py
src/serialite/_dataclass.py
src/serialite/_decorators.py
src/serialite/_descriptors.py
src/serialite/_dispatcher.py
src/serialite/_fields_serializer.py
src/serialite/_implementations/__init__.py
src/serialite/_implementations/_array.py
src/serialite/_implementations/_boolean.py
src/serialite/_implementations/_date_time.py
src/serialite/_implementations/_dictionary.py
src/serialite/_implementations/_float.py
src/serialite/_implementations/_integer.py
src/serialite/_implementations/_json.py
src/serialite/_implementations/_list.py
src/serialite/_implementations/_literal.py
src/serialite/_implementations/_none.py
src/serialite/_implementations/_ordered_set.py
src/serialite/_implementations/_path.py
src/serialite/_implementations/_reserved.py
src/serialite/_implementations/_set.py
src/serialite/_implementations/_string.py
src/serialite/_implementations/_tuple.py
src/serialite/_implementations/_union.py
src/serialite/_implementations/_uuid.py
src/serialite/_mixins.py
src/serialite/_monkey_patches.py
src/serialite/_numeric_check.py
src/serialite/_result.py
src/serialite/_stable_set.py
tests/__init__.py
tests/fastapi/__init__.py
tests/fastapi/test_abstract.py
tests/fastapi/test_concrete.py
tests/fastapi/test_monkey_patching.py
tests/implementations/__init__.py
tests/implementations/test_boolean.py
tests/implementations/test_date_time.py
tests/implementations/test_float.py
tests/implementations/test_integer.py
tests/implementations/test_json.py
tests/implementations/test_list.py
tests/implementations/test_literal.py
tests/implementations/test_none.py
tests/implementations/test_optional.py
tests/implementations/test_ordered_dict.py
tests/implementations/test_ordered_set.py
tests/implementations/test_raw_dict.py
tests/implementations/test_reserved.py
tests/implementations/test_set.py
tests/implementations/test_string.py
tests/implementations/test_try_union.py
tests/implementations/test_tuple.py
tests/implementations/test_uuid.py
tests/test_dataclass.py
tests/test_dispatcher.py
tests/test_field_serializers.py
tests/test_mixins.py
tests/test_numpy.py
tests/test_serializers_base.py
tests/test_stable_set.py

Analysis:
.github/workflows/ci.yml
```.yml
name: CI

on:
  pull_request:
  push:
    branches:
      - master

env:
  python-version: "3.10"
  poetry-version: "1.8.4"

jobs:
  test:
    strategy:
      matrix:
        python-version: ["3.10", "3.11", "3.12", "3.13"]
    runs-on: ubuntu-24.04
    steps:
      - name: Checkout repo
        uses: actions/checkout@v4
      - name: Install Poetry
        run: pipx install poetry==${{ env.poetry-version }}
      - name: Install Python ${{ matrix.python-version }}
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
          cache: poetry
      - name: Install environment
        run: poetry install
      - name: Test with nox
        run: >-
          poetry run nox -s
          test-${{ matrix.python-version }}
          test_fastapi-${{ matrix.python-version }}
          test_numpy-${{ matrix.python-version }}
          test_ordered_set-${{ matrix.python-version }}
      - name: Store coverage
        uses: actions/upload-artifact@v4
        with:
          name: coverage-${{ matrix.python-version }}
          path: .coverage.*
          include-hidden-files: true
          if-no-files-found: error
  coverage:
    needs: test
    runs-on: ubuntu-24.04
    steps:
      - name: Checkout repo
        uses: actions/checkout@v4
      - name: Install Poetry
        run: pipx install poetry==${{ env.poetry-version }}
      - name: Install Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ env.python-version }}
          cache: poetry
      - name: Install environment
        run: poetry install
      - name: Fetch coverage
        uses: actions/download-artifact@v4
        with:
          pattern: coverage-*
          merge-multiple: true
      - name: Combine coverage and generate report
        run: poetry run nox -s coverage
      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v4
        with:
          token: ${{ secrets.CODECOV_TOKEN }}
          fail_ci_if_error: true
  lint:
    runs-on: ubuntu-24.04
    steps:
      - name: Checkout repo
        uses: actions/checkout@v4
      - name: Install Poetry
        run: pipx install poetry==${{ env.poetry-version }}
      - name: Install Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ env.python-version }}
          cache: poetry
      - name: Install environment
        run: poetry install
      - name: Run code quality checks
        run: poetry run nox -s lint
  poetry-check:
    runs-on: ubuntu-24.04
    steps:
      - name: Checkout repo
        uses: actions/checkout@v4
      - name: Install Poetry
        run: pipx install poetry==${{ env.poetry-version }}
      - name: Install Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ env.python-version }}
      - name: Validate Poetry configuration and lockfile freshness
        run: poetry lock --check

```
.github/workflows/release.yml
```.yml
name: Release

on:
  push:
    tags:
      - 'v*'

env:
  python-version: "3.10"
  poetry-version: "1.8.4"

jobs:
  pypi-publish:
    name: Publish release to PyPI
    runs-on: ubuntu-24.04
    environment: release
    permissions:
      id-token: write
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      - name: Install Poetry
        run: pipx install poetry==${{ env.poetry-version }}
      - name: Install Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ env.python-version }}
      - name: Build release with Poetry
        run: poetry build
      - name: Check that tag version and Poetry version match
        run: '[[ "v$(poetry version --short)" == "${{ github.ref_name }}" ]]'
      - name: Upload distribution to PyPI
        uses: pypa/gh-action-pypi-publish@release/v1

```
.gitignore
```.gitignore
__pycache__
/.nox
/.coverage*
/coverage.xml
/dist

```
README.md
# Serialite

Serialite is a library serializing and deserializing arbitrarily complex objects in Python. You
apply the `@serializable` decorator to a dataclass to automatically create `to_data` and `from_data`
methods using the type annotations. Or for more control, inherit from the `SerializableMixin` and
implement the class attribute `__fields_serializer__`. For even more control, inherit from the 
abstract base class `Serializer` and implement the `to_data` and `from_data` methods directly. 

## Basics

The abstract base class is `Serializer`:

```python
class Serializer(Generic[Output]):
    def from_data(self, data: Json) -> DeserializationSuccess[Output]: ...
    def to_data(self, value: Output) -> Json: ...
```

The class is generic in the type of the object that it serializes. The two abstract methods
`from_data` and `to_data` are the key to the whole design, which revolves around getting objects to
and from JSON-serializable data, which are objects constructed entirely of `bool`s, `int`s, 
`float`s, `list`s, and `dict`s. Such structures can be consumed by `json.dumps` to produce a string
and produced by `json.loads` after consuming a string. By basing the serialization around JSON
serializable data, complex structures can be built up or torn down piece by piece while
alternatively building up complex error messages during deserialization which pinpoint the location
in the structure where the bad data exist.

For new classes, it is recommended that the `Serializer` be implemented on the class itself. There is
an abstract base class `Serializable` that classes can inherit from to indicate this. There is a mixin
`SerializableMixin` that provides an implementation of `from_data` and `to_data` for any class that
implements the `__fields_serializer` class attribute.

For `dataclass`es, it is even easier. There is a decorator `serializable` that inserts
`SerializableMixin` into the list of base classes after the `dataclass` decorator has run and also
generates `__fields_serializer__` from the data class attributes.

Finding the correct serializer for each type can be a pain, so
`serializer(cls: type) -> Serializer` is provided as a convenience function. This is a single
dispatch function, which looks up the serializer registered for a particular type. For example,
`serializer(list[float])` will return `ListSerializer(FloatSerializer)`.

noxfile.py
```.py
from nox import options, parametrize
from nox_poetry import Session, session

options.sessions = ["test", "test_fastapi", "test_numpy", "test_ordered_set", "coverage", "lint"]


@session(python=["3.10", "3.11", "3.12", "3.13"])
def test(s: Session):
    s.install(".", "pytest", "pytest-cov")
    s.env["COVERAGE_FILE"] = f".coverage.{s.python}"
    s.run("python", "-m", "pytest", "--cov", "serialite")


@session(python=["3.10", "3.11", "3.12", "3.13"])
def test_fastapi(s: Session):
    s.install(".[fastapi]", "pytest", "pytest-cov", "httpx")
    s.env["COVERAGE_FILE"] = f".coverage.fastapi.{s.python}"
    s.run("python", "-m", "pytest", "--cov", "serialite", "tests/fastapi")


@session(python=["3.10", "3.11", "3.12", "3.13"])
def test_numpy(s: Session):
    s.install(".[numpy]", "pytest", "pytest-cov")
    s.env["COVERAGE_FILE"] = f".coverage.numpy.{s.python}"
    s.run("python", "-m", "pytest", "--cov", "serialite", "tests/test_numpy.py")


@session(python=["3.10", "3.11", "3.12", "3.13"])
def test_ordered_set(s: Session):
    s.install(".[ordered-set]", "pytest", "pytest-cov")
    s.env["COVERAGE_FILE"] = f".coverage.ordered_set.{s.python}"
    s.run(
        "python", "-m", "pytest", "--cov", "serialite", "tests/implementations/test_ordered_set.py"
    )


@session(venv_backend="none")
def coverage(s: Session):
    s.run("coverage", "combine")
    s.run("coverage", "html")
    s.run("coverage", "xml")


@session(venv_backend="none")
@parametrize("command", [["ruff", "check", "."], ["ruff", "format", "--check", "."]])
def lint(s: Session, command: list[str]):
    s.run(*command)


@session(venv_backend="none")
def format(s: Session) -> None:
    s.run("ruff", "check", ".", "--select", "I", "--fix")
    s.run("ruff", "format", ".")

```
pyproject.toml
```.toml
[tool.poetry]
name = "serialite"
version = "0.3.5"
description = "A serialization library for Python"
authors = ["David Hagen <david@drhagen.com>"]
license = "MIT"
readme = "README.md"
repository = "https://github.com/drhagen/serialite"
keywords = ["serialization", "deserialization", "serde", "pydantic", "fastapi"]
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "Operating System :: OS Independent",
]


[tool.poetry.dependencies]
python = "^3.10"
typing_extensions = "^4.3"
fastapi = { version = ">=0.100,<0.111", optional = true }
pydantic = { version = "^1.10", optional = true }
ordered-set = { version = "^4.1", optional = true }
numpy = { version = "^1.25", optional = true }

[tool.poetry.dev-dependencies]
nox_poetry = "^1.0.3"

# Test
pytest = "^8"
pytest-cov = "*"
httpx = "*" # Needed by starlette testclient

# Lint
ruff = "^0.3"

[tool.poetry.extras]
fastapi = ["fastapi", "pydantic"]
numpy = ["numpy"]
ordered-set = ["ordered-set"]


[tool.coverage.run]
branch = true

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "raise NotImplementedError",
    "if TYPE_CHECKING:",
]

[tool.coverage.paths]
source = [
    "src/",
    ".nox/test*/lib/python*/site-packages/",
    ".nox/test*/Lib/site-packages/",
]


[tool.ruff]
src = ["src"]
line-length = 99

[tool.ruff.lint]
extend-select = [
    "I", # isort
    "N", # pep8-naming
    "RUF", # ruff
    "B", # flake8-bugbear
    "N", # flake8-broken-line
    "C4", # flake8-comprehensions
    "PIE", # flake8-pie
    "PT", # flake8-pytest-style
    "PTH", # flake8-use-pathlib
    "ERA", # flake8-eradicate
]
# F402: Variable shadowing is perfectly fine
# PT011: testing for broad exceptions is fine
extend-ignore = ["F402", "PT011"]

[tool.ruff.lint.per-file-ignores]
# F401: unused-import; Allow unused imports in __init__.py files
"__init__.py" = ["F401"]

[tool.ruff.lint.isort]
extra-standard-library = ["typing_extensions"]

[tool.ruff.lint.pep8-naming]
classmethod-decorators = ["serialite._descriptors.classproperty"]

[tool.ruff.lint.flake8-bugbear]
extend-immutable-calls = ["serialite.field", "fastapi.Body"]


[build-system]
requires = ["poetry-core>=1.0.0"]
build-backend = "poetry.core.masonry.api"

```
src/serialite/__init__.py
```.py
from ._base import Serializable, Serializer
from ._dataclass import field
from ._decorators import abstract_serializable, serializable
from ._dispatcher import serializer
from ._fields_serializer import (
    AccessPermissions,
    FieldsSerializer,
    FieldsSerializerField,
    MultiField,
    SingleField,
    empty_default,
    no_default,
)
from ._implementations import *  # noqa: F403
from ._mixins import AbstractSerializableMixin, SerializableMixin
from ._monkey_patches import (
    monkey_patch_fastapi_create_cloned_field,
    monkey_patch_pydantic_get_flat_models_from_model,
    monkey_patch_pydantic_instancecheck,
    monkey_patch_pydantic_model_type_schema,
    monkey_patch_pydantic_subclasscheck,
)
from ._result import (
    DeserializationError,
    DeserializationFailure,
    DeserializationResult,
    DeserializationSuccess,
)
from ._stable_set import StableSet

monkey_patch_pydantic_subclasscheck()
monkey_patch_pydantic_instancecheck()
monkey_patch_fastapi_create_cloned_field()
monkey_patch_pydantic_get_flat_models_from_model()
monkey_patch_pydantic_model_type_schema()

```
src/serialite/_base.py
```.py
from __future__ import annotations

__all__ = ["Serializer", "Serializable"]

from abc import abstractmethod
from typing import TYPE_CHECKING, Any, Generic, TypeVar

from ._descriptors import classproperty
from ._result import DeserializationFailure, DeserializationResult
from ._stable_set import StableSet

if TYPE_CHECKING:
    from pydantic.typing import AbstractSetIntStr, MappingIntStrAny

Output = TypeVar("Output")
SerializableOutput = TypeVar("SerializableOutput", bound="Serializable")


class Serializer(Generic[Output]):
    """Serialize and deserialize a particular object."""

    @abstractmethod
    def from_data(self, data: Any) -> DeserializationResult[Output]:
        """Deserialize an object from data."""
        raise NotImplementedError()

    @abstractmethod
    def to_data(self, value: Output) -> Any:
        """Serialize an object to data."""
        raise NotImplementedError()

    def collect_openapi_models(
        self, parent_models: StableSet[Serializer]
    ) -> StableSet[Serializer]:
        """Collect the set of OpenAPI models required for this Serializer.

        `Serializer`s that represent models should return a set containing
        themselves.

        `Serializer`s with child `Serializer`s that may be models should add
        themselves to `parent_models` and pass that to all children's
        `collect_openapi_models` method. The parent `Serializer` and all models
        received from children should be combined and returned.

        The default is to return no models.
        """
        return StableSet()

    def to_openapi_schema(self, refs: dict[Serializer, str], force: bool = False) -> Any:
        """Generate the OpenAPI schema representation for this class.

        Each serializer should check if its fully qualified name exists in
        `refs` and return a '$ref', unless `force` is true, in which case it
        should return its full schema, but not pass `force` to its child
        serializers.

        The default is no schema.
        """
        return {}


class Serializable(Serializer[SerializableOutput]):
    """Classes that serialize instances of themselves."""

    # There is no way to indicate in Python's type system that
    # type[Serializable] is an instance of Serializer. So these signatures
    # appear inconsistent with the base class.
    @classmethod
    @abstractmethod
    def from_data(cls, data: Any) -> DeserializationResult[Output]:
        pass

    @abstractmethod
    def to_data(self: SerializableOutput) -> Any:
        pass

    @classmethod
    def collect_openapi_models(cls, parent_models: StableSet[Serializer]) -> StableSet[Serializer]:
        return StableSet()

    @classmethod
    def to_openapi_schema(cls, refs: dict[Serializer, str], force: bool = False) -> Any:
        return {}

    # All attributes and methods below this point are for Pydantic
    # compatibility. These methods along with the appropriate monkey patching
    # allow all Serialite Serializables to be used as Pydantic BaseModels.

    # This flag is used by the issubclass(_, BaseModel) monkey patch to identify
    # classes that claim to be subclasses of BaseModel.
    _is_pydantic_base_model = True

    # This flag protects dataclasses from conversion
    __processed__ = True

    @classmethod
    def validate(cls, value: Any, values, field, config):
        # This is the canonical name for the main Pydantic validator. It does
        # not have to have this name as long as it is returned by
        # __get_validators__.

        # FastAPI passes in both data to be parsed and instances of the object
        # itself for some reason. Politely return the object if we get an
        # instance of this class.
        if isinstance(value, cls):
            return value

        result = cls.from_data(value)

        if isinstance(result, DeserializationFailure):
            # Must raise ValueError, TypeError, or AssertionError for Pydantic
            # to catch it. Or we could construct a Pydantic ValidationError.
            # https://pydantic-docs.helpmanual.io/usage/validators/
            raise ValueError(result.error)
        else:
            return result.or_die()

    @classmethod
    def __get_validators__(cls):
        # FastAPI uses pydantic.fields.ModelField to convert a type hint into a
        # Pydantic parser. ModelField relies on this field to get the parser.
        # The call chain is here: APIRoute > get_dependant > get_param_field >
        # create_response_field > ModelField > prepare > populate_validators >
        # __get_validators__

        yield cls.validate

    @classproperty
    def __config__(cls):
        # FastAPI accesses this attribute in a few places. It does not matter.
        try:
            from pydantic import BaseConfig

            return BaseConfig
        except ImportError:
            # Protect against auto-documentation programs trying to get all
            # properties.
            return None

    def dict(
        self,
        include: AbstractSetIntStr | MappingIntStrAny = None,
        exclude: AbstractSetIntStr | MappingIntStrAny = None,
        by_alias: bool = False,
        skip_defaults: bool = None,  # noqa: RUF013
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
    ):
        # FastAPI and Pydantic can only serialize instances of the validator,
        # which is why dict is implemented on Serializable instead of plain Serializer.
        # Serialite Serializers simply cannot be passed directly to FastAPI.

        data = self.to_data()
        if exclude is not None:
            data = {key: value for key, value in data.items() if key not in exclude}

        if hasattr(self, "__subclass_serializers__"):
            # Pydantic has no concept of algebraic data types. It does not use
            # the field to determine how to serialize an object. It purely asks
            # the object itself how it should be serialized via the dict
            # method. This implementation of dict assumes that anytime a
            # subclass of an abstract serializable is serialized, it was
            # supposed to be serialized with the abstract serializer, not the
            # concrete class. This is not a good assumption, but Pydantic is not
            # expressive enough to have two serializers for the same object.
            return {"_type": self.__class__.__name__} | data
        else:
            return data

```
src/serialite/_dataclass.py
```.py
__all__ = ["field"]

import dataclasses
from dataclasses import MISSING, Field

from ._base import Serializer


def field(
    *,
    default=MISSING,
    default_factory=MISSING,
    serializer: Serializer | type = MISSING,
    init: bool = True,
    repr: bool = True,
    hash: bool | None = None,
    compare: bool = True,
    metadata: dict | None = None,
    kw_only: bool = MISSING,
) -> Field:
    serializer_metadata = (metadata if metadata is not None else {}) | {"serializer": serializer}
    return dataclasses.field(
        default=default,
        default_factory=default_factory,
        init=init,
        repr=repr,
        hash=hash,
        compare=compare,
        metadata=serializer_metadata,
        kw_only=kw_only,
    )

```
src/serialite/_decorators.py
```.py
__all__ = ["serializable", "abstract_serializable"]

import dataclasses
from dataclasses import MISSING
from functools import wraps
from typing import get_type_hints

from ._base import Serializable, Serializer
from ._descriptors import classproperty
from ._fields_serializer import FieldsSerializer, SingleField, no_default
from ._mixins import AbstractSerializableMixin, SerializableMixin

# Allow commented out code in this file because it is important documentation
# ruff: noqa: ERA001


# Inspired by https://stackoverflow.com/a/14412901/1485877
def flexible_decorator(dec):
    """A decorator decorator to allow it to be used with or without parameters.

    Decorate a decorator like this:

    @decorator
    def multiply(f, factor=2):
        # Multiply a function's return value by some factor
        @wraps(f)
        def wrap(*args, **kwargs):
            return factor * f(*args, **kwargs)
        return wrap

    Then use the decorator in any of the following ways:

    @multiply
    def f1(x, y):
        return x + y

    @multiply(3)
    def f2(x, y):
        return x * y

    @multiply(factor=5)
    def f3(x, y):
        return x - y

    assert f1(2, 3) == (2 + 3) * 2
    assert f2(2, 5) == (2 * 5) * 3
    assert f3(8, 1) == (8 - 1) * 5

    Note that this technique will fail if the decorator can be parameterized
    with a single positional argument that is callable.
    """

    @wraps(dec)
    def new_dec(*args, **kwargs):
        if len(args) == 1 and len(kwargs) == 0 and callable(args[0]):
            # Bare decorated function
            return dec(args[0])
        else:
            # Decorator called with arguments
            return lambda f: dec(f, *args, **kwargs)

    return new_dec


def infer_fields_serializer(cls):
    from . import serializer

    if "__fields_serializer__" in cls.__dict__:
        raise TypeError(
            "Cannot apply serializable decorator to a class that already defines"
            " __fields_serializer__. Remove __fields_serializer__ so that serializable can add it"
            " or inherit from SerializableMixin to use the __fields_serializer__ that is already"
            " defined."
        )

    if dataclasses.is_dataclass(cls):
        # The field serializers and default values are inferred from the dataclass fields.
        # If available, the serializer on the dataclass field takes priority
        fields = dataclasses.fields(cls)
        types = get_type_hints(cls)

        serializer_fields = {}
        for field in fields:
            maybe_serializer = field.metadata.get("serializer", MISSING)
            if maybe_serializer is not MISSING:
                field_serializer = maybe_serializer
            else:
                field_serializer = serializer(types[field.name])

            maybe_default = field.default
            maybe_factory_default = field.default_factory
            if maybe_default is MISSING and maybe_factory_default is MISSING:
                # Recast to our sentinel for no default
                field_default = no_default
            elif maybe_default is not MISSING:
                field_default = maybe_default
            elif maybe_factory_default is not MISSING:
                field_default = maybe_factory_default()

            serializer_fields[field.name] = SingleField(field_serializer, default=field_default)

        cls.__fields_serializer__ = FieldsSerializer(**serializer_fields)
    else:
        raise TypeError("The serializable decorator can only be applied to dataclasses.")


@flexible_decorator
def serializable(cls):
    """Decorator that provides Serializable interface.

    This decorator can be applied to a dataclass. It inserts `SerializableMixin`
    at the front of the list of base classes and generates a reasonable
    `__fields_serializer__` class attribute from the dataclass fields.
    """
    infer_fields_serializer(cls)

    new_bases = (SerializableMixin, *cls.__bases__)
    try:
        # Try to mutate the bases of the class in place.
        # This will fail if the only base is `object`.
        cls.__bases__ = new_bases
        cls.__init_subclass__()
    except TypeError:
        # If that fails, create a new class with the same name
        # This breaks any descriptors--in particular, cached_property--so do not use this technique
        # cls = type(cls.__name__, (SerializableMixin,) + cls.__bases__, dict(cls.__dict__))

        # Add the appropriate methods directly to the class
        # Only supply implementation if it was not supplied in class
        # Get the canonical implementations from Serializable and SerializableMixin.
        # Get the method from the __dict__ and not from attribute access so that
        # we get the unbound methods rather than the bound ones.
        if "from_data" not in cls.__dict__:
            cls.from_data = SerializableMixin.__dict__["from_data"]

        if "to_data" not in cls.__dict__:
            cls.to_data = SerializableMixin.__dict__["to_data"]

        if "collect_openapi_models" not in cls.__dict__:
            cls.collect_openapi_models = SerializableMixin.__dict__["collect_openapi_models"]

        if "to_openapi_schema" not in cls.__dict__:
            cls.to_openapi_schema = SerializableMixin.__dict__["to_openapi_schema"]

        if "_is_pydantic_base_model" not in cls.__dict__:
            cls._is_pydantic_base_model = Serializable.__dict__["_is_pydantic_base_model"]

        if "validate" not in cls.__dict__:
            cls.validate = Serializable.__dict__["validate"]

        if "__get_validators__" not in cls.__dict__:
            cls.__get_validators__ = Serializable.__dict__["__get_validators__"]

        if "__config__" not in cls.__dict__:
            cls.__config__ = Serializable.__dict__["__config__"]

        if "dict" not in cls.__dict__:
            cls.dict = Serializable.__dict__["dict"]

        if "__processed__" not in cls.__dict__:
            cls.__processed__ = Serializable.__dict__["__processed__"]

    return cls


@classproperty
def __subclass_serializers__(cls) -> dict[str, Serializer]:  # noqa: N807
    return {subclass.__name__: subclass for subclass in cls.__subclasses__()}


def infer_subclass_serializers(cls):
    if "__subclass_serializers__" in cls.__dict__:
        raise TypeError(
            "Cannot apply abstract_serializable decorator to a class that already defines"
            " __subclass_serializers__. Remove __subclass_serializers__ so that"
            " abstract_serializable can add it or inherit from AbstractSerializableMixin to use"
            " the __subclass_serializers__ that is already defined."
        )

    cls.__subclass_serializers__ = __subclass_serializers__


@flexible_decorator
def abstract_serializable(cls):
    """Decorator that provides AbstractSerializableMixin interface.

    This decorator can be applied to an abstract class. It inserts
    `AbstractSerializableMixin` at the front of the list of base classes and
    generates a reasonable `__subclass_serializers__` class property.
    """
    infer_subclass_serializers(cls)

    new_bases = (AbstractSerializableMixin, *cls.__bases__)
    try:
        # Try to mutate the bases of the class in place.
        # This will fail if the only base is `object`.
        cls.__bases__ = new_bases
        cls.__init_subclass__()
    except TypeError:
        # If that fails, create a new class with the same name
        # This breaks any descriptors--in particular, cached_property--so do not use this technique
        # cls = type(
        #     cls.__name__,
        #     (AbstractSerializableMixin,) + cls.__bases__, dict(cls.__dict__),
        # )

        # Do the same thing as serializable, but use AbstractSerializableMixin
        # instead of SerializableMixin.
        if "from_data" not in cls.__dict__:
            cls.from_data = AbstractSerializableMixin.__dict__["from_data"]

        if "to_data" not in cls.__dict__:
            cls.to_data = AbstractSerializableMixin.__dict__["to_data"]

        if "__subclass_serializers__" not in cls.__dict__:
            cls.__subclass_serializers__ = AbstractSerializableMixin.__dict__[
                "__subclass_serializers__"
            ]

        if "collect_openapi_models" not in cls.__dict__:
            cls.collect_openapi_models = AbstractSerializableMixin.__dict__[
                "collect_openapi_models"
            ]

        if "to_openapi_schema" not in cls.__dict__:
            cls.to_openapi_schema = AbstractSerializableMixin.__dict__["to_openapi_schema"]

        if "_is_pydantic_base_model" not in cls.__dict__:
            cls._is_pydantic_base_model = Serializable.__dict__["_is_pydantic_base_model"]

        if "validate" not in cls.__dict__:
            cls.validate = Serializable.__dict__["validate"]

        if "__get_validators__" not in cls.__dict__:
            cls.__get_validators__ = Serializable.__dict__["__get_validators__"]

        if "__config__" not in cls.__dict__:
            cls.__config__ = Serializable.__dict__["__config__"]

        if "dict" not in cls.__dict__:
            cls.dict = Serializable.__dict__["dict"]

        if "__processed__" not in cls.__dict__:
            cls.__processed__ = Serializable.__dict__["__processed__"]

    return cls

```
src/serialite/_descriptors.py
```.py
__all__ = ["classproperty"]


# classmethod cannot be used with property, so we have to manually write our own
# descriptor class. From https://stackoverflow.com/a/39542816/
class classproperty(property):  # noqa: N801
    def __get__(self, obj, objtype=None):
        return super().__get__(objtype)

    def __set__(self, obj, value):
        super().__set__(type(obj), value)

    def __delete__(self, obj):
        super().__delete__(type(obj))

```
src/serialite/_dispatcher.py
```.py
__all__ = ["serializer"]

from abc import get_cache_token
from datetime import datetime
from pathlib import Path
from types import GenericAlias, UnionType
from typing import Any, Literal, TypeVar, Union, get_origin
from uuid import UUID

from ._base import Serializer

Output = TypeVar("Output")


def subclassdispatch(func):
    """Single dispatch based on the subclass of the first argument.

    This is a modified version of `functools.singledispatch` that dispatches on
    whether or not the first argument is a subtype of the registered type.

    It is a decorator of a generic function `func`.

    ```
    @subclassdispatch
    def my_func(cls: type):
        print('Default implementation')
    ```

    This imbues `func` with the `func.register` decorator, which can be used to
    register methods of the generic function for a particular type.

    ```
    @my_func.register(list)
    def my_func_for_int(cls):
        print('list was received')
    ```

    If `func` is called with a type `cls` (not an instance of a type, an actual
    type object itself), then the body of the method that is registered with a
    subtype of `cls` (including `cls` itself) will be run. If no supertype of
    `cls` is registered, then the body of the generic function is run.

    This will only work as the dispatcher for `serializer` as the `Union`,
    `Optional`, `Literal`, and `Any` types are hardcoded to dispatch to their
    respective serializers because the `issubclass` function does not work on
    them. This decorator cannot be used outside of this module.
    """
    from functools import _find_impl, update_wrapper
    from types import MappingProxyType
    from typing import _GenericAlias
    from weakref import WeakKeyDictionary

    registry = {}
    dispatch_cache = WeakKeyDictionary()
    cache_token = None

    def dispatch(cls: type):
        """generic_func.dispatch(cls) -> <function implementation>

        Runs the dispatch algorithm to return the best available implementation
        for the given `cls` registered on `generic_func`
        """
        nonlocal cache_token
        if cache_token is not None:
            current_token = get_cache_token()
            if cache_token != current_token:
                dispatch_cache.clear()
                cache_token = current_token

        origin = get_origin(cls)
        if origin in {Union, UnionType}:
            # issubclass does not work on Union and Optional
            # WeakKeyDictionary does not work on UnionType
            # must bypass the dispatcher
            if len(cls.__args__) == 2 and cls.__args__[1] is type(None):
                # Optional is just a Union with NoneType in the second argument
                return optional_to_data
            else:
                # This is the standard Union
                return union_to_data

        try:
            impl = dispatch_cache[cls]
        except KeyError:
            try:
                impl = registry[cls]
            except KeyError:
                if isinstance(cls, GenericAlias) or issubclass(cls.__class__, _GenericAlias):
                    # issubclass does not work on Generic types since Python 3.7.0;
                    # must extract the base class and dispatch on that
                    if origin is Literal:
                        # issubclass does not work on Literal either
                        impl = literal_to_data
                    else:
                        # This is the standard Generic class
                        impl = _find_impl(origin, registry)
                elif cls is Any:
                    # issubclass does not work on Any; must directly inject this
                    impl = any_to_data
                else:
                    impl = _find_impl(cls, registry)
            dispatch_cache[cls] = impl
        return impl

    def register(cls, func=None):
        """generic_func.register(cls, func) -> func

        Registers a new implementation for the given *cls* on a *generic_func*.
        """
        nonlocal cache_token
        if func is None:
            return lambda f: register(cls, f)
        registry[cls] = func
        if cache_token is None and hasattr(cls, "__abstractmethods__"):
            cache_token = get_cache_token()
        dispatch_cache.clear()
        return func

    def wrapper(*args, **kw):
        # This differs from functools.singledispatch by using args[0] rather than args[0].__class__
        return dispatch(args[0])(*args, **kw)

    registry[object] = func
    wrapper.register = register
    wrapper.dispatch = dispatch
    wrapper.registry = MappingProxyType(registry)
    wrapper._clear_cache = dispatch_cache.clear
    update_wrapper(wrapper, func)
    return wrapper


# Classes we control can have from_data and to_data methods on them. External
# classes need to have a Serializer defined for them. By default we duck type
# and assume that the appropriate methods are already defined on the class.


@subclassdispatch
def serializer(cls: type[Output]) -> Serializer[Output]:
    """Given a class, return a serializer of instances of that class."""
    return cls


@serializer.register(type(None))
def none_to_data(cls):
    from ._implementations import NoneSerializer

    return NoneSerializer()


@serializer.register(bool)
def boolean_to_data(cls):
    from ._implementations import BooleanSerializer

    return BooleanSerializer()


@serializer.register(int)
def integer_to_data(cls):
    from ._implementations import IntegerSerializer

    return IntegerSerializer()


@serializer.register(float)
def float_to_data(cls):
    from ._implementations import FloatSerializer

    return FloatSerializer()


@serializer.register(str)
def string_to_data(cls):
    from ._implementations import StringSerializer

    return StringSerializer()


@serializer.register(datetime)
def datetime_to_data(cls):
    from ._implementations import DateTimeSerializer

    return DateTimeSerializer()


@serializer.register(UUID)
def uuid_to_data(cls):
    from ._implementations import UuidSerializer

    return UuidSerializer()


@serializer.register(list)
def list_to_data(cls):
    from ._implementations import ListSerializer

    return ListSerializer(serializer(cls.__args__[0]))


@serializer.register(set)
def set_to_data(cls):
    from ._implementations import SetSerializer

    return SetSerializer(serializer(cls.__args__[0]))


@serializer.register(tuple)
def tuple_to_data(cls):
    from ._implementations import TupleSerializer

    return TupleSerializer(*(serializer(arg) for arg in cls.__args__))


@serializer.register(dict)
def dict_to_data(cls):
    from ._implementations import OrderedDictSerializer, RawDictSerializer

    if cls.__args__[0] is str:
        return RawDictSerializer(serializer(cls.__args__[1]))
    else:
        return OrderedDictSerializer(serializer(cls.__args__[0]), serializer(cls.__args__[1]))


@serializer.register(Path)
def path_to_data(cls):
    from ._implementations import PathSerializer

    return PathSerializer()


# Union disables subclassing so Optional cannot be used to dispatch
# @serializer.register(Optional)
def optional_to_data(cls):
    from ._implementations import OptionalSerializer

    return OptionalSerializer(serializer(cls.__args__[0]))


# Union disables subclassing so it cannot be used to dispatch
# @serializer.register(Union)
def union_to_data(cls):
    from ._implementations import TryUnionSerializer

    return TryUnionSerializer(*[serializer(type_arg) for type_arg in cls.__args__])


# @serializer.register(Literal)
def literal_to_data(cls):
    from ._implementations import LiteralSerializer

    return LiteralSerializer(*cls.__args__)


# @serializer.register(Any)
def any_to_data(cls):
    from ._implementations import JsonSerializer

    return JsonSerializer()


try:
    import numpy as np
except ImportError:
    pass
else:

    @serializer.register(np.ndarray)
    def array_to_data(cls):
        from ._implementations import ArraySerializer

        return ArraySerializer(dtype=float)


try:
    from ordered_set import OrderedSet
except ImportError:
    pass
else:

    @serializer.register(OrderedSet)
    def ordered_set_to_data(cls):
        from ._implementations import OrderedSetSerializer

        return OrderedSetSerializer(serializer(cls.__args__[0]))

```
src/serialite/_fields_serializer.py
```.py
from __future__ import annotations

__all__ = [
    "FieldsSerializer",
    "AccessPermissions",
    "FieldsSerializerField",
    "SingleField",
    "MultiField",
    "no_default",
    "empty_default",
]

from collections.abc import Mapping
from enum import Enum, auto
from typing import Any

from ._base import Serializer
from ._result import DeserializationFailure, DeserializationResult, DeserializationSuccess
from ._stable_set import StableSet

# A sentinel object to indicate that a default is not available,
# so an error should be raised if the item is not found
no_default = object()

# A sentinel object to indicate that a default is not necessary,
# so the associated field should remain blank
empty_default = object()


class AccessPermissions(Enum):
    read_write = auto()
    read_only = auto()
    write_only = auto()

    def readable(self):
        return self == AccessPermissions.read_write or self == AccessPermissions.read_only

    def writeable(self):
        return self == AccessPermissions.read_write or self == AccessPermissions.write_only


class FieldsSerializerField:
    def __init__(
        self,
        *,
        default: Any = no_default,
        hide_default: bool = True,
        access: AccessPermissions = AccessPermissions.read_write,
    ):
        """Abstract base class for arguments to FieldsSerializer.

        Subclasses of this algebraic data type serve a single purpose in
        fulfilling the `object_field_serializers` argument of
        `FieldsSerializer`.
        """
        self.default = default
        self.hide_default = hide_default
        self.access = access

    @property
    def readable(self):
        return self.access.readable()

    @property
    def writable(self):
        return self.access.writeable()


class SingleField(FieldsSerializerField):
    def __init__(
        self,
        serializer: Serializer | Any,
        *,
        default: Any = no_default,
        hide_default: bool = True,
        access: AccessPermissions = AccessPermissions.read_write,
    ):
        """A field serializer with a direct data field to object field mapping.

        This is only useful as an argument to `FieldsSerializer`. It represents
        a field where the name of the field in the data is the same as the name
        of the field on the object.

        `serializer` is either a `serialite.Serializer` or an object which can
        be passed to `serialite.serializer` to obtain one.

        `default` controls what happens if the data does not provide a value for
        this field. If it is the sentinel `no_default`, then a failure is
        generated. If it is the sentinel `empty_default`, then no value for this
        field is given. If it is any other value, then that value is given for
        this field.

        If `hide_default` is `True`, when serializing, if the serialized value
        equals `default`, then the field is omitted from the serialized data.

        If `access` is `read_write`, the field is used when both deserializing
        and serializing. If it is `read_only`, the field is only used when
        serializing. If it is `write_only`, the field is only used when
        deserializing.
        """
        from . import serializer as lookup_serializer

        if not isinstance(serializer, Serializer):
            serializer = lookup_serializer(serializer)

        super().__init__(default=default, hide_default=hide_default, access=access)
        self.serializer = serializer


class MultiField(FieldsSerializerField):
    def __init__(
        self,
        serializers: dict[str, Serializer | Any],
        *,
        default: Any = no_default,
        hide_default: bool = True,
        access: AccessPermissions = AccessPermissions.read_write,
        to_data: str = None,  # noqa: RUF013
    ):
        """A field serializer with a direct data field to object field mapping.

        This is only useful as an argument to `FieldsSerializer`. It represents
        a field where there are multiple data fields that can map to a single
        object field. The name of the data field controls which serializer is
        applied. Multiple data fields being satisfied results in a failure.

        Each value in `serializers` is either a `serialite.Serializer` or an
        object which can be passed to `serialite.serializer` to obtain one.

        `default` controls what happens if the data does not provide a value for
        this field. If it is the sentinel `no_default`, then a failure is
        generated. If it is the sentinel `empty_default`, then no value for this
        field is given. If it is any other value, then that value is given for
        this field.

        If `hide_default` is `True`, when serializing, if the serialized value
        equals `default`, then the field is omitted from the serialized data.

        If `access` is `read_write`, the field is used when both deserializing
        and serializing. If it is `read_only`, the field is only used when
        serializing. If it is `write_only`, the field is only used when
        deserializing.

        `to_data` determines which serializer is used when serializing to data.
        If this is not provided, then the first serializer in `serializers` is
        used.
        """
        from . import serializer

        cleaned_field_serializers = {}
        for name, field in serializers.items():
            # Serializers can be instances or subclasses of base class Serializer
            if (
                isinstance(field, Serializer)
                or isinstance(field, type)
                and issubclass(field, Serializer)
            ):
                cleaned_field_serializers[name] = field
            else:
                cleaned_field_serializers[name] = serializer(field)

        if to_data is None:
            to_data = next(iter(serializers.keys()))

        super().__init__(default=default, hide_default=hide_default, access=access)
        self.serializers = cleaned_field_serializers
        self.to_data = to_data


class FieldsSerializer(Mapping):
    # Implement mapping so that __fields_serializer__ of a base class can be **kwarg
    # into a subclass

    def __init__(self, **object_field_serializers: FieldsSerializerField | Serializer | Any):
        from . import serializer

        # Raw serializers are wrapped in `SingleField`s,
        # other objects get a lookup for their serializer
        cleaned_object_field_serializers = {}
        for name, field in object_field_serializers.items():
            if isinstance(field, FieldsSerializerField):
                cleaned_object_field_serializers[name] = field
            elif (
                isinstance(field, Serializer)
                or isinstance(field, type)
                and issubclass(field, Serializer)
            ):
                cleaned_object_field_serializers[name] = SingleField(field)
            else:
                cleaned_object_field_serializers[name] = SingleField(serializer(field))

        self.object_field_serializers = cleaned_object_field_serializers

        data_field_deserializers = {}
        data_name_to_object_name = {}
        for object_field_name, field_serializer in self.object_field_serializers.items():
            if isinstance(field_serializer, SingleField):
                if object_field_name in data_field_deserializers:
                    raise ValueError(
                        f"Data field name appears multiple times: {object_field_name}"
                    )
                data_field_deserializers[object_field_name] = field_serializer.serializer
                data_name_to_object_name[object_field_name] = object_field_name
            elif isinstance(field_serializer, MultiField):
                for data_field_name, serializer in field_serializer.serializers.items():
                    if data_field_name in data_field_deserializers:
                        raise ValueError(
                            f"Data field name appears multiple times: {object_field_name}"
                        )
                    data_field_deserializers[data_field_name] = serializer
                    data_name_to_object_name[data_field_name] = object_field_name

        # Mapping of data field name to deserializer.
        # Because of `MultiField`s, there may be legal data fields that are not keys of
        # `self.serializers`. This collects all the possible field names with their associated
        # `Serializer`s.
        self.data_field_deserializers = data_field_deserializers

        # Mapping of each data field name to its object field name.
        # `MultiField`s allow for the data field name to be different from the object field name to
        # which it maps. This provides the mapping from data field name to object field name.
        self.data_name_to_object_name = data_name_to_object_name

    def from_data(self, data: dict[str, Any], *, allow_unused=False) -> DeserializationResult:
        """Deserialize fields from a dictionary.

        Complex objects are usually serialized as a dictionary, where each key
        of the dictionary is an object of a particular type. This function
        performs the following tasks required to deserialize such an object:

        (1) Check that the data is actually a dictionary.
        (2) Check that the keys in the data map to an object field.
            (a) If a field is missing, a default value may be supplied.
            (b) If there are extra keys in the data, this is a failure unless
                `allow_unused` is True
        (3) Run the deserializer for each field.

        This returns either (1) a `DeserializationSuccess` containing a
        dictionary with the same keys as `self.object_field_serializers` but the
        values have been replaced by the deserialized values of deserialized
        fields or (2) a `DeserializationFailure` containing a dictionary with
        the subset of keys from `self.object_field_serializers` whose
        deserializers failed and values containing the deserialization errors.

        If `format` is `"data"`, then the fields of the data are themselves data
        and `from_data` of each field serializer will be used. If `format` is
        `"string"`, then the fields of the data are still in string form and
        `from_string` of each serializer will be used. The former is for typical
        JSON data, while the latter is for query parameters.
        """
        # Return early if the data isn't even a dict
        if not isinstance(data, dict):
            return DeserializationFailure(f"Not a dictionary: {data!r}")

        values = {}
        errors = {}

        # Check that all data fields are valid, that all values are valid,
        # and map data fields to object fields
        for key, value in data.items():
            if (
                key not in self.data_name_to_object_name
                or not self.object_field_serializers[self.data_name_to_object_name[key]].writable
            ):
                # This data field name is not understood
                if not allow_unused:
                    # Fail it
                    errors[key] = "This field is invalid."
                else:
                    # Quietly ignore it
                    pass
            else:
                # This data field maps to an object field
                object_field_name = self.data_name_to_object_name[key]
                if object_field_name in values:
                    # If this object field is already filled, it must have been
                    # filled under a different data field name in the same
                    # MultiField serializer field. Find the data field name
                    # already used and report this field cannot be used as long
                    # as the first one is also used.
                    multi_field = self.object_field_serializers[object_field_name]
                    preexisting_keys = [
                        field_key
                        for field_key in multi_field.serializers.keys()
                        if field_key in data and field_key != key
                    ]
                    errors[key] = (
                        "This field cannot be provided because these fields are already provided: "
                        + ", ".join(preexisting_keys)
                    )
                else:
                    error_or_value = self.data_field_deserializers[key].from_data(value)

                    if isinstance(error_or_value, DeserializationFailure):
                        errors[key] = error_or_value.error

                        # Mark this object field as handled so that an additional error is not
                        # generated
                        values[object_field_name] = None
                    else:
                        values[object_field_name] = error_or_value.value

        # Check that object fields have been created, defaulted, or ignored
        for object_field_name, serializer_field in self.object_field_serializers.items():
            if object_field_name not in values and serializer_field.writable:
                if serializer_field.default is no_default:
                    # This field is required
                    if isinstance(serializer_field, SingleField):
                        errors[object_field_name] = "This field is required."
                    elif isinstance(serializer_field, MultiField):
                        error_message = "One of these fields is required: " + ", ".join(
                            serializer_field.serializers.keys()
                        )
                        errors[object_field_name] = error_message
                    else:
                        raise TypeError(
                            f"Expected FieldsSerializerField, not {type(serializer_field)}"
                        )
                elif serializer_field.default is empty_default:
                    # This field can be ignored
                    pass
                else:
                    # This field has a default value
                    values[object_field_name] = serializer_field.default

        if len(errors) > 0:
            return DeserializationFailure(errors)
        else:
            return DeserializationSuccess(values)

    def to_data(self, values, *, source="dictionary"):
        """Serialize fields to a dictionary.

        For each item in `self.object_field_serializers`, the item in `values`
        with the corresponding key is extracted, its serializer is run, and the
        serialized value is put into the return dictionary.
        """
        data = {}
        for object_field_name, serializer_field in self.object_field_serializers.items():
            if not serializer_field.readable:
                # This field is not serialized
                continue

            if source == "dictionary":
                value = values[object_field_name]
            elif source == "object":
                value = getattr(values, object_field_name)
            else:
                raise ValueError(
                    f"Input argument source must be 'dictionary' or 'object' not {source!r}"
                )

            if (
                serializer_field.hide_default
                and serializer_field.default is not no_default
                and serializer_field.default is not empty_default
                and value == serializer_field.default
            ):
                # Do not serialize the value if it equals the default
                continue

            if isinstance(serializer_field, SingleField):
                serializer = serializer_field.serializer
                data_field_name = object_field_name
            elif isinstance(serializer_field, MultiField):
                serializer = serializer_field.serializers[serializer_field.to_data]
                data_field_name = serializer_field.to_data
            else:
                raise TypeError(f"Expected FieldsSerializerField, not {type(serializer_field)}")

            data[data_field_name] = serializer.to_data(value)

        return data

    def collect_openapi_models(
        self, parent_models: StableSet[Serializer]
    ) -> StableSet[Serializer]:
        models = StableSet()
        for serializer in self.data_field_deserializers.values():
            models |= serializer.collect_openapi_models(parent_models)
        return models

    def to_openapi_schema(self, refs: dict[Serializer, str]) -> dict[str, Any]:
        required = []
        properties = {}
        for name, field in self.object_field_serializers.items():
            if isinstance(field, SingleField):
                property = field.serializer.to_openapi_schema(refs)

                if field.default is not no_default and field.default is not None:
                    # OpenAPI generator 5 crashes if the default is null
                    property["default"] = field.serializer.to_data(field.default)
                else:
                    required.append(name)

                properties[name] = property
            else:
                raise NotImplementedError()

        return {
            "type": "object",
            "required": required,
            "properties": properties,
        }

    def __iter__(self):
        yield from self.object_field_serializers.keys()

    def __getitem__(self, item):
        return self.object_field_serializers[item]

    def __len__(self):
        return len(self.object_field_serializers)

```
src/serialite/_implementations/__init__.py
```.py
from ._boolean import BooleanSerializer
from ._date_time import DateTimeSerializer
from ._dictionary import OrderedDictSerializer, RawDictSerializer
from ._float import FloatSerializer
from ._integer import (
    IntegerSerializer,
    NonnegativeIntegerSerializer,
    PositiveIntegerSerializer,
)
from ._json import JsonSerializer
from ._list import ListSerializer
from ._literal import LiteralSerializer
from ._none import NoneSerializer
from ._path import PathSerializer
from ._reserved import ReservedSerializer
from ._set import SetSerializer
from ._string import StringSerializer
from ._tuple import TupleSerializer
from ._union import OptionalSerializer, TryUnionSerializer
from ._uuid import UuidSerializer

try:
    from ._array import ArraySerializer
except ImportError:
    pass

try:
    from ._ordered_set import OrderedSetSerializer
except ImportError:
    pass

```
src/serialite/_implementations/_array.py
```.py
__all__ = ["ArraySerializer"]

from typing import Generic, TypeVar

import numpy as np

from .._base import Serializer
from .._dispatcher import serializer
from .._result import DeserializationFailure, DeserializationResult, DeserializationSuccess
from .._stable_set import StableSet
from ._list import ListSerializer

Element = TypeVar("Element")


class ArraySerializer(Generic[Element], Serializer[np.ndarray]):
    def __init__(
        self,
        element_serializer: Serializer[Element] | None = None,
        dtype: type[Element] | None = None,
    ):
        if element_serializer is None and dtype is None:
            raise TypeError("Either element_serializer or dtype must be specified.")

        if element_serializer is None:
            element_serializer = serializer(dtype)

        self.list_serializer = ListSerializer(element_serializer)
        self.element_serializer = element_serializer
        self.dtype = dtype

    def from_data(self, data) -> DeserializationResult[np.ndarray]:
        elements = self.list_serializer.from_data(data)

        if isinstance(elements, DeserializationFailure):
            return elements
        else:
            return DeserializationSuccess(np.array(elements.value, dtype=self.dtype))

    def to_data(self, value: np.ndarray):
        if not isinstance(value, np.ndarray):
            raise ValueError(f"Not an array: {value!r}")

        return self.list_serializer.to_data(value.tolist())

    def collect_openapi_models(
        self, parent_models: StableSet[Serializer]
    ) -> StableSet[Serializer]:
        return self.element_serializer.collect_openapi_models(parent_models)

    def to_openapi_schema(self, refs: dict[Serializer, str], force: bool = False):
        return {"type": "array", "items": self.element_serializer.to_openapi_schema(refs)}

```
src/serialite/_implementations/_boolean.py
```.py
__all__ = ["BooleanSerializer"]

from .._base import Serializer
from .._result import DeserializationFailure, DeserializationResult, DeserializationSuccess


class BooleanSerializer(Serializer[bool]):
    def from_data(self, data) -> DeserializationResult[bool]:
        if isinstance(data, bool):
            return DeserializationSuccess(data)
        else:
            return DeserializationFailure(f"Not a valid boolean: {data!r}")

    def to_data(self, value: bool):
        if not isinstance(value, bool):
            raise ValueError(f"Not an bool: {value!r}")
        return value

    def to_openapi_schema(self, refs: dict[Serializer, str], force: bool = False):
        return {"type": "boolean"}

```
src/serialite/_implementations/_date_time.py
```.py
__all__ = ["DateTimeSerializer"]

from datetime import datetime

from .._base import Serializer
from .._result import DeserializationFailure, DeserializationResult, DeserializationSuccess


class DateTimeSerializer(Serializer[datetime]):
    def from_data(self, data) -> DeserializationResult[datetime]:
        if isinstance(data, str):
            if data.endswith("Z"):
                # Python does not handle the terminal "Z"
                # https://github.com/python/cpython/issues/80010
                sanitized_data = data[:-1] + "+00:00"
            else:
                sanitized_data = data
            try:
                value = datetime.fromisoformat(sanitized_data)
            except ValueError:
                return DeserializationFailure(f"Not a valid DateTime: {data!r}")
            else:
                return DeserializationSuccess(value)
        else:
            return DeserializationFailure(f"Not a valid DateTime: {data!r}")

    def to_data(self, value):
        if not isinstance(value, datetime):
            raise ValueError(f"Not a DateTime: {value!r}")
        return value.isoformat(sep=" ")

    def to_openapi_schema(self, refs: dict[Serializer, str], force: bool = False):
        return {"type": "string", "format": "date-time"}

```
src/serialite/_implementations/_dictionary.py
```.py
__all__ = ["OrderedDictSerializer", "RawDictSerializer"]

from collections import OrderedDict
from typing import Generic, TypeVar

from .._base import Serializer
from .._result import DeserializationFailure, DeserializationResult, DeserializationSuccess
from .._stable_set import StableSet
from ._string import StringSerializer

Key = TypeVar("Key")
Value = TypeVar("Value")


class OrderedDictSerializer(Generic[Key, Value], Serializer[dict[Key, Value]]):
    """Serializing a dictionary as a list of entries.

    The fields of a JSON object is inherently unordered. Also, the keys cannot
    be anything except strings. If retaining the order of a dictionary is
    desired or allowing a key other than a string is required, this serializer
    can be used. It is represented as a JSON list (which is ordered) or
    2-element lists, where the first element is the key and the second element
    is the value.
    """

    def __init__(self, key_serializer: Serializer[Key], value_serializer: Serializer[Value]):
        self.key_serializer = key_serializer
        self.value_serializer = value_serializer

    def from_data(self, data) -> DeserializationResult[dict[Key, Value]]:
        # Return early if the data isn't even a list
        if not isinstance(data, list):
            return DeserializationFailure(f"Not a valid list: {data!r}")

        # Validate keys first, so that errors in values can be better formatted
        errors = {}
        keys = []
        for i, item in enumerate(data):
            if not isinstance(item, (list, tuple)) or len(item) != 2:
                errors[str(i)] = f"Not a valid length-2 list: {item!r}"
            else:
                value_or_error = self.key_serializer.from_data(item[0])
                if isinstance(value_or_error, DeserializationFailure):
                    errors[str(i)] = value_or_error.error
                else:
                    keys.append(value_or_error.value)

        if len(errors) > 0:
            return DeserializationFailure(errors)

        # Validate values, including the key in errors to help identify the location of the failure
        errors = {}
        values = []
        for i, item in enumerate(data):
            value_or_error = self.value_serializer.from_data(item[1])
            if isinstance(value_or_error, DeserializationFailure):
                errors[str(keys[i])] = value_or_error.error
            else:
                values.append((keys[i], value_or_error.value))

        if len(errors) > 0:
            return DeserializationFailure(errors)
        else:
            return DeserializationSuccess(OrderedDict(values))

    def to_data(self, value: dict[Key, Value]):
        if not isinstance(value, dict):
            raise ValueError(f"Not an dict: {value!r}")

        return [
            [self.key_serializer.to_data(key), self.value_serializer.to_data(value)]
            for key, value in value.items()
        ]


class RawDictSerializer(Generic[Value], Serializer[dict[str, Value]]):
    """Serializing a dictionary to a dictionary rather than a list of tuples.

    OpenAPI does not understand tuples and therefore cannot capture the
    definition of an ordered dictionary as given by `OrderedDictSerializer`.
    `RawDictSerializer` can be used to serialize dictionaries when the key is a
    string and order is unimportant and a type that is understood by OpenAPI is
    important.
    """

    def __init__(
        self,
        value_serializer: Serializer[Value],
        *,
        key_serializer: Serializer[str] = StringSerializer(),  # noqa: B008
    ):
        self.value_serializer = value_serializer
        self.key_serializer = key_serializer

    def from_data(self, data) -> DeserializationResult[dict[str, Value]]:
        # Return early if the data isn't even a dict
        if not isinstance(data, dict):
            return DeserializationFailure(f"Not a valid dict: {data!r}")

        # Validate keys and values
        # Include the key in errors to help identify the location of the failure
        errors = {}
        values = {}
        for key, value in data.items():
            key_or_error = self.key_serializer.from_data(key)
            if isinstance(key_or_error, DeserializationFailure):
                errors[key] = key_or_error.error
                continue
            else:
                output_key = key_or_error.value

            value_or_error = self.value_serializer.from_data(value)
            if isinstance(value_or_error, DeserializationFailure):
                # Use original keys for errors
                errors[key] = value_or_error.error
            else:
                # Use deserialized keys for values
                values[output_key] = value_or_error.value

        if len(errors) > 0:
            return DeserializationFailure(errors)
        else:
            return DeserializationSuccess(values)

    def to_data(self, value: dict[str, Value]):
        if not isinstance(value, dict):
            raise ValueError(f"Not an dict: {value!r}")

        return {
            self.key_serializer.to_data(key): self.value_serializer.to_data(value)
            for key, value in value.items()
        }

    def collect_openapi_models(
        self, parent_models: StableSet[Serializer]
    ) -> StableSet[Serializer]:
        return self.value_serializer.collect_openapi_models(parent_models)

    def to_openapi_schema(self, refs: dict[Serializer, str], force: bool = False):
        return {
            "type": "object",
            "additionalProperties": self.value_serializer.to_openapi_schema(refs),
        }

```
src/serialite/_implementations/_float.py
```.py
__all__ = ["FloatSerializer"]

from math import inf, isnan, nan
from typing import Any, Sequence

from .._base import Serializer
from .._numeric_check import is_real
from .._result import DeserializationFailure, DeserializationResult, DeserializationSuccess


class FloatSerializer(Serializer[float]):
    def __init__(
        self,
        nan_values: Sequence[Any] = (nan,),
        inf_values: Sequence[Any] = (inf,),
        neg_inf_values: Sequence[Any] = (-inf,),
    ):
        self.nan_values = nan_values
        self.inf_values = inf_values
        self.neg_inf_values = neg_inf_values

    def from_data(self, data) -> DeserializationResult[float]:
        if data in self.nan_values:
            return DeserializationSuccess(nan)
        elif data in self.inf_values:
            return DeserializationSuccess(inf)
        elif data in self.neg_inf_values:
            return DeserializationSuccess(-inf)
        elif is_real(data):
            return DeserializationSuccess(float(data))
        else:
            return DeserializationFailure(f"Not a valid float: {data!r}")

    def to_data(self, value: float):
        if not is_real(value):
            raise ValueError(f"Not a float: {value!r}")

        if isnan(value):
            return self.nan_values[0]
        elif value == inf:
            return self.inf_values[0]
        elif value == -inf:
            return self.neg_inf_values[0]
        else:
            return float(value)

    def to_openapi_schema(self, refs: dict[Serializer, str], force: bool = False):
        return {"type": "number"}

```
src/serialite/_implementations/_integer.py
```.py
__all__ = ["IntegerSerializer", "NonnegativeIntegerSerializer", "PositiveIntegerSerializer"]

from .._base import Serializer
from .._numeric_check import is_int
from .._result import DeserializationFailure, DeserializationResult, DeserializationSuccess


class IntegerSerializer(Serializer[int]):
    def from_data(self, data) -> DeserializationResult[int]:
        if isinstance(data, int):
            return DeserializationSuccess(data)
        else:
            return DeserializationFailure(f"Not a valid integer: {data!r}")

    def to_data(self, value: int):
        if not isinstance(value, int):
            raise ValueError(f"Not an int: {value!r}")
        return value

    def to_openapi_schema(self, refs: dict[Serializer, str], force: bool = False):
        return {"type": "integer"}


class NonnegativeIntegerSerializer(Serializer[int]):
    def from_data(self, data) -> DeserializationResult[int]:
        if is_int(data) and data >= 0:
            return DeserializationSuccess(data)
        else:
            return DeserializationFailure(f"Not a valid nonnegative integer: {data!r}")

    def to_data(self, value: int):
        if not is_int(value) or value < 0:
            raise ValueError(f"Not an nonnegative int: {value!r}")
        return value

    def to_openapi_schema(self, refs: dict[Serializer, str], force: bool = False):
        return {"type": "integer", "minimum": 0}


class PositiveIntegerSerializer(Serializer[int]):
    def from_data(self, data) -> DeserializationResult[int]:
        if is_int(data) and data > 0:
            return DeserializationSuccess(data)
        else:
            return DeserializationFailure(f"Not a valid positive integer: {data!r}")

    def to_data(self, value: int):
        if not is_int(value) or value <= 0:
            raise ValueError(f"Not an positive int: {value!r}")
        return value

    def to_openapi_schema(self, refs: dict[Serializer, str], force: bool = False):
        return {"type": "integer", "minimum": 1}

```
src/serialite/_implementations/_json.py
```.py
__all__ = ["JsonSerializer"]

from typing import Any

from .._base import Serializer
from .._result import DeserializationResult, DeserializationSuccess


class JsonSerializer(Serializer[Any]):
    """Serializer for any valid JSON object.

    By definition, the data is already valid JSON, so `from_data` and `to_data`
    merely return their inputs.
    """

    def from_data(self, data) -> DeserializationResult[Any]:
        return DeserializationSuccess(data)

    def to_data(self, value: Any):
        return value

```
src/serialite/_implementations/_list.py
```.py
__all__ = ["ListSerializer"]

from typing import Generic, TypeVar

from .._base import Serializer
from .._result import DeserializationFailure, DeserializationResult, DeserializationSuccess
from .._stable_set import StableSet

Element = TypeVar("Element")

try:
    from numpy import ndarray
except ImportError:
    # Class that will never pass an isinstance check
    class ndarray:  # noqa: N801
        pass


class ListSerializer(Generic[Element], Serializer[list[Element]]):
    def __init__(self, element_serializer: Serializer[Element]):
        self.element_serializer = element_serializer

    def from_data(self, data) -> DeserializationResult[list[Element]]:
        # Return early if the data isn't even a list
        if not isinstance(data, list):
            return DeserializationFailure(f"Not a valid list: {data!r}")

        # Validate values
        errors = {}
        values = []
        for i, value in enumerate(data):
            value_or_error = self.element_serializer.from_data(value)
            if isinstance(value_or_error, DeserializationFailure):
                errors[str(i)] = value_or_error.error
            else:
                values.append(value_or_error.value)

        if len(errors) > 0:
            return DeserializationFailure(errors)
        else:
            return DeserializationSuccess(values)

    def to_data(self, value: list[Element]):
        # Accept an ndarray also for ergonomics
        if not isinstance(value, (list, ndarray)):
            raise ValueError(f"Not a list: {value!r}")

        return [self.element_serializer.to_data(item) for item in value]

    def collect_openapi_models(
        self, parent_models: StableSet[Serializer]
    ) -> StableSet[Serializer]:
        return self.element_serializer.collect_openapi_models(parent_models)

    def to_openapi_schema(self, refs: dict[Serializer, str], force: bool = False):
        return {"type": "array", "items": self.element_serializer.to_openapi_schema(refs)}

```
src/serialite/_implementations/_literal.py
```.py
__all__ = ["LiteralSerializer"]

from .._base import Serializer
from .._numeric_check import is_int, is_real
from .._result import DeserializationFailure, DeserializationSuccess


class LiteralSerializer(Serializer):
    def __init__(self, *possibilities):
        self.possibilities = possibilities

    def from_data(self, data):
        if data in self.possibilities:
            return DeserializationSuccess(data)
        else:
            return DeserializationFailure(f"Not one of {list(self.possibilities)!r}: {data!r}")

    def to_data(self, value):
        if value not in self.possibilities:
            raise ValueError(f"Not one of {list(self.possibilities)!r}: {value!r}")

        return value

    def to_openapi_schema(self, refs: dict[Serializer, str], force: bool = False):
        if all(isinstance(x, str) for x in self.possibilities):
            return {"type": "string", "enum": self.possibilities}
        elif all(is_int(x) for x in self.possibilities):
            return {"type": "integer", "enum": self.possibilities}
        elif all(is_real(x) for x in self.possibilities):
            return {"type": "number", "enum": self.possibilities}
        else:
            return {"enum": self.possibilities}

```
src/serialite/_implementations/_none.py
```.py
__all__ = ["NoneSerializer"]

from .._base import Serializer
from .._result import DeserializationFailure, DeserializationSuccess


class NoneSerializer(Serializer[None]):
    def from_data(self, data):
        if data is None:
            return DeserializationSuccess(None)
        else:
            return DeserializationFailure(f"Not a null: {data!r}")

    def to_data(self, value: None):
        if value is not None:
            raise ValueError(f"Not an None: {value!r}")
        return value

    def to_openapi_schema(self, refs: dict[Serializer, str], force: bool = False):
        return {"nullable": True}

```
src/serialite/_implementations/_ordered_set.py
```.py
__all__ = ["OrderedSetSerializer"]


from typing import Generic, TypeVar

from ordered_set import OrderedSet

from .._base import Serializer
from .._result import DeserializationFailure, DeserializationResult, DeserializationSuccess
from .._stable_set import StableSet

Element = TypeVar("Element")


class OrderedSetSerializer(Generic[Element], Serializer[OrderedSet[Element]]):
    def __init__(self, element_serializer: Serializer[Element]):
        self.element_serializer = element_serializer

    def from_data(self, data) -> DeserializationResult[OrderedSet[Element]]:
        # Return early if the data isn't even a list
        if not isinstance(data, list):
            return DeserializationFailure(f"Not a valid list: {data!r}")

        # Validate values
        errors = {}
        values = OrderedSet()
        for i, value in enumerate(data):
            value_or_error = self.element_serializer.from_data(value)
            if isinstance(value_or_error, DeserializationFailure):
                errors[str(i)] = value_or_error.error
            elif value_or_error.value in values:
                errors[str(i)] = (
                    f"Duplicated value found: {value_or_error.value!r}. "
                    "Expected a list of unique values."
                )
            else:
                values.add(value_or_error.value)

        if len(errors) > 0:
            return DeserializationFailure(errors)
        else:
            return DeserializationSuccess(values)

    def to_data(self, value: OrderedSet[Element]):
        if not isinstance(value, OrderedSet):
            raise ValueError(f"Not an OrderedSet: {value!r}")

        return [self.element_serializer.to_data(item) for item in value]

    def collect_openapi_models(
        self, parent_models: StableSet[Serializer]
    ) -> StableSet[Serializer]:
        return self.element_serializer.collect_openapi_models(parent_models)

    def to_openapi_schema(self, refs: dict[Serializer, str], force: bool = False):
        return {"type": "array", "items": self.element_serializer.to_openapi_schema(refs)}

```
src/serialite/_implementations/_path.py
```.py
__all__ = ["PathSerializer"]

from pathlib import Path

from .._base import Serializer
from .._result import DeserializationFailure, DeserializationResult, DeserializationSuccess
from ._string import StringSerializer


class PathSerializer(Serializer):
    def from_data(self, data) -> DeserializationResult:
        path_or_error = StringSerializer().from_data(data)

        if isinstance(path_or_error, DeserializationFailure):
            return path_or_error
        else:
            path = path_or_error.or_die()

            return DeserializationSuccess(Path(path))

    def to_data(self, value):
        return value.as_posix()

```
src/serialite/_implementations/_reserved.py
```.py
__all__ = ["ReservedSerializer"]

from collections.abc import Set
from typing import Generic, TypeVar

from .._base import Serializer
from .._result import DeserializationFailure, DeserializationResult
from .._stable_set import StableSet

Element = TypeVar("Element")


class ReservedSerializer(Generic[Element], Serializer[Element]):
    def __init__(self, internal_serializer: Serializer[Element], *, reserved: Set[Element]):
        self.internal_serializer = internal_serializer
        self.reserved = reserved

    def from_data(self, data) -> DeserializationResult[Element]:
        result = self.internal_serializer.from_data(data)

        if isinstance(result, DeserializationFailure):
            return result
        elif result.value in self.reserved:
            return DeserializationFailure(f"Reserved value: {result.value!r}")
        else:
            return result

    def to_data(self, value):
        if value in self.reserved:
            raise ValueError(f"Reserved value: {value}")

        return self.internal_serializer.to_data(value)

    def collect_openapi_models(
        self, parent_models: StableSet[Serializer]
    ) -> StableSet[Serializer]:
        return self.internal_serializer.collect_openapi_models(parent_models)

    def to_openapi_schema(self, refs: dict[Serializer, str], force: bool = False):
        return self.internal_serializer.to_openapi_schema(refs)

```
src/serialite/_implementations/_set.py
```.py
__all__ = ["SetSerializer"]


from typing import Generic, TypeVar

from .._base import Serializer
from .._result import DeserializationFailure, DeserializationResult, DeserializationSuccess
from .._stable_set import StableSet

Element = TypeVar("Element")


class SetSerializer(Generic[Element], Serializer[set[Element]]):
    def __init__(self, element_serializer: Serializer[Element]):
        self.element_serializer = element_serializer

    def from_data(self, data) -> DeserializationResult[set[Element]]:
        # Return early if the data isn't even a list
        if not isinstance(data, list):
            return DeserializationFailure(f"Not a valid list: {data!r}")

        # Validate values
        errors = {}
        values = set()
        for i, value in enumerate(data):
            value_or_error = self.element_serializer.from_data(value)
            if isinstance(value_or_error, DeserializationFailure):
                errors[str(i)] = value_or_error.error
            elif value_or_error.value in values:
                errors[str(i)] = (
                    f"Duplicated value found: {value_or_error.value!r}. "
                    "Expected a list of unique values."
                )
            else:
                values.add(value_or_error.value)

        if len(errors) > 0:
            return DeserializationFailure(errors)
        else:
            return DeserializationSuccess(values)

    def to_data(self, value: set[Element]):
        if not isinstance(value, set):
            raise ValueError(f"Not a set: {value!r}")

        return [self.element_serializer.to_data(item) for item in value]

    def collect_openapi_models(
        self, parent_models: StableSet[Serializer]
    ) -> StableSet[Serializer]:
        return self.element_serializer.collect_openapi_models(parent_models)

    def to_openapi_schema(self, refs: dict[Serializer, str], force: bool = False):
        return {"type": "array", "items": self.element_serializer.to_openapi_schema(refs)}

```
src/serialite/_implementations/_string.py
```.py
__all__ = ["StringSerializer"]

import re

from .._base import Serializer
from .._result import DeserializationFailure, DeserializationResult, DeserializationSuccess


class StringSerializer(Serializer[str]):
    def __init__(self, accept: str | None = None):
        self.accept = accept
        self.accept_regex = re.compile(accept) if accept is not None else None

    def from_data(self, data) -> DeserializationResult[str]:
        if isinstance(data, str):
            if self.accept is None or self.accept_regex.fullmatch(data):
                return DeserializationSuccess(data)
            else:
                return DeserializationFailure(f"Does not match regex r'{self.accept}': {data!r}")
        else:
            return DeserializationFailure(f"Not a valid string: {data!r}")

    def to_data(self, value: str):
        if not isinstance(value, str):
            raise ValueError(f"Not a string: {value!r}")
        if self.accept is not None and not self.accept_regex.fullmatch(value):
            raise ValueError(f"Does not match regex r'{self.accept}': {value!r}")
        return value

    def to_openapi_schema(self, refs: dict[Serializer, str], force: bool = False):
        return {"type": "string"}

```
src/serialite/_implementations/_tuple.py
```.py
__all__ = ["TupleSerializer"]

from typing import Generic
from typing_extensions import TypeVarTuple, Unpack

from .._base import Serializer
from .._result import DeserializationFailure, DeserializationResult, DeserializationSuccess
from .._stable_set import StableSet

TupleArguments = TypeVarTuple("TupleArguments")

try:
    from numpy import ndarray
except ImportError:
    # Class that will never pass an isinstance check
    class ndarray:  # noqa: N801
        pass


class TupleSerializer(Generic[Unpack[TupleArguments]], Serializer[tuple[Unpack[TupleArguments]]]):
    def __init__(self, *element_serializers: Unpack[TupleArguments]):
        self.element_serializers = element_serializers

    def from_data(self, data) -> DeserializationResult[tuple[Unpack[TupleArguments]]]:
        # Return early if the data isn't even a list
        if not isinstance(data, list):
            return DeserializationFailure(f"Not a valid list: {data!r}")

        # Return early if the list is not the correct length
        if len(data) != len(self.element_serializers):
            return DeserializationFailure(
                f"Has {len(data)} elements, not {len(self.element_serializers)}: {data!r}"
            )

        # Validate values
        errors = {}
        values = []
        for i, (item, serializer) in enumerate(zip(data, self.element_serializers)):
            value_or_error = serializer.from_data(item)
            if isinstance(value_or_error, DeserializationFailure):
                errors[str(i)] = value_or_error.error
            else:
                values.append(value_or_error.value)

        if len(errors) > 0:
            return DeserializationFailure(errors)
        else:
            return DeserializationSuccess(tuple(values))

    def to_data(self, value: tuple[Unpack[TupleArguments]]):
        # Accept an ndarray or list for ergonomics
        if not isinstance(value, (tuple, list, ndarray)):
            raise ValueError(f"Not a tuple: {value!r}")
        if len(value) != len(self.element_serializers):
            raise ValueError(
                f"Has {len(value)} elements, not {len(self.element_serializers)}: {value}"
            )

        return [
            serializer.to_data(item) for item, serializer in zip(value, self.element_serializers)
        ]

    def collect_openapi_models(
        self, parent_models: StableSet[Serializer]
    ) -> StableSet[Serializer]:
        models = StableSet()
        for serializer in self.element_serializers:
            models |= serializer.collect_openapi_models(parent_models)
        return models

    def to_openapi_schema(self, refs: dict[Serializer, str], force: bool = False):
        n = len(self.element_serializers)
        return {
            "type": "array",
            "prefixItems": [
                serializer.to_openapi_schema(refs) for serializer in self.element_serializers
            ],
            "minItems": n,
            "maxItems": n,
        }

```
src/serialite/_implementations/_union.py
```.py
__all__ = ["TryUnionSerializer", "OptionalSerializer"]

from typing import Generic, TypeVar

from .._base import Serializer
from .._result import DeserializationFailure, DeserializationResult, DeserializationSuccess
from .._stable_set import StableSet

Element = TypeVar("Element")


class TryUnionSerializer(Serializer):
    def __init__(self, *serializers: Serializer):
        self.serializers = serializers

    def from_data(self, data):
        # Try each possibility and return the first value that succeeds,
        # otherwise return both errors
        errors = {}
        for serializer in self.serializers:
            value_or_error = serializer.from_data(data)
            if isinstance(value_or_error, DeserializationSuccess):
                return value_or_error
            else:
                errors[str(serializer)] = value_or_error.error

        return DeserializationFailure(errors)

    def to_data(self, value):
        # Try each possibility. It should not be possible for both to fail.
        errors = []
        for serializer in self.serializers:
            try:
                return serializer.to_data(value)
            except Exception as e:
                errors.append(e)

        raise ValueError(
            "All available serializers failed: " + ", ".join(map(str, self.serializers)), errors
        )

    def collect_openapi_models(
        self, parent_models: StableSet[Serializer]
    ) -> StableSet[Serializer]:
        models = StableSet()
        for serializer in self.serializers:
            models |= serializer.collect_openapi_models(parent_models)
        return models

    def to_openapi_schema(self, refs: dict[Serializer, str], force: bool = False):
        return {
            "oneOf": [serializer.to_openapi_schema(refs) for serializer in self.serializers],
        }


class OptionalSerializer(Generic[Element], Serializer[Element | None]):
    def __init__(self, element_serializer: Serializer[Element]):
        self.element_serializer = element_serializer

    def from_data(self, data) -> DeserializationResult[Element | None]:
        if data is None:
            return DeserializationSuccess(None)
        else:
            return self.element_serializer.from_data(data)

    def to_data(self, value: Element | None):
        if value is None:
            return None
        else:
            return self.element_serializer.to_data(value)

    def collect_openapi_models(
        self, parent_models: StableSet[Serializer]
    ) -> StableSet[Serializer]:
        return self.element_serializer.collect_openapi_models(parent_models)

    def to_openapi_schema(self, refs: dict[Serializer, str], force: bool = False):
        return self.element_serializer.to_openapi_schema(refs) | {"nullable": True}

```
src/serialite/_implementations/_uuid.py
```.py
__all__ = ["UuidSerializer"]

from uuid import UUID

from .._base import Serializer
from .._result import DeserializationFailure, DeserializationResult, DeserializationSuccess


class UuidSerializer(Serializer[UUID]):
    def from_data(self, data) -> DeserializationResult[UUID]:
        if isinstance(data, str):
            try:
                value = UUID(data)
            except Exception:
                return DeserializationFailure(f"Not a valid UUID: {data!r}")
            else:
                return DeserializationSuccess(value)
        else:
            return DeserializationFailure(f"Not a valid UUID: {data!r}")

    def to_data(self, value: UUID):
        if not isinstance(value, UUID):
            raise ValueError(f"Not a UUID: {value!r}")
        return str(value)

    def to_openapi_schema(self, refs: dict[Serializer, str], force: bool = False):
        return {"type": "string", "format": "uuid"}

```
src/serialite/_mixins.py
```.py
__all__ = ["SerializableMixin", "AbstractSerializableMixin"]

from typing import ClassVar

from ._base import Serializable, Serializer
from ._fields_serializer import FieldsSerializer
from ._result import DeserializationFailure, DeserializationSuccess
from ._stable_set import StableSet


class SerializableMixin(Serializable):
    """A mixin to make simple classes serializable.

    This mixin inspects an abstract `__fields_serializer__` to provide an
    implementation for `Serializable`.
    """

    __fields_serializer__: ClassVar[FieldsSerializer]

    @classmethod
    def from_data(cls, data):
        value_or_error = cls.__fields_serializer__.from_data(data)

        if isinstance(value_or_error, DeserializationFailure):
            return value_or_error
        else:
            return DeserializationSuccess(cls(**value_or_error.value))

    def to_data(self):
        return self.__fields_serializer__.to_data(self, source="object")

    @classmethod
    def collect_openapi_models(cls, parent_models: StableSet[Serializer]) -> StableSet[Serializer]:
        # Every class that uses AbstractSerializableMixin gets put into the OpenAPI models.
        if cls not in parent_models:
            this_set = StableSet(cls)
            parent_models |= this_set
            return this_set | cls.__fields_serializer__.collect_openapi_models(parent_models)

    @classmethod
    def to_openapi_schema(cls, refs: dict[Serializer, str], force: bool = False):
        if force or cls not in refs:
            schema = cls.__fields_serializer__.to_openapi_schema(refs)

            if hasattr(cls, "__subclass_serializers__"):
                # It is not possible in OpenAPI to have the discriminator field
                # only in places where the base class is expected (that is,
                # where it is needed), so we have to say that it is accepted for
                # the subclass, even though it is not. This works as long as no
                # place in the API accepts just a concrete class.

                discriminator_field = {"_type": {"type": "string", "enum": [cls.__name__]}}
                schema = schema | {"properties": discriminator_field | schema["properties"]}

            return schema
        else:
            return refs[cls]


class AbstractSerializableMixin(Serializable):
    """Provides Serializable for abstract base classes.

    This mixin inspects an abstract `__subclass_serializers__` to provide an
    implementation for `Serializable`.

    This provides a standard way to serialize instances of an abstract base
    class. The concrete classes must be `Serializable`; that is, they have
    their own implementation of `from_data` and `to_data` for serializing and
    deserializing instances of themselves. The concrete classes must also
    deserialize from and serialize to a dictionary. This is important because
    `to_data` of this mixin will add the key "_type" to the dictionary
    containing the name of the subclass. Likewise, `from_data` of this mixin
    will look for the key "_type" to determine which subclass to dispatch the
    remainder of the dictionary to.
    """

    __subclass_serializers__: ClassVar[dict[str, Serializable]]

    @classmethod
    def from_data(cls, data):
        try:
            type_name = data["_type"]
        except KeyError:
            return DeserializationFailure({"_type": "This field is required."})
        except TypeError:
            return DeserializationFailure(f"Not a dictionary: {data!r}")

        # The rest of data
        subclass_data = {key: value for key, value in data.items() if key != "_type"}

        subclass = cls.__subclass_serializers__.get(type_name)
        if subclass is None:
            return DeserializationFailure({"_type": f"Class not found: {type_name!r}"})
        else:
            return subclass.from_data(subclass_data)

    @classmethod
    def to_data(cls, value):
        if not isinstance(value, cls):
            raise TypeError(f"Expected instance of {cls}, but got {value}")

        if value.to_data == cls.to_data:
            raise TypeError(
                "Recursion in AbstractSerializableMixin.to_data detected while processing"
                f" {value}.This likely do to a failure to implement to_data on {type(value)}"
            )

        return {"_type": value.__class__.__name__} | value.to_data()

    @classmethod
    def collect_openapi_models(cls, parent_models: StableSet[Serializer]) -> StableSet[Serializer]:
        # Every class that uses AbstractSerializableMixin gets put into the OpenAPI models.
        if cls not in parent_models:
            this_set = StableSet(cls)
            parent_models |= this_set
            models = StableSet()
            for subclass in cls.__subclass_serializers__.values():
                models |= subclass.collect_openapi_models(parent_models)
            return this_set | models
        else:
            return StableSet()

    @classmethod
    def to_openapi_schema(cls, refs: dict[Serializer, str], force: bool = False):
        if force or cls not in refs:
            return {
                "type": "object",
                "discriminator": {"propertyName": "_type"},
                "oneOf": [
                    subclass.to_openapi_schema(refs)
                    for subclass in cls.__subclass_serializers__.values()
                ],
            }
        else:
            return refs[cls]

```
src/serialite/_monkey_patches.py
```.py
from __future__ import annotations

__all__ = [
    "monkey_patch_pydantic_subclasscheck",
    "monkey_patch_pydantic_instancecheck",
    "monkey_patch_fastapi_create_cloned_field",
    "monkey_patch_pydantic_get_flat_models_from_model",
    "monkey_patch_pydantic_model_type_schema",
]

from typing import TYPE_CHECKING, Any

from ._stable_set import StableSet

if TYPE_CHECKING:
    from pydantic import BaseModel
    from pydantic.fields import ModelField
    from pydantic.schema import TypeModelOrEnum, TypeModelSet


def __subclasscheck__(cls: type, sub: type) -> bool:  # noqa: N807
    from pydantic import BaseModel

    if cls is BaseModel and hasattr(sub, "_is_pydantic_base_model"):
        # To minimize the blast radius, only change how subclassing works on
        # exactly BaseModel. Hypothetical subtypes of BaseModel will not be
        # affected by this method.
        return sub._is_pydantic_base_model
    else:
        return super(type(BaseModel), cls).__subclasscheck__(sub)


def monkey_patch_pydantic_subclasscheck() -> None:
    # Pydantic and FastAPI make extensive use of issubclass(cls, BaseModel).
    # To implement a Pydantic interface, it is not enough to duck type the key
    # methods. The call to issubclass must be intercepted and rewritten.
    # Fortunately, BaseModel has its own metaclass, so we can attach a new
    # definition of __subclasscheck__ to it that will cause
    # issubclass(cls, BaseModel) to return the value of _is_pydantic_base_model
    # if it exists. We cannot look for __get_validators__ because some non-Base
    # Model classes in Pydantic have this method and FastAPI treats them very
    # differently.

    try:
        from pydantic import BaseModel
    except ImportError:
        pass
    else:
        metaclass = type(BaseModel)
        metaclass.__subclasscheck__ = __subclasscheck__


def __instancecheck__(cls: type, instance: Any) -> bool:  # noqa: N807
    from pydantic import BaseModel

    if cls is BaseModel and hasattr(instance, "_is_pydantic_base_model"):
        # To minimize the blast radius, only change how isinstance works on
        # exactly BaseModel. Hypothetical subtypes of BaseModel will not be
        # affected by this method.
        return instance._is_pydantic_base_model
    else:
        return super(type(BaseModel), cls).__instancecheck__(instance)


def monkey_patch_pydantic_instancecheck() -> None:
    # Pydantic and FastAPI also make extensive use of
    # isinstance(obj, BaseModel). We need to patch __instancecheck__ using the
    # same process for the same reasons. Normally, __instancecheck__ calls
    # __subclasscheck__, but Pydantic overrode the default behavior in order to
    # work around a Python bug.
    # https://github.com/samuelcolvin/pydantic/pull/4081

    try:
        from pydantic import BaseModel
    except ImportError:
        pass
    else:
        metaclass = type(BaseModel)
        metaclass.__instancecheck__ = __instancecheck__


def monkey_patch_fastapi_create_cloned_field() -> None:
    # To work around a misfeature in Pydantic, FastAPI clones every
    # Pydantic class that it receives. This breaks Serialite's
    # AbstractSerializableMixin because the cloned abstract serializer now has
    # no subclasses. The function that does the cloning is monkey patched to
    # simply pass Serialite classes through without modification.

    try:
        from fastapi import routing, utils
        from fastapi.utils import create_cloned_field as original_create_cloned_field
    except ImportError:
        pass
    else:

        def create_cloned_field(
            field: ModelField,
            *,
            cloned_types: dict[type[BaseModel], type[BaseModel]] | None = None,
        ):
            original_type = field.type_
            if hasattr(original_type, "to_data"):
                return field
            else:
                return original_create_cloned_field(field, cloned_types=cloned_types)

        utils.create_cloned_field = create_cloned_field
        routing.create_cloned_field = create_cloned_field


def monkey_patch_pydantic_get_flat_models_from_model() -> None:
    # Just like Serialite, Pydantic collects all the models by traversing the
    # models it already has. It is cleaner to let Serialite do its own traversal
    # by monkey patching pydantic.schema.get_flat_models_from_model to intercept
    # Serialite classes.

    try:
        from pydantic import schema
        from pydantic.schema import (
            get_flat_models_from_model as original_get_flat_models_from_model,
        )
    except ImportError:
        pass
    else:

        def get_flat_models_from_model(
            model: type[BaseModel], known_models: TypeModelSet = None
        ) -> TypeModelSet:
            if hasattr(model, "collect_openapi_models"):
                if known_models is None:
                    known_models = StableSet()

                new_models = model.collect_openapi_models(StableSet())

                return known_models | new_models
            else:
                return original_get_flat_models_from_model(model, known_models)

        schema.get_flat_models_from_model = get_flat_models_from_model


def monkey_patch_pydantic_model_type_schema() -> None:
    # Just like Serialite, Pydantic takes all the models it found and generates
    # the schema for each one using references where appropriate. It does not
    # use the .schema method, but the model_type_schema function instead. It is
    # cleaner to intercept Serialite classes passed to this function.

    try:
        from pydantic import schema
        from pydantic.schema import model_type_schema as original_model_type_schema
    except ImportError:
        pass
    else:

        def model_type_schema(
            model: type[BaseModel],
            *,
            by_alias: bool,
            model_name_map: dict[TypeModelOrEnum, str],
            ref_template: str,
            ref_prefix: str | None = None,
            known_models: TypeModelSet,
        ) -> tuple[dict[str, Any], dict[str, Any], set[str]]:
            if ref_template is None:
                from pydantic.schema import default_ref_template

                ref_template = default_ref_template

            if hasattr(model, "to_openapi_schema"):
                if ref_prefix is None:
                    ref_prefix = "#/definitions/"

                refs = {
                    model: {"$ref": ref_prefix + name} for model, name in model_name_map.items()
                }

                # For inexplicable reasons, Pydantic requires that all the
                # definitions of sub models need to be returned right now.
                models = model.collect_openapi_models(StableSet())

                definitions = {
                    model.__name__: model.to_openapi_schema(refs, force=True) for model in models
                }

                return model.to_openapi_schema(refs, force=True), definitions, models
            else:
                return original_model_type_schema(
                    model,
                    by_alias=by_alias,
                    model_name_map=model_name_map,
                    ref_prefix=ref_prefix,
                    ref_template=ref_template,
                    known_models=known_models,
                )

        schema.model_type_schema = model_type_schema

```
src/serialite/_numeric_check.py
```.py
__all__ = ["is_int", "is_real"]

from numbers import Real


def is_int(value):
    """Tests if a value is of type int.

    This behaves exactly like isinstance(value, int) except that bool is
    specifically excluded. In Python, bool is a proper subclass of int.
    """
    return isinstance(value, int) and not isinstance(value, bool)


def is_real(value):
    """Tests if a value is of type Real.

    This behaves exactly like isinstance(value, Real) except that bool is
    specifically excluded. In Python, bool is a proper subclass of int.
    """
    return isinstance(value, Real) and not isinstance(value, bool)

```
src/serialite/_result.py
```.py
from __future__ import annotations

__all__ = [
    "DeserializationError",
    "DeserializationResult",
    "DeserializationFailure",
    "DeserializationSuccess",
]

from abc import abstractmethod
from dataclasses import dataclass
from typing import Any, Generic, NoReturn, TypeVar

Output = TypeVar("Output")


class DeserializationError(Exception):
    """Default exception raised by DeserializationResult.or_die."""

    def __init__(self, error):
        super().__init__(error)
        self.error = error

    def __str__(self):
        return repr(self.error)

    def __repr__(self):
        return f"DeserializationError({self.error!r})"


class DeserializationResult(Generic[Output]):
    """Abstract base class for return value of `Serializer.from_data`."""

    @abstractmethod
    def or_die(self, exception: Exception | type[Exception] = DeserializationError) -> Output:
        """Return value or raise exception.

        If this is a `DeserializationSuccess`, return the value. If this is a
        `DeserializationFailure`, raise an exception. The error may be supplied.
        If the exception is an instance of `BaseException`, it is simply raised.
        Otherwise, it is called with the contents of `self.error` and then
        raised. By default, a `DeserializationError` is constructed and raised.
        """


@dataclass(frozen=True)
class DeserializationFailure(DeserializationResult[NoReturn]):
    """Container for error indicating failure to deserialize.

    This is returned whenever `Serializer.from_data` fails. The `error`
    parameter must be JSON serializable so that it can be returned in an HTTP
    response.
    """

    error: Any

    def or_die(self, exception: Exception | type[Exception] = DeserializationError) -> NoReturn:
        if isinstance(exception, Exception):
            # Simply raise a fully formed exception
            raise exception
        else:
            # Pass error structure to an exception class or other callable
            raise exception(self.error)


@dataclass(frozen=True)
class DeserializationSuccess(Generic[Output], DeserializationResult[Output]):
    """Container for deserialized value.

    This is returned whenever `Serializer.from_data` succeeds. The `value`
    parameter can be any Python object.
    """

    value: Output

    def or_die(self, exception: Exception | type[Exception] = DeserializationError) -> Output:
        return self.value

```
src/serialite/_stable_set.py
```.py
__all__ = ["StableSet"]

from collections.abc import Iterable, Set
from typing import TypeVar

Element = TypeVar("Element", covariant=True)


class StableSet(Set[Element]):
    """An immutable set with stable iteration order."""

    def __init__(self, *items: Element):
        self._elements = {item: None for item in items}

    def __contains__(self, item: Element):
        return item in self._elements.keys()

    def __iter__(self):
        return iter(self._elements.keys())

    def __len__(self):
        return len(self._elements)

    def __or__(self, other: Iterable[Element]):
        return StableSet(*self._elements.keys(), *other)

    def __ror__(self, other: Iterable[Element]):
        return StableSet(*other, *self._elements.keys())

    def __and__(self, other: Iterable[Element]):
        return StableSet(*(element for element in self._elements.keys() if element in other))

    def __rand__(self, other: Iterable[Element]):
        return StableSet(*(element for element in other if element in self._elements))

    def __xor__(self, other: Iterable[Element]):
        return StableSet(
            *(element for element in self._elements.keys() if element not in other),
            *(element for element in other if element not in self._elements),
        )

    def __rxor__(self, other: Iterable[Element]):
        return StableSet(
            *(element for element in other if element not in self._elements),
            *(element for element in self._elements.keys() if element not in other),
        )

    def __sub__(self, other: Iterable[Element]):
        return StableSet(*(element for element in self._elements.keys() if element not in other))

    def __repr__(self):
        return f"StableSet({', '.join(map(repr, self._elements))})"

```
tests/__init__.py
```.py

```
tests/fastapi/__init__.py
```.py
import pytest

try:
    import fastapi
except ImportError:
    pytest.skip("FastAPI not available", allow_module_level=True)

```
tests/fastapi/test_abstract.py
```.py
from dataclasses import dataclass

import pytest
from fastapi import Body, FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel

from serialite import (
    AbstractSerializableMixin,
    FieldsSerializer,
    SerializableMixin,
    SingleField,
    abstract_serializable,
    serializable,
)

# Starting in Python 3.10, classes can get garbage collected and not show up in
# __subclasses__ anymore. This is a place to put such objects to prevent them
# from being garbage collected.
garbage_collection_protection = []


@pytest.fixture(scope="module")
def fastapi_mixin_client():
    app = FastAPI()

    class Base(AbstractSerializableMixin):
        __subclass_serializers__ = {}  # noqa: RUF012
        __fields_serializer__ = FieldsSerializer(a=str, b=float)

        def __init__(self, a: str, b: float):
            self.a = a
            self.b = b

    class Foo(SerializableMixin, Base):
        __fields_serializer__ = FieldsSerializer(**Base.__fields_serializer__, c=bool)

        def __init__(self, a: str, b: float, c: bool):
            super().__init__(a, b)
            self.c = c

    Base.__subclass_serializers__["Foo"] = Foo

    class Bar(SerializableMixin, Base):
        __fields_serializer__ = FieldsSerializer(
            **Base.__fields_serializer__, d=SingleField(int, default=-1)
        )

        def __init__(self, a: str, b: float, d: int = -1):
            super().__init__(a, b)
            self.d = d

    Base.__subclass_serializers__["Bar"] = Bar

    garbage_collection_protection.extend([Foo, Bar])

    @app.post("/")
    def base_a(base: Base = Body(...)) -> str:
        return base.a

    class Wrapper(BaseModel):
        base: Base

    @app.post("/wrapped/")
    def wrapped(wrapped: Wrapper) -> Wrapper:
        if not isinstance(wrapped, Wrapper):
            raise TypeError
        return wrapped

    return TestClient(app)


@pytest.fixture()
def fastapi_dataclass_client():
    app = FastAPI()

    @abstract_serializable
    @dataclass(frozen=True)
    class Base:
        a: str
        b: float

    @serializable
    @dataclass(frozen=True)
    class Foo(Base):
        c: bool

    @serializable
    @dataclass(frozen=True)
    class Bar(Base):
        d: int = -1

    garbage_collection_protection.extend([Foo, Bar])

    @app.post("/")
    def base_a(base: Base) -> str:
        return base.a

    class Wrapper(BaseModel):
        base: Base

    @app.post("/wrapped/")
    def wrapped(wrapped: Wrapper) -> Wrapper:
        if not isinstance(wrapped, Wrapper):
            raise TypeError
        return wrapped

    return TestClient(app)


@pytest.mark.parametrize("client_fixture", ["fastapi_mixin_client", "fastapi_dataclass_client"])
def test_fastapi_basic(client_fixture, request):
    client = request.getfixturevalue(client_fixture)

    response = client.post("/", json={"_type": "Foo", "a": "anything", "b": 2.0, "c": True})
    assert response.json() == "anything"

    response = client.post("/", json={"_type": "Bar", "a": "anything", "b": 2.0, "d": 2})
    assert response.json() == "anything"


@pytest.mark.parametrize("client_fixture", ["fastapi_mixin_client", "fastapi_dataclass_client"])
def test_fastapi_strict(client_fixture, request):
    client = request.getfixturevalue(client_fixture)

    response = client.post("/", json={"_type": "Foo", "a": "anything", "b": "2.0", "c": True})
    assert response.status_code == 422

    response = client.post("/", json={"_type": "Bar", "a": "anything", "b": 2.0, "d": 2.0})
    assert response.status_code == 422


@pytest.mark.parametrize("client_fixture", ["fastapi_mixin_client", "fastapi_dataclass_client"])
def test_fastapi_not_too_strict(client_fixture, request):
    client = request.getfixturevalue(client_fixture)

    response = client.post("/", json={"_type": "Foo", "a": "anything", "b": 2, "c": True})
    assert response.json() == "anything"

    response = client.post("/", json={"_type": "Bar", "a": "anything", "b": 2, "d": 2})
    assert response.json() == "anything"


@pytest.mark.parametrize("client_fixture", ["fastapi_mixin_client", "fastapi_dataclass_client"])
def test_fastapi_basic_wrapped(client_fixture, request):
    client = request.getfixturevalue(client_fixture)

    data = {"base": {"_type": "Foo", "a": "anything", "b": 2.0, "c": True}}
    response = client.post("/wrapped/", json=data)
    assert response.json() == data

    data = {"base": {"_type": "Bar", "a": "anything", "b": 2.0, "d": 2}}
    response = client.post("/wrapped/", json=data)
    assert response.json() == data


@pytest.mark.parametrize("client_fixture", ["fastapi_mixin_client", "fastapi_dataclass_client"])
def test_fastapi_wrapped_strict(client_fixture, request):
    client = request.getfixturevalue(client_fixture)

    data = {"base": {"_type": "Foo", "a": "anything", "b": "2.0", "c": True}}
    response = client.post("/wrapped/", json=data)
    assert response.status_code == 422

    data = {"base": {"_type": "Bar", "a": "anything", "b": 2.0, "d": 2.0}}
    response = client.post("/wrapped/", json=data)
    assert response.status_code == 422


@pytest.mark.parametrize("client_fixture", ["fastapi_mixin_client", "fastapi_dataclass_client"])
def test_fastapi_wrapped_not_too_strict(client_fixture, request):
    client = request.getfixturevalue(client_fixture)

    data = {"base": {"_type": "Foo", "a": "anything", "b": 2, "c": True}}
    response = client.post("/wrapped/", json=data)
    assert response.json() == data

    data = {"base": {"_type": "Bar", "a": "anything", "b": 2, "d": 2}}
    response = client.post("/wrapped/", json=data)
    assert response.json() == data

```
tests/fastapi/test_concrete.py
```.py
from dataclasses import dataclass

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel

from serialite import FieldsSerializer, SerializableMixin, SingleField, serializable

# If a Serialite class is passed directly to FastAPI, its deserialization and
# serialization is handled directly by FastAPI. If a Serialite class is a member
# of a Pydantic class, its deserialization and serialization is handled by
# Pydantic. Both cases need to be tested.


@pytest.fixture()
def fastapi_mixin_client():
    app = FastAPI()

    class Foo(SerializableMixin):
        __fields_serializer__ = FieldsSerializer(
            a=int, b=float, c=bool, d=SingleField(str, default="default")
        )

        def __init__(self, a: int, b: float, c: bool, d: str = "default"):
            self.a = a
            self.b = b
            self.c = c
            self.d = d

    class Bar(SerializableMixin):
        __fields_serializer__ = FieldsSerializer(foo=Foo)

        def __init__(self, foo: Foo):
            self.foo = foo

    @app.post("/", response_model=Bar)
    def extract_foo(bar: Bar) -> Bar:
        if not isinstance(bar, Bar):
            raise TypeError
        return bar

    return TestClient(app)


@pytest.fixture()
def pydantic_mixin_client():
    app = FastAPI()

    class Foo(SerializableMixin):
        __fields_serializer__ = FieldsSerializer(
            a=int, b=float, c=bool, d=SingleField(str, default="default")
        )

        def __init__(self, a: int, b: float, c: bool, d: str = "default"):
            self.a = a
            self.b = b
            self.c = c
            self.d = d

    class Bar(BaseModel):
        foo: Foo

    @app.post("/", response_model=Bar)
    def extract_foo(bar: Bar) -> Bar:
        return bar

    return TestClient(app)


@pytest.fixture()
def fastapi_dataclass_client():
    app = FastAPI()

    @serializable
    @dataclass(frozen=True)
    class Foo:
        a: int
        b: float
        c: bool
        d: str = "default"

    @serializable
    @dataclass(frozen=True)
    class Bar:
        foo: Foo

    @app.post("/", response_model=Bar)
    def extract_foo(bar: Bar) -> Bar:
        if not isinstance(bar, Bar):
            raise TypeError
        return bar

    return TestClient(app)


@pytest.fixture()
def pydantic_dataclass_client():
    app = FastAPI()

    @serializable
    @dataclass(frozen=True)
    class Foo:
        a: int
        b: float
        c: bool
        d: str = "default"

    class Bar(BaseModel):
        foo: Foo

    @app.post("/", response_model=Bar)
    def extract_foo(bar: Bar) -> Bar:
        if not isinstance(bar, Bar):
            raise TypeError
        return bar

    return TestClient(app)


all_clients = [
    "fastapi_mixin_client",
    "pydantic_mixin_client",
    "fastapi_dataclass_client",
    "pydantic_dataclass_client",
]


@pytest.mark.parametrize("client_fixture", all_clients)
def test_fastapi(client_fixture, request):
    client = request.getfixturevalue(client_fixture)

    data = {"foo": {"a": 1, "b": 2.0, "c": True, "d": "anything"}}
    response = client.post("/", json=data)
    assert response.json() == data


@pytest.mark.parametrize("client_fixture", all_clients)
def test_fastapi_ignore_default(client_fixture, request):
    client = request.getfixturevalue(client_fixture)

    data = {"foo": {"a": 1, "b": 2.0, "c": True}}
    response = client.post("/", json=data)
    assert response.json() == data


@pytest.mark.parametrize("client_fixture", all_clients)
def test_fastapi_drop_default(client_fixture, request):
    client = request.getfixturevalue(client_fixture)

    response = client.post("/", json={"foo": {"a": 1, "b": 2.0, "c": True, "d": "default"}})
    assert response.json() == {"foo": {"a": 1, "b": 2.0, "c": True}}


@pytest.mark.parametrize("client_fixture", all_clients)
def test_fastapi_strict(client_fixture, request):
    client = request.getfixturevalue(client_fixture)

    response = client.post("/", json={"foo": {"a": "1", "b": 2.0, "c": True, "d": "anything"}})
    assert response.status_code == 422


@pytest.mark.parametrize("client_fixture", all_clients)
def test_fastapi_not_too_strict(client_fixture, request):
    client = request.getfixturevalue(client_fixture)

    data = {"foo": {"a": 1, "b": 2, "c": True, "d": "anything"}}
    response = client.post("/", json=data)
    assert response.json() == data
    assert isinstance(response.json()["foo"]["b"], float)


@pytest.fixture()
def fastapi_pydantic_client():
    app = FastAPI()

    class Foo(BaseModel):
        a: int
        b: float
        c: bool
        d: str = "default"

    class Bar(BaseModel):
        foo: Foo

    @app.post("/", response_model=Bar)
    def extract_foo(bar: Bar) -> Bar:
        if not isinstance(bar, Bar):
            raise TypeError
        return bar

    return TestClient(app)


@pytest.mark.parametrize("client_fixture", all_clients)
def test_schema(client_fixture, request, fastapi_pydantic_client):
    client = request.getfixturevalue(client_fixture)

    actual_response = client.get("/openapi.json").json()
    expected_response = fastapi_pydantic_client.get("/openapi.json").json()
    assert actual_response["paths"] == expected_response["paths"]
    assert actual_response["paths"] == expected_response["paths"]
    assert actual_response["components"]["schemas"]["Bar"]["type"] == "object"
    assert actual_response["components"]["schemas"]["Foo"]["type"] == "object"
    assert (
        actual_response["components"]["schemas"]["Bar"]["properties"]
        == expected_response["components"]["schemas"]["Bar"]["properties"]
    )
    assert actual_response["components"]["schemas"]["Bar"]["required"] == ["foo"]
    assert actual_response["components"]["schemas"]["Foo"]["required"] == ["a", "b", "c"]
    assert actual_response["components"]["schemas"]["Foo"]["properties"]["a"] == {
        "type": "integer"
    }
    assert actual_response["components"]["schemas"]["Foo"]["properties"]["b"] == {"type": "number"}
    assert actual_response["components"]["schemas"]["Foo"]["properties"]["c"] == {
        "type": "boolean"
    }
    assert actual_response["components"]["schemas"]["Foo"]["properties"]["d"] == {
        "type": "string",
        "default": "default",
    }

```
tests/fastapi/test_monkey_patching.py
```.py
from pydantic import BaseModel

from serialite import SerializableMixin


def test_serialite_is_subclass_of_pydantic():
    class Foo(SerializableMixin):
        def __init__(self, a: int):
            self.a = a

    assert issubclass(Foo, BaseModel)


def test_random_is_not_subclass_of_pydantic():
    assert not issubclass(list, BaseModel)


def test_serialite_is_not_subclass_of_pydantic_subclass():
    class Foo(SerializableMixin):
        def __init__(self, a: int):
            self.a = a

    class UnknownClass(BaseModel):
        pass

    assert not issubclass(Foo, UnknownClass)

```
tests/implementations/__init__.py
```.py

```
tests/implementations/test_boolean.py
```.py
import pytest

from serialite import BooleanSerializer, DeserializationFailure, DeserializationSuccess

boolean_serializer = BooleanSerializer()


@pytest.mark.parametrize("data", [True, False])
def test_valid_inputs(data):
    assert boolean_serializer.from_data(data) == DeserializationSuccess(data)
    assert boolean_serializer.to_data(data) == data


@pytest.mark.parametrize("data", ["maybe", "true"])
def test_from_data_failure(data):
    assert boolean_serializer.from_data(data) == DeserializationFailure(
        f"Not a valid boolean: {data!r}"
    )


def test_to_data_failure():
    with pytest.raises(ValueError):
        _ = boolean_serializer.to_data("true")

```
tests/implementations/test_date_time.py
```.py
from datetime import datetime, timezone

import pytest

from serialite import DateTimeSerializer, DeserializationFailure, DeserializationSuccess

date_time_serializer = DateTimeSerializer()


def test_valid_inputs():
    data = "1969-07-20 20:17:40.000500+00:00"
    value = datetime(1969, 7, 20, 20, 17, 40, 500, timezone.utc)

    assert date_time_serializer.from_data(data) == DeserializationSuccess(value)
    assert date_time_serializer.to_data(value) == data


def test_terminal_z():
    data = "1969-07-20 20:17:40.000500Z"
    value = datetime(1969, 7, 20, 20, 17, 40, 500, timezone.utc)

    assert date_time_serializer.from_data(data) == DeserializationSuccess(value)


@pytest.mark.parametrize("data", [1969, "Hello World"])
def test_from_data_failure(data):
    assert date_time_serializer.from_data(data) == DeserializationFailure(
        f"Not a valid DateTime: {data!r}"
    )


def test_to_data_failure():
    with pytest.raises(ValueError):
        _ = date_time_serializer.to_data("1969")

```
tests/implementations/test_float.py
```.py
from math import inf, isnan, nan

import pytest

from serialite import DeserializationFailure, DeserializationSuccess, FloatSerializer

float_serializer = FloatSerializer()


def float_equal(a, b):
    if isnan(a) and isnan(b):
        return True
    else:
        return a == b


@pytest.mark.parametrize("data", [12, 15.34])
def test_valid_inputs(data):
    actual = float_serializer.from_data(data)
    expected = DeserializationSuccess(data)
    assert actual == expected
    assert isinstance(actual.or_die(), float)  # Verify actual result is a float (not int)
    assert float_serializer.to_data(data) == data


@pytest.mark.parametrize(("data", "value"), [("nan", nan), ("inf", inf), ("-inf", -inf)])
def test_nonfinite_inputs(data, value):
    nonfinite_float_serializer = FloatSerializer(
        nan_values=("nan",), inf_values=("inf",), neg_inf_values=("-inf",)
    )

    # Do not use equality because DeserializationSuccess(nan) != DeserializationSuccess(nan)
    actual = nonfinite_float_serializer.from_data(data)
    assert isinstance(actual, DeserializationSuccess)
    assert float_equal(actual.or_die(), value)
    assert nonfinite_float_serializer.to_data(value) == data


def test_from_data_failure():
    data = "12.5"
    assert float_serializer.from_data(data) == DeserializationFailure("Not a valid float: '12.5'")


def test_to_data_failure():
    with pytest.raises(ValueError):
        _ = float_serializer.to_data("12.5")

```
tests/implementations/test_integer.py
```.py
import pytest

from serialite import (
    DeserializationFailure,
    DeserializationSuccess,
    IntegerSerializer,
    NonnegativeIntegerSerializer,
    PositiveIntegerSerializer,
)

integer_serializer = IntegerSerializer()


class TestIntegerSerializer:
    @pytest.mark.parametrize("data", [12, -15])
    def test_valid_inputs(self, data):
        assert integer_serializer.from_data(data) == DeserializationSuccess(data)
        assert integer_serializer.to_data(data) == data

    @pytest.mark.parametrize("data", ["12", 3.5])
    def test_from_data_failure(self, data):
        assert integer_serializer.from_data(data) == DeserializationFailure(
            f"Not a valid integer: {data!r}"
        )

    def test_to_data_failure(self):
        with pytest.raises(ValueError):
            _ = integer_serializer.to_data(13.5)


nonnegative_integer_serializer = NonnegativeIntegerSerializer()


class TestNonnegativeIntegerSerializer:
    @pytest.mark.parametrize("data", [15, 0])
    def test_valid_inputs(self, data):
        assert nonnegative_integer_serializer.from_data(data) == DeserializationSuccess(data)
        assert nonnegative_integer_serializer.to_data(data) == data

    @pytest.mark.parametrize("data", [12.5, -1, "10"])
    def test_from_data_failure(self, data):
        actual = nonnegative_integer_serializer.from_data(data)
        expected = DeserializationFailure(f"Not a valid nonnegative integer: {data!r}")
        assert actual == expected

    @pytest.mark.parametrize("value", [12.5, -1])
    def test_to_data_failure(self, value):
        with pytest.raises(ValueError):
            _ = nonnegative_integer_serializer.to_data(value)


positive_integer_serializer = PositiveIntegerSerializer()


class TestPositiveIntegerSerializer:
    def test_valid_inputs(self):
        data = 15

        assert positive_integer_serializer.from_data(data) == DeserializationSuccess(data)
        assert positive_integer_serializer.to_data(data) == data

    @pytest.mark.parametrize("data", [12.5, -1, 0])
    def test_from_data_failure(self, data):
        actual = positive_integer_serializer.from_data(data)
        expected = DeserializationFailure(f"Not a valid positive integer: {data!r}")
        assert actual == expected

    @pytest.mark.parametrize("value", [12.5, -1, 0])
    def test_to_data_failure(self, value):
        with pytest.raises(ValueError):
            _ = positive_integer_serializer.to_data(value)

```
tests/implementations/test_json.py
```.py
from serialite import DeserializationSuccess, JsonSerializer


# no error checking, since data is assumed to be valid JSON
def test_valid_inputs():
    data = {"a": "Hello world", "b": 2}

    json_serializer = JsonSerializer()

    assert json_serializer.from_data(data) == DeserializationSuccess(data)
    assert json_serializer.to_data(data) == data

```
tests/implementations/test_list.py
```.py
import pytest

from serialite import (
    DeserializationFailure,
    DeserializationSuccess,
    FloatSerializer,
    ListSerializer,
)

list_serializer = ListSerializer(FloatSerializer())


def test_valid_inputs():
    data = [12.3, 15.5, 16.0]

    assert list_serializer.from_data(data) == DeserializationSuccess(data)
    assert list_serializer.to_data(data) == data


def test_from_data_failure_top_level():
    data = 12.5
    assert list_serializer.from_data(data) == DeserializationFailure("Not a valid list: 12.5")


def test_from_data_failure_element():
    data = ["str1", 15.5, "str2"]
    actual = list_serializer.from_data(data)
    expected_msg = {"0": "Not a valid float: 'str1'", "2": "Not a valid float: 'str2'"}
    assert actual == DeserializationFailure(expected_msg)


def test_to_data_failure_top_level():
    with pytest.raises(ValueError):
        _ = list_serializer.to_data(12.5)


def test_to_data_failure_element():
    with pytest.raises(ValueError):
        _ = list_serializer.to_data([12.5, "a"])

```
tests/implementations/test_literal.py
```.py
import pytest

from serialite import DeserializationFailure, DeserializationSuccess, LiteralSerializer

literal_serializer = LiteralSerializer("none", 1, 2, 3)


@pytest.mark.parametrize("data", ["none", 2])
def test_valid_inputs(data):
    assert literal_serializer.from_data(data) == DeserializationSuccess(data)
    assert literal_serializer.to_data(data) == data


def test_invalid_input():
    data = "invalid"

    assert literal_serializer.from_data(data) == DeserializationFailure(
        "Not one of ['none', 1, 2, 3]: 'invalid'"
    )
    with pytest.raises(ValueError):
        _ = literal_serializer.to_data(data)

```
tests/implementations/test_none.py
```.py
import pytest

from serialite import DeserializationFailure, DeserializationSuccess, NoneSerializer

none_serializer = NoneSerializer()


def test_valid_inputs():
    data = None

    assert none_serializer.from_data(data) == DeserializationSuccess(data)
    assert none_serializer.to_data(data) == data


@pytest.mark.parametrize("data", ["none", False, {}])
def test_from_data_failure(data):
    data = "none"
    assert none_serializer.from_data(data) == DeserializationFailure(f"Not a null: {data!r}")


def test_to_data_failure():
    with pytest.raises(ValueError):
        _ = none_serializer.to_data(False)

```
tests/implementations/test_optional.py
```.py
import pytest

from serialite import (
    DeserializationFailure,
    DeserializationSuccess,
    FloatSerializer,
    OptionalSerializer,
)

optional_serializer = OptionalSerializer(FloatSerializer())


@pytest.mark.parametrize("data", [12.5, None])
def test_valid_inputs(data):
    assert optional_serializer.from_data(data) == DeserializationSuccess(data)
    assert optional_serializer.to_data(data) == data


def test_from_data_failure():
    data = "12.5"
    assert optional_serializer.from_data(data) == DeserializationFailure(
        "Not a valid float: '12.5'"
    )


def test_to_data_failure():
    with pytest.raises(ValueError):
        _ = optional_serializer.to_data("12.5")

```
tests/implementations/test_ordered_dict.py
```.py
from collections import OrderedDict

import pytest

from serialite import (
    DeserializationFailure,
    DeserializationSuccess,
    FloatSerializer,
    OrderedDictSerializer,
    StringSerializer,
)

ordered_dict_serializer = OrderedDictSerializer(StringSerializer(), FloatSerializer())


def test_valid_inputs():
    # from_data: Accepts list of list or tuple (with 2 elements in each)
    data = [["A", 12.3], ["B", 15.5], ["C", 16.0]]
    value = OrderedDict([("A", 12.3), ("B", 15.5), ("C", 16.0)])

    assert ordered_dict_serializer.from_data(data) == DeserializationSuccess(value)
    assert ordered_dict_serializer.to_data(value) == data


def test_from_data_failure_not_a_list():
    data = {"A": 12.3, "B": 15.5}
    actual = ordered_dict_serializer.from_data(data)
    expected = DeserializationFailure("Not a valid list: {'A': 12.3, 'B': 15.5}")
    assert actual == expected


def test_from_data_failure_keys():
    # 2- Deserializing keys generates failures
    data = [[True, 12.3], ["B", 15.5], [1, 16.0]]
    actual = ordered_dict_serializer.from_data(data)
    expected_msg = {"0": "Not a valid string: True", "2": "Not a valid string: 1"}
    assert actual == DeserializationFailure(expected_msg)


def test_from_data_failure_values():
    data = [["A", "12.3"], ["B", 15.5], ["C", False]]
    actual = ordered_dict_serializer.from_data(data)
    expected_msg = {"A": "Not a valid float: '12.3'", "C": "Not a valid float: False"}
    assert actual == DeserializationFailure(expected_msg)


def test_from_data_failure_items():
    data = [["A", 12.3], ["B", 15.5, 18.9], ["C", 16.0]]
    actual = ordered_dict_serializer.from_data(data)
    expected_msg = {"1": "Not a valid length-2 list: ['B', 15.5, 18.9]"}
    assert actual == DeserializationFailure(expected_msg)


def test_to_data_failure():
    with pytest.raises(ValueError):
        _ = ordered_dict_serializer.to_data([12.34, 15.5])

```
tests/implementations/test_ordered_set.py
```.py
import pytest

try:
    from ordered_set import OrderedSet
except ImportError:
    pytest.skip("ordered-set not available", allow_module_level=True)

from serialite import (
    DeserializationFailure,
    DeserializationSuccess,
    FloatSerializer,
    OrderedSetSerializer,
)

ordered_set_serializer = OrderedSetSerializer(FloatSerializer())


def test_valid_inputs():
    data = [12.3, 15.5, 16.0]
    value = OrderedSet([12.3, 15.5, 16.0])

    assert ordered_set_serializer.from_data(data) == DeserializationSuccess(value)
    assert ordered_set_serializer.to_data(value) == data


def test_from_data_failure_top_level():
    data = 12.5
    assert ordered_set_serializer.from_data(data) == DeserializationFailure(
        "Not a valid list: 12.5"
    )


def test_from_data_failure_element():
    data = ["str1", 15.5, "str2"]
    actual = ordered_set_serializer.from_data(data)
    expected_msg = {"0": "Not a valid float: 'str1'", "2": "Not a valid float: 'str2'"}
    assert actual == DeserializationFailure(expected_msg)


def test_from_data_failure_uniqueness():
    data = [12.3, 15.5, 16.0, 12.3]
    actual = ordered_set_serializer.from_data(data)
    expected_msg = {"3": "Duplicated value found: 12.3. Expected a list of unique values."}
    assert actual == DeserializationFailure(expected_msg)


def test_to_data_failure_top_level():
    with pytest.raises(ValueError):
        _ = ordered_set_serializer.to_data(12.5)


def test_to_data_failure_element():
    with pytest.raises(ValueError):
        _ = ordered_set_serializer.to_data(OrderedSet([12.5, "a"]))

```
tests/implementations/test_raw_dict.py
```.py
import pytest

from serialite import (
    DeserializationFailure,
    DeserializationSuccess,
    FloatSerializer,
    RawDictSerializer,
    ReservedSerializer,
    StringSerializer,
)

raw_dict_serializer = RawDictSerializer(FloatSerializer())
raw_dict_serializer_with_key = RawDictSerializer(
    key_serializer=ReservedSerializer(StringSerializer(), reserved={"null"}),
    value_serializer=FloatSerializer(),
)


def test_valid_inputs():
    data = {"a": 12.3, "b": 15.5, "c": 16.0}

    assert raw_dict_serializer.from_data(data) == DeserializationSuccess(data)
    assert raw_dict_serializer.to_data(data) == data


def test_from_data_failure_not_a_dict():
    data = 12.5
    assert raw_dict_serializer.from_data(data) == DeserializationFailure("Not a valid dict: 12.5")


def test_from_data_failure_value():
    data = {"a": "str1", "b": 15.5, "c": "str2"}
    actual = raw_dict_serializer.from_data(data)
    expected_msg = {"a": "Not a valid float: 'str1'", "c": "Not a valid float: 'str2'"}
    assert actual == DeserializationFailure(expected_msg)


def test_to_data_failure():
    with pytest.raises(ValueError):
        _ = raw_dict_serializer.to_data(12.3)


def test_key_serializer_valid_inputs():
    data = {"a": 12.3, "b": 15.5, "c": 16.0}

    assert raw_dict_serializer_with_key.from_data(data) == DeserializationSuccess(data)
    assert raw_dict_serializer_with_key.to_data(data) == data


def test_key_serializer_bad_inputs():
    data = {"a": 12.3, "null": 15.5, "c": 16.0}

    assert raw_dict_serializer_with_key.from_data(data) == DeserializationFailure(
        {"null": "Reserved value: 'null'"}
    )
    with pytest.raises(ValueError):
        _ = raw_dict_serializer_with_key.to_data(data)

```
tests/implementations/test_reserved.py
```.py
import pytest

from serialite import (
    DeserializationFailure,
    DeserializationSuccess,
    ReservedSerializer,
    StringSerializer,
)

reserved_serializer = ReservedSerializer(StringSerializer(), reserved={"false", "true"})


def test_valid_inputs():
    data = "foo"
    assert reserved_serializer.from_data(data) == DeserializationSuccess(data)
    assert reserved_serializer.to_data(data) == data


def test_reserved_inputs():
    data = "true"
    assert reserved_serializer.from_data(data) == DeserializationFailure("Reserved value: 'true'")


def test_to_data_failure():
    with pytest.raises(ValueError):
        _ = reserved_serializer.to_data("true")

```
tests/implementations/test_set.py
```.py
import pytest

from serialite import (
    DeserializationFailure,
    DeserializationSuccess,
    FloatSerializer,
    SetSerializer,
)

set_serializer = SetSerializer(FloatSerializer())


def test_valid_inputs():
    data = [12.3, 15.5, 16.0]
    value = {12.3, 15.5, 16.0}

    assert set_serializer.from_data(data) == DeserializationSuccess(value)
    assert sorted(set_serializer.to_data(value)) == sorted(data)


def test_from_data_failure_top_level():
    data = 12.5
    assert set_serializer.from_data(data) == DeserializationFailure("Not a valid list: 12.5")


def test_from_data_failure_element():
    data = ["str1", 15.5, "str2"]
    actual = set_serializer.from_data(data)
    expected_msg = {"0": "Not a valid float: 'str1'", "2": "Not a valid float: 'str2'"}
    assert actual == DeserializationFailure(expected_msg)


def test_from_data_failure_uniqueness():
    data = [12.3, 15.5, 16.0, 12.3]
    actual = set_serializer.from_data(data)
    expected_msg = {"3": "Duplicated value found: 12.3. Expected a list of unique values."}
    assert actual == DeserializationFailure(expected_msg)


def test_to_data_failure_top_level():
    with pytest.raises(ValueError):
        _ = set_serializer.to_data(12.5)


def test_to_data_failure_element():
    with pytest.raises(ValueError):
        _ = set_serializer.to_data({12.5, "a"})

```
tests/implementations/test_string.py
```.py
import pytest

from serialite import DeserializationFailure, DeserializationSuccess, StringSerializer

string_serializer = StringSerializer()
regex_serializer = StringSerializer(r"[a-zA-Z]+")


def test_valid_inputs():
    data = "Hello World"

    assert string_serializer.from_data(data) == DeserializationSuccess(data)
    assert string_serializer.to_data(data) == data


def test_from_data_failure():
    data = 12.5
    assert string_serializer.from_data(data) == DeserializationFailure("Not a valid string: 12.5")


def test_to_data_failure():
    with pytest.raises(ValueError):
        _ = string_serializer.to_data(12.5)


def test_regex():
    assert regex_serializer.from_data("foo") == DeserializationSuccess("foo")
    assert regex_serializer.to_data("foo") == "foo"
    assert regex_serializer.from_data("foo ") == DeserializationFailure(
        "Does not match regex r'[a-zA-Z]+': 'foo '"
    )
    assert regex_serializer.from_data(" foo") == DeserializationFailure(
        "Does not match regex r'[a-zA-Z]+': ' foo'"
    )
    with pytest.raises(ValueError):
        _ = regex_serializer.to_data("foo*")

```
tests/implementations/test_try_union.py
```.py
import pytest

from serialite import (
    BooleanSerializer,
    DeserializationFailure,
    DeserializationSuccess,
    FloatSerializer,
    IntegerSerializer,
    TryUnionSerializer,
)

try_union_serializer = TryUnionSerializer(
    FloatSerializer(), IntegerSerializer(), BooleanSerializer()
)


@pytest.mark.parametrize("data", [True, 12, 13.5])
def test_valid_inputs(data):
    assert try_union_serializer.from_data(data) == DeserializationSuccess(data)
    assert try_union_serializer.to_data(data) == data


def test_from_data_failure():
    # The error message is too complex to bother verifying
    data = "Hello!"
    actual = try_union_serializer.from_data(data)
    assert isinstance(actual, DeserializationFailure)


def test_to_data_failure():
    with pytest.raises(ValueError):
        _ = try_union_serializer.to_data("invalid")

```
tests/implementations/test_tuple.py
```.py
import pytest

from serialite import (
    DeserializationFailure,
    DeserializationSuccess,
    FloatSerializer,
    StringSerializer,
    TupleSerializer,
)

tuple_serializer = TupleSerializer(FloatSerializer(), StringSerializer())


def test_valid_inputs():
    data = [12.3, "foo"]
    value = tuple(data)

    assert tuple_serializer.from_data(data) == DeserializationSuccess(value)
    assert tuple_serializer.to_data(value) == data


def test_from_data_failure_wrong_type():
    data = 12.5
    assert tuple_serializer.from_data(data) == DeserializationFailure("Not a valid list: 12.5")


def test_from_data_failure_wrong_length():
    data = [12.5]
    assert tuple_serializer.from_data(data) == DeserializationFailure(
        "Has 1 elements, not 2: [12.5]"
    )


def test_from_data_failure_element():
    data = ["12.3", "str2"]
    actual = tuple_serializer.from_data(data)
    expected_msg = {"0": "Not a valid float: '12.3'"}
    assert actual == DeserializationFailure(expected_msg)


def test_to_data_failure_wrong_type():
    with pytest.raises(ValueError):
        _ = tuple_serializer.to_data(12.5)


def test_to_data_failure_wrong_length():
    with pytest.raises(ValueError):
        _ = tuple_serializer.to_data([12.3, "str2", "str3"])


def test_to_data_failure_element():
    with pytest.raises(ValueError):
        _ = tuple_serializer.to_data(["12.5", "a"])

```
tests/implementations/test_uuid.py
```.py
from uuid import UUID

import pytest

from serialite import DeserializationFailure, DeserializationSuccess, UuidSerializer

uuid_serializer = UuidSerializer()


def test_valid_inputs():
    data = "00112233-4455-6677-8899-aabbccddeeff"
    value = UUID(data)

    assert uuid_serializer.from_data(data) == DeserializationSuccess(value)
    assert uuid_serializer.to_data(value) == data


@pytest.mark.parametrize("data", [12.5, "Hello World"])
def test_from_data_failure(data):
    assert uuid_serializer.from_data(data) == DeserializationFailure(f"Not a valid UUID: {data!r}")


def test_to_data_failure():
    with pytest.raises(ValueError):
        # string instead of UUID object
        _ = uuid_serializer.to_data("00112233-4455-6677-8899-aabbccddeeff")

```
tests/test_dataclass.py
```.py
import dataclasses
from dataclasses import dataclass

import pytest

from serialite import (
    DeserializationFailure,
    PositiveIntegerSerializer,
    abstract_serializable,
    field,
    serializable,
)


@serializable
@dataclass
class Basic:
    a: int
    b: str


@serializable
@dataclass(frozen=True)
class Frozen:
    a: int
    b: str


@abstract_serializable
@dataclass(frozen=True)
class Base:
    a: int


@serializable
@dataclass(frozen=True)
class Derived(Base):
    b: str


@pytest.mark.parametrize("cls", [Basic, Frozen, Derived])
def test_dataclass_basic(cls: type):
    value = cls(1, "foo")
    data = {"a": 1, "b": "foo"}

    assert value.to_data() == data
    assert cls.from_data(data).or_die() == value


@serializable
@dataclass(frozen=True)
class Default:
    a: int
    b: str = "bar"


@serializable
@dataclass(frozen=True)
class FieldDefault:
    a: int
    b: str = field(default="bar")


@serializable
@dataclass(frozen=True)
class FieldDefaultFactory:
    a: int
    b: str = field(default_factory=lambda: "bar")


@serializable
@dataclass(frozen=True)
class BuiltinFieldDefault:
    a: int
    b: str = dataclasses.field(default="bar")


@serializable
@dataclass(frozen=True)
class BuiltinFieldDefaultFactory:
    a: int
    b: str = dataclasses.field(default_factory=lambda: "bar")


@pytest.mark.parametrize(
    "cls",
    [Default, FieldDefault, FieldDefaultFactory, BuiltinFieldDefault, BuiltinFieldDefaultFactory],
)
def test_dataclass_field(cls: type):
    value_not_default = cls(1, "foo")
    value_implicit_default = cls(1)
    value_explicit_default = cls(1, "bar")
    data_not_default = {"a": 1, "b": "foo"}
    data_implicit_default = {"a": 1}
    data_explicit_default = {"a": 1, "b": "bar"}

    assert value_implicit_default == value_explicit_default

    assert value_not_default.to_data() == data_not_default
    assert value_implicit_default.to_data() == data_implicit_default
    assert value_explicit_default.to_data() == data_implicit_default

    assert cls.from_data(data_not_default).or_die() == value_not_default
    assert cls.from_data(data_implicit_default).or_die() == value_implicit_default
    assert cls.from_data(data_explicit_default).or_die() == value_implicit_default


def test_field_serializer_is_serializer():
    @serializable
    @dataclass(frozen=True)
    class Override:
        a: int = field(serializer=PositiveIntegerSerializer())
        b: str = "bar"

    value = Override(1)
    good_data = {"a": 1}
    bad_data = {"a": -1}

    assert value.to_data() == good_data
    assert Override.from_data(good_data).or_die() == value
    assert Override.from_data(bad_data) == DeserializationFailure(
        {"a": "Not a valid positive integer: -1"}
    )


def test_field_serializer_is_type():
    @serializable
    @dataclass(frozen=True)
    class IsType:
        a: int
        b: list = field(default_factory=list, serializer=list[str])

    value_default = IsType(1)
    value = IsType(1, ["a", "b"])

    data_default = {"a": 1}
    good_data = {"a": 1, "b": ["a", "b"]}
    bad_data = {"a": 1, "b": ["a", 2]}

    assert value_default.to_data() == data_default
    assert value.to_data() == good_data

    assert IsType.from_data(data_default).or_die() == value_default
    assert IsType.from_data(good_data).or_die() == value
    assert IsType.from_data(bad_data) == DeserializationFailure(
        {"b": {"1": "Not a valid string: 2"}}
    )

```
tests/test_dispatcher.py
```.py
from datetime import datetime
from typing import Any, Dict, List, Literal, Optional, Tuple, Union
from uuid import UUID

import pytest

from serialite import DeserializationSuccess, serializer


@pytest.mark.parametrize(
    ("data_type", "data", "value"),
    [
        (bool, True, True),
        (int, 3, 3),
        (float, 2.5, 2.5),
        (str, "a", "a"),
        (datetime, "2018-06-28 03:18:53", datetime(2018, 6, 28, 3, 18, 53)),
        (
            UUID,
            "00112233-4455-6677-8899-aabbccddeeff",
            UUID("00112233-4455-6677-8899-aabbccddeeff"),
        ),
        (List[int], [11, 22, 33], [11, 22, 33]),
        (List[str], ["a", "b"], ["a", "b"]),
        (list[str], ["a", "b"], ["a", "b"]),
        (Tuple[int, str], [5, "a"], (5, "a")),
        (tuple[int, str], [5, "a"], (5, "a")),
        (Dict[str, int], {"a": 11, "b": 22}, {"a": 11, "b": 22}),
        (dict[str, int], {"a": 11, "b": 22}, {"a": 11, "b": 22}),
        (Dict[int, float], [[11, 11.5], [22, 22.8]], {11: 11.5, 22: 22.8}),
        (dict[int, float], [[11, 11.5], [22, 22.8]], {11: 11.5, 22: 22.8}),
    ],
)
def test_dispatch(data_type, data, value):
    this_serializer = serializer(data_type)

    assert this_serializer.from_data(data) == DeserializationSuccess(value)
    assert this_serializer.to_data(value) == data


@pytest.mark.parametrize("type", [Optional[int], int | None])
def test_dispatch_optional(type):
    optional_serializer = serializer(type)

    assert optional_serializer.from_data(1).or_die() == 1
    assert optional_serializer.to_data(1) == 1
    assert optional_serializer.from_data(None).or_die() is None
    assert optional_serializer.to_data(None) is None


@pytest.mark.parametrize("type", [Union[str, int], str | int])
def test_dispatch_union(type):
    union_serializer = serializer(type)

    assert union_serializer.from_data(1).or_die() == 1
    assert union_serializer.to_data(1) == 1
    assert union_serializer.from_data("a").or_die() == "a"
    assert union_serializer.to_data("a") == "a"


def test_dispatch_literal():
    literal_serializer = serializer(Literal["none", 1, 2, 3])

    assert literal_serializer.from_data("none").or_die() == "none"
    assert literal_serializer.to_data(1) == 1
    assert literal_serializer.from_data(2).or_die() == 2
    assert literal_serializer.to_data(3) == 3


def test_dispatch_any():
    any_serializer = serializer(Any)

    assert any_serializer.from_data(1).or_die() == 1
    assert any_serializer.from_data("any string").or_die() == "any string"
    assert any_serializer.from_data({"a": 1}).or_die() == {"a": 1}

```
tests/test_field_serializers.py
```.py
from uuid import UUID

import pytest

from serialite import (
    AccessPermissions,
    DeserializationFailure,
    DeserializationSuccess,
    FieldsSerializer,
    MultiField,
    SingleField,
    UuidSerializer,
    empty_default,
    serializer,
)


@pytest.mark.parametrize(
    "fields_serializer",
    [
        FieldsSerializer(myField=UUID),
        FieldsSerializer(myField=UuidSerializer()),
        FieldsSerializer(myField=SingleField(UUID)),
        FieldsSerializer(myField=SingleField(UuidSerializer())),
    ],
)
def test_single_field(fields_serializer):
    data = {"myField": "00112233-4455-6677-8899-aabbccddeeff"}
    value = {"myField": UUID("00112233-4455-6677-8899-aabbccddeeff")}

    assert fields_serializer.from_data(data).or_die() == value
    assert fields_serializer.to_data(value) == data


@pytest.mark.parametrize(
    "fields_serializer",
    [
        FieldsSerializer(myField=MultiField({"a": UUID})),
        FieldsSerializer(myField=MultiField({"a": UUID, "b": str})),
        FieldsSerializer(myField=MultiField({"b": str, "a": UUID}, to_data="a")),
        FieldsSerializer(myField=MultiField({"a": UuidSerializer()})),
    ],
)
def test_multi_field(fields_serializer):
    data = {"a": "00112233-4455-6677-8899-aabbccddeeff"}
    value = {"myField": UUID("00112233-4455-6677-8899-aabbccddeeff")}

    assert fields_serializer.from_data(data).or_die() == value
    assert fields_serializer.to_data(value) == data


@pytest.mark.parametrize(
    "fields_serializer",
    [
        FieldsSerializer(myField=SingleField(str, default="Pirate")),
        FieldsSerializer(myField=MultiField({"a": str, "b": int}, default="Pirate")),
    ],
)
def test_default_value(fields_serializer):
    data = {}
    value = {"myField": "Pirate"}

    assert fields_serializer.from_data(data).or_die() == value
    assert fields_serializer.to_data(value) == data


def test_from_data_not_dict():
    fields_serializer = FieldsSerializer()
    assert fields_serializer.from_data(1) == DeserializationFailure("Not a dictionary: 1")


@pytest.mark.parametrize(
    "fields_serializer",
    [
        FieldsSerializer(a=int),
        FieldsSerializer(myField=MultiField({"b": str, "a": int})),
    ],
)
def test_from_data_deserialization_failure(fields_serializer):
    data = {"a": "2.5"}
    assert fields_serializer.from_data(data) == DeserializationFailure(
        {"a": "Not a valid integer: '2.5'"}
    )


def test_from_data_invalid_field():
    fields_serializer = FieldsSerializer(myField=str)
    assert fields_serializer.from_data({"c": 1, "myField": "Hello"}) == DeserializationFailure(
        {"c": "This field is invalid."}
    )


def test_from_data_invalid_field_allowed():
    fields_serializer = FieldsSerializer(myField=str)
    assert fields_serializer.from_data(
        {"c": 1, "myField": "Hello"}, allow_unused=True
    ) == DeserializationSuccess({"myField": "Hello"})


def test_from_data_multi_field_repeated_fields():
    fields_serializer = FieldsSerializer(a=MultiField({"b": int, "c": str}))
    assert fields_serializer.from_data({"b": 2, "c": "Boom"}) == DeserializationFailure(
        {"c": "This field cannot be provided because these fields are already provided: b"}
    )


@pytest.mark.parametrize(
    "fields_serializer",
    [
        FieldsSerializer(myField=SingleField(UUID, default=empty_default)),
        FieldsSerializer(myField=MultiField({"myField": UUID, "alt": str}, default=empty_default)),
    ],
)
def test_from_data_default_value_empty_default(fields_serializer):
    data = {}
    value = {}

    assert fields_serializer.from_data(data) == DeserializationSuccess(value)


def test_from_data_no_default_single_field():
    fields_serializer = FieldsSerializer(myField=SingleField(str))
    data = {}
    assert fields_serializer.from_data(data) == DeserializationFailure(
        {"myField": "This field is required."}
    )


def test_from_data_no_default_multi_field():
    fields_serializer = FieldsSerializer(myField=MultiField({"a": str, "b": int}))
    data = {}
    assert fields_serializer.from_data(data) == DeserializationFailure(
        {"myField": "One of these fields is required: a, b"}
    )


def test_from_data_field_not_writable():
    data = {"b": "Hiding"}

    fields_serializer = FieldsSerializer(
        myField=MultiField({"a": int, "b": str}, access=AccessPermissions.read_only)
    )
    assert fields_serializer.from_data(data) == DeserializationFailure(
        {"b": "This field is invalid."}
    )

    fields_serializer = FieldsSerializer(b=SingleField(str, access=AccessPermissions.read_only))
    assert fields_serializer.from_data(data, allow_unused=True) == DeserializationSuccess({})


def test_to_data_default_value_no_hiding():
    value = {"myField": "Pirate"}

    fields_serializer = FieldsSerializer(
        myField=SingleField(str, default="Pirate", hide_default=False)
    )
    assert fields_serializer.to_data(value) == value

    fields_serializer = FieldsSerializer(
        myField=MultiField({"a": str, "b": int}, default="Pirate", hide_default=False)
    )
    assert fields_serializer.to_data(value) == {"a": "Pirate"}


def test_to_data_multi_field_use_to_data():
    fields_serializer = FieldsSerializer(myField=MultiField({"a": int, "b": str}))
    value = {"myField": 2}
    assert fields_serializer.to_data(value) == {"a": 2}

    fields_serializer = FieldsSerializer(myField=MultiField({"a": int, "b": str}, to_data="b"))
    value = {"myField": "3"}
    assert fields_serializer.to_data(value) == {"b": "3"}


def test_to_data_source_object():
    class TempObject:
        def __init__(self, a, b):
            self.a = a
            self.b = b

    fields_serializer = FieldsSerializer(a=int, b=str)
    actual = fields_serializer.to_data(TempObject(3, "Hello"), source="object")
    expected = {"a": 3, "b": "Hello"}
    assert actual == expected


def test_to_data_source_invalid():
    fields_serializer = FieldsSerializer(a=int)
    with pytest.raises(ValueError):
        _ = fields_serializer.to_data({"a": 1}, source="integer")


def test_to_data_field_not_readable():
    fields_serializer = FieldsSerializer(
        a=int, b=SingleField(serializer(str), access=AccessPermissions.write_only)
    )
    value = {"a": 3, "b": "Hiding"}
    expected = {"a": 3}  # Do not serialize b
    actual = fields_serializer.to_data(value)
    assert actual == expected


def test_empty_input():
    fields_serializer = FieldsSerializer()

    assert fields_serializer.from_data({}) == DeserializationSuccess({})
    assert fields_serializer.to_data({}) == {}

```
tests/test_mixins.py
```.py
from abc import abstractmethod
from dataclasses import dataclass

from serialite import (
    AbstractSerializableMixin,
    DeserializationFailure,
    DeserializationSuccess,
    serializable,
)


class DataAbstractSerializableClass(AbstractSerializableMixin):
    __subclass_serializers__ = {}  # noqa: RUF012

    @abstractmethod
    def get_value(self):
        raise NotImplementedError()


# Subclass A: implements from_data and to_data
# This class does not have @serializable decorator by design
class DataSubClassSerializableA(DataAbstractSerializableClass):
    value: float

    @classmethod
    def from_data(cls, data):
        return DeserializationSuccess(data["value"])

    @classmethod
    def to_data(cls, value):
        return {"value": value}

    def get_value(self):
        return self.value


DataSubClassSerializableA.__subclass_serializers__["DataSubClassSerializableA"] = (
    DataSubClassSerializableA
)


def test_from_data_valid():
    data = {"_type": "DataSubClassSerializableA", "value": 2.4}
    assert DataAbstractSerializableClass.from_data(data) == DeserializationSuccess(2.4)


def test_from_data_no_type():
    data = {"value": 2.4}
    actual = DataAbstractSerializableClass.from_data(data)
    expected = DeserializationFailure({"_type": "This field is required."})
    assert actual == expected


def test_from_data_not_a_dict():
    data = "Boom"
    actual = DataAbstractSerializableClass.from_data(data)
    expected = DeserializationFailure("Not a dictionary: 'Boom'")
    assert actual == expected


def test_from_data_not_a_subclass():
    data = {"_type": "NotThere", "value": 2.4}
    actual = DataAbstractSerializableClass.from_data(data)
    expected = DeserializationFailure({"_type": "Class not found: 'NotThere'"})
    assert actual == expected


# Base class with serializable decorator
@serializable
@dataclass(frozen=True)
class DataSerializableClass:
    dimension: int
    value: float
    name: str
    outputs: dict[str, float]


def test_valid_inputs():
    data = {"dimension": 3, "value": 5.6, "name": "macrophage", "outputs": {"a": 1.2, "b": 3.4}}
    value = DataSerializableClass(3, 5.6, "macrophage", {"a": 1.2, "b": 3.4})

    assert DataSerializableClass.from_data(data) == DeserializationSuccess(value)
    assert DataSerializableClass.to_data(value) == data


def test_from_data_failure():
    # Missing required field: name
    data = {"dimension": 3, "value": 5.6, "outputs": {"a": 1.2, "b": 3.4}}
    assert DataSerializableClass.from_data(data) == DeserializationFailure(
        {"name": "This field is required."}
    )

    # Deserialization failure
    data = {"dimension": 3, "value": 5.6, "name": "macrophage", "outputs": "Boom"}
    assert DataSerializableClass.from_data(data) == DeserializationFailure(
        {"outputs": "Not a valid dict: 'Boom'"}
    )

```
tests/test_numpy.py
```.py
import pytest

try:
    import numpy as np
except ImportError:
    pytest.skip("NumPy not available", allow_module_level=True)

from serialite import (
    ArraySerializer,
    DeserializationFailure,
    DeserializationSuccess,
    IntegerSerializer,
    serializer,
)

array_serializer = ArraySerializer(dtype=int)


class TestArraySerializer:
    @pytest.mark.parametrize(
        "serializer_obj", [ArraySerializer(dtype=int), ArraySerializer(IntegerSerializer())]
    )
    def test_valid_inputs(self, serializer_obj):
        data = [12, 15, 18]
        value = np.asarray(data, dtype=int)

        actual = serializer_obj.from_data(data)
        assert isinstance(actual, DeserializationSuccess)
        np.testing.assert_equal(actual.or_die(), value)

        assert serializer_obj.to_data(value) == data

    def test_from_data_failure(self):
        data = ["str1", 15, "str2"]
        actual = array_serializer.from_data(data)
        expected_msg = {"0": "Not a valid integer: 'str1'", "2": "Not a valid integer: 'str2'"}
        assert actual == DeserializationFailure(expected_msg)

    def test_to_data_failure_not_array(self):
        with pytest.raises(ValueError):
            _ = array_serializer.to_data(3)

    def test_to_data_failure_bad_element(self):
        with pytest.raises(ValueError):
            _ = array_serializer.to_data([12, 15, 18])


def test_dispatch_np_array():
    data = [1.1, 2.2, 3.3, 4.4]
    value = np.asarray([1.1, 2.2, 3.3, 4.4])
    array_serializer = serializer(np.ndarray)

    np.testing.assert_equal(array_serializer.from_data(data).or_die(), value)
    assert array_serializer.to_data(value) == data

```
tests/test_serializers_base.py
```.py
import pytest

from serialite import (
    DeserializationError,
    DeserializationFailure,
    DeserializationSuccess,
    Serializer,
)


class TestDeserializationError:
    def test_constructor(self):
        obj = DeserializationError("error msg")
        assert obj.error == "error msg"

    def test_str(self):
        obj = DeserializationError("error msg")
        assert str(obj) == "'error msg'"

    def test_repr(self):
        obj = DeserializationError("error msg")
        assert repr(obj) == "DeserializationError('error msg')"


class TestDeserializationFailure:
    def test_constructor(self):
        error = "Should be integer"
        actual = DeserializationFailure(error)
        assert actual.error == error

    def test_or_die(self):
        error = "Should be integer"
        obj = DeserializationFailure(error)
        with pytest.raises(DeserializationError):
            obj.or_die()

    def test_or_die_custom(self):
        error = "Should be integer"
        obj = DeserializationFailure(error)
        with pytest.raises(TypeError):
            obj.or_die(TypeError("Custom message"))


class TestDeserializationSuccess:
    def test_constructor(self):
        value = "pass"
        actual = DeserializationSuccess(value)
        assert actual.value == value

    def test_or_die(self):
        value = "my value"
        obj = DeserializationSuccess(value)
        actual = obj.or_die()
        assert actual == value


class NoneSerializer(Serializer):
    @staticmethod
    def from_data(data):
        if data is None:
            return DeserializationSuccess(None)
        else:
            return DeserializationFailure(f"Not None: {data!r}")

    @staticmethod
    def to_data(value):
        if value is None:
            return None
        else:
            raise TypeError("Value must be None.")

```
tests/test_stable_set.py
```.py
import pytest

from serialite import StableSet


@pytest.mark.parametrize(
    ("set1", "set2"),
    [
        (StableSet(), StableSet()),
        (StableSet(4, 1), StableSet(4, 1)),
        (StableSet(4, 1), StableSet(1, 4)),
    ],
)
def test_equal(set1, set2):
    assert set1 == set2


@pytest.mark.parametrize(
    ("set1", "set2"),
    [
        (StableSet(), StableSet(2)),
        (StableSet(2), StableSet()),
        (StableSet(4), StableSet(4, 1)),
        (StableSet(4, 1), StableSet(4)),
    ],
)
def test_not_equal(set1, set2):
    assert set1 != set2


@pytest.mark.parametrize(
    ("set1", "set2", "expected"),
    [
        (StableSet(), StableSet(), StableSet()),
        (StableSet(4, 1), StableSet(4), StableSet(4, 1)),
        (StableSet(4, 1, 2), StableSet(4, 5, 6), StableSet(4, 1, 2, 5, 6)),
    ],
)
def test_union(set1, set2, expected):
    actual = set1 | set2
    assert actual == expected
    assert list(actual) == list(expected)


@pytest.mark.parametrize(
    ("set1", "set2", "expected"),
    [
        (StableSet(), StableSet(), StableSet()),
        (StableSet(4, 1), StableSet(1, 4), StableSet(4, 1)),
        (StableSet(4, 1), StableSet(4), StableSet(4)),
        (StableSet(4, 1, 2), StableSet(4, 5, 6), StableSet(4)),
    ],
)
def test_intersection(set1, set2, expected):
    actual = set1 & set2
    assert actual == expected
    assert list(actual) == list(expected)


@pytest.mark.parametrize(
    ("set1", "set2", "expected"),
    [
        (StableSet(), StableSet(), StableSet()),
        (StableSet(4, 1), StableSet(1, 4), StableSet()),
        (StableSet(4, 1), StableSet(4), StableSet(1)),
        (StableSet(4, 1, 2), StableSet(4, 5, 6), StableSet(1, 2)),
    ],
)
def test_subtraction(set1, set2, expected):
    actual = set1 - set2
    assert actual == expected
    assert list(actual) == list(expected)


@pytest.mark.parametrize(
    ("set1", "set2", "expected"),
    [
        (StableSet(), StableSet(), StableSet()),
        (StableSet(4, 1), StableSet(1, 4), StableSet()),
        (StableSet(4, 1), StableSet(4), StableSet(1)),
        (StableSet(4, 1, 2), StableSet(4, 5, 6), StableSet(1, 2, 5, 6)),
    ],
)
def test_difference(set1, set2, expected):
    actual = set1 ^ set2
    assert actual == expected
    assert list(actual) == list(expected)

```


