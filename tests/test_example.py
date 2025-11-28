#!/usr/bin/env python3
"""Test script for the example SWIG module."""

import sys
from pathlib import Path

# Add the lib directory to the Python path
lib_dir = Path(__file__).resolve().parent.parent / 'lib'
sys.path.insert(0, str(lib_dir))

import example


def test_add():
    """Test the add function."""
    assert example.add(2, 3) == 5
    assert example.add(-1, 1) == 0
    assert example.add(0, 0) == 0
    print("test_add passed")


def test_multiply():
    """Test the multiply function."""
    assert abs(example.multiply(2.5, 4.0) - 10.0) < 1e-9
    assert abs(example.multiply(-2.0, 3.0) - (-6.0)) < 1e-9
    assert abs(example.multiply(0.0, 100.0) - 0.0) < 1e-9
    print("test_multiply passed")


def test_factorial():
    """Test the factorial function."""
    assert example.factorial(0) == 1
    assert example.factorial(1) == 1
    assert example.factorial(5) == 120
    assert example.factorial(10) == 3628800
    assert example.factorial(-1) == -1  # Error case for negative input
    print("test_factorial passed")


def test_fibonacci():
    """Test the fibonacci function."""
    assert example.fibonacci(0) == 0
    assert example.fibonacci(1) == 1
    assert example.fibonacci(10) == 55
    assert example.fibonacci(15) == 610
    print("test_fibonacci passed")


def main():
    """Run all tests."""
    print("Running tests...")
    test_add()
    test_multiply()
    test_factorial()
    test_fibonacci()
    print("All tests passed!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
