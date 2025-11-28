#!/bin/bash

# Build script for SWIG C arrays wrapper

set -e  # Exit on error

echo "Building SWIG wrapper for C arrays..."

# Step 1: Generate SWIG wrapper
echo "Running SWIG..."
swig -python -c++ -o c_arrays_wrap.cpp c_arrays.i

# Step 2: Compile
echo "Compiling..."
g++ -fPIC -c c_arrays_wrap.cpp $(python3-config --includes) -o c_arrays_wrap.o

# Step 3: Link (platform-specific)
echo "Linking..."
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    echo "Detected macOS"
    g++ -shared c_arrays_wrap.o -o _c_arrays.so -undefined dynamic_lookup
else
    # Linux
    echo "Detected Linux"
    g++ -shared c_arrays_wrap.o -o _c_arrays.so
fi

echo "Build complete! Created _c_arrays.so"
