# pixi_swig_py

A test repository for building Python C extensions with SWIG, CMake, and Pixi.

## Overview

This project demonstrates how to:
- Write a simple C library
- Use SWIG to generate Python bindings
- Build the extension module with CMake
- Manage dependencies with Pixi

## Project Structure

```
pixi_swig_py/
├── CMakeLists.txt       # CMake build configuration
├── pixi.toml            # Pixi configuration file
├── README.md            # This file
├── src/
│   ├── example.c        # C library implementation
│   ├── example.h        # C library header
│   └── example.i        # SWIG interface file
└── tests/
    └── test_example.py  # Python test script
```

## Prerequisites

- [Pixi](https://pixi.sh/) package manager (recommended), OR
- CMake >= 3.15
- SWIG >= 4.0
- Python >= 3.9 with development headers

## Building with Pixi (Recommended)

Pixi will handle all dependencies automatically:

```bash
# Configure and build
pixi run build

# Run tests
pixi run test

# Clean build artifacts
pixi run clean
```

## Building without Pixi

If you have CMake, SWIG, and Python installed:

```bash
# Configure
cmake -B build -S .

# Build
cmake --build build

# Test
python tests/test_example.py
```

## Usage

After building, you can use the module in Python:

```python
import sys
sys.path.insert(0, 'lib')

import example

# Basic arithmetic
print(example.add(2, 3))        # Output: 5
print(example.multiply(2.5, 4)) # Output: 10.0

# Factorial
print(example.factorial(5))     # Output: 120

# Fibonacci
print(example.fibonacci(10))    # Output: 55
```

## License

MIT
