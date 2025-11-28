#!/usr/bin/env python3
"""Test script for c_arrays SWIG wrapper"""

import sys
import os

# Add the build directory to path if needed
sys.path.insert(0, os.path.dirname(__file__))

try:
    import c_arrays
    print("✓ Module imported successfully")
except ImportError as e:
    print(f"✗ Failed to import module: {e}")
    sys.exit(1)


def test_double_array():
    """Test DoubleArray functionality"""
    print("\n--- Testing DoubleArray ---")
    
    # Create array of 5 doubles
    arr = c_arrays.DoubleArray(5)
    
    # Set values
    for i in range(5):
        arr[i] = i * 1.5
    
    # Read values
    print("Array contents:")
    for i in range(5):
        value = arr[i]
        expected = i * 1.5
        print(f"  arr[{i}] = {value} (expected {expected})")
        assert abs(value - expected) < 1e-10, f"Mismatch at index {i}"
    
    print("✓ DoubleArray test passed")


def test_float_array():
    """Test FloatArray functionality"""
    print("\n--- Testing FloatArray ---")
    
    arr = c_arrays.FloatArray(3)
    test_values = [3.14, 2.71, 1.41]
    
    for i, val in enumerate(test_values):
        arr[i] = val
    
    for i, expected in enumerate(test_values):
        value = arr[i]
        print(f"  arr[{i}] = {value} (expected {expected})")
        assert abs(value - expected) < 1e-6, f"Mismatch at index {i}"
    
    print("✓ FloatArray test passed")


def test_int_array():
    """Test IntArray functionality"""
    print("\n--- Testing IntArray ---")
    
    arr = c_arrays.IntArray(4)
    
    for i in range(4):
        arr[i] = i * 10
    
    for i in range(4):
        value = arr[i]
        expected = i * 10
        print(f"  arr[{i}] = {value} (expected {expected})")
        assert value == expected, f"Mismatch at index {i}"
    
    print("✓ IntArray test passed")


def test_unsigned_array():
    """Test UnsignedArray functionality"""
    print("\n--- Testing UnsignedArray ---")
    
    arr = c_arrays.UnsignedArray(3)
    test_values = [0, 42, 4294967295]  # Include max unsigned int
    
    for i, val in enumerate(test_values):
        arr[i] = val
    
    for i, expected in enumerate(test_values):
        value = arr[i]
        print(f"  arr[{i}] = {value} (expected {expected})")
        assert value == expected, f"Mismatch at index {i}"
    
    print("✓ UnsignedArray test passed")


def test_pointer_manipulation():
    """Test pointer casting with cdata"""
    print("\n--- Testing Pointer Manipulation ---")
    
    arr = c_arrays.DoubleArray(10)
    arr[0] = 123.456
    
    # Get pointer to array
    ptr = arr.cast()
    print(f"  Pointer: {ptr}")
    print("✓ Pointer manipulation test passed")


if __name__ == "__main__":
    print("=" * 50)
    print("C Arrays SWIG Wrapper Test Suite")
    print("=" * 50)
    
    try:
        test_double_array()
        test_float_array()
        test_int_array()
        test_unsigned_array()
        test_pointer_manipulation()
        
        print("\n" + "=" * 50)
        print("✓ All tests passed!")
        print("=" * 50)
    except Exception as e:
        print(f"\n✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
