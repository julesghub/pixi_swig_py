from setuptools import setup, Extension
import sys
import os

# Determine the module name and package structure
module_name = "c_arrays"
package_name = "jpack"

# Create the SWIG extension
c_arrays_module = Extension(
    name=f"{package_name}._{module_name}",
    sources=["c_arrays.i"],
    swig_opts=[
        "-python",
        "-c++",  # Use if you have C++ code
        "-Wall",  # Show warnings
    ],
    extra_compile_args=["-std=c++11"] if sys.platform != "win32" else [],
)

setup(
    name="underworld-c-arrays",
    version="1.0.0",
    description="SWIG wrappers for C arrays",
    ext_modules=[c_arrays_module],
    py_modules=[f"{package_name}.{module_name}"],
)
