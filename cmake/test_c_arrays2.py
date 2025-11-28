#!/usr/bin/env python3
"""Test the CMake-built SWIG extension"""

import sys

try:
    import c_arrays
    print("✓ Module imported successfully")
except ImportError as e:
    print(f"✗ Failed to import: {e}")
    sys.exit(1)

# Test DoubleArray
arr = c_arrays.DoubleArray(5)
arr[0] = 3.14
arr[1] = 2.71

print(f"✓ DoubleArray[0] = {arr[0]}")
print(f"✓ DoubleArray[1] = {arr[1]}")

print("\n✓ All tests passed!")
