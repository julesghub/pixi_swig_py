"""
Setup script using CMake 4.0+ to build SWIG extensions
"""
import os
import sys
import subprocess
import shutil
import re
from pathlib import Path
from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext


def get_cmake_version():
    """Get CMake version and check if it's 4.0+"""
    try:
        output = subprocess.check_output(
            ['cmake', '--version'], 
            stderr=subprocess.STDOUT,
            text=True
        )
        match = re.search(r'cmake version (\d+\.\d+\.\d+)', output, re.IGNORECASE)
        if match:
            version_str = match.group(1)
            major, minor, patch = map(int, version_str.split('.'))
            return version_str, (major, minor, patch)
    except Exception as e:
        print(f"Error getting CMake version: {e}")
    return None, (0, 0, 0)


class CMakeExtension(Extension):
    """Extension class for CMake-based builds"""
    
    def __init__(self, name, sourcedir=""):
        super().__init__(name, sources=[])
        self.sourcedir = os.path.abspath(sourcedir)


class CMakeBuild(build_ext):
    """Custom build_ext command that uses CMake 4.0+"""
    
    def run(self):
        # Check CMake availability and version
        cmake_version_str, cmake_version_tuple = get_cmake_version()
        
        if cmake_version_str is None:
            raise RuntimeError(
                "CMake must be installed to build this extension.\n"
                "Download from: https://cmake.org/download/"
            )
        
        print(f"Found CMake version: {cmake_version_str}")
        
        # Check for CMake 4.0+
        if cmake_version_tuple < (4, 0, 0):
            raise RuntimeError(
                f"CMake >= 4.0.0 is required, but found {cmake_version_str}\n"
                f"Please upgrade CMake from: https://cmake.org/download/"
            )
        
        for ext in self.extensions:
            self.build_extension(ext)
    
    def build_extension(self, ext):
        extdir = os.path.abspath(
            os.path.dirname(self.get_ext_fullpath(ext.name))
        )
        
        if not extdir.endswith(os.path.sep):
            extdir += os.path.sep
        
        # Detect debug build
        debug = int(os.environ.get('DEBUG', 0)) if self.debug is None else self.debug
        cfg = 'Debug' if debug else 'Release'
        
        # CMake configuration arguments
        cmake_args = [
            f"-DCMAKE_LIBRARY_OUTPUT_DIRECTORY={extdir}",
            f"-DCMAKE_INSTALL_PREFIX='../..'", # install path in project root dir
            f"-DPYTHON_EXECUTABLE={sys.executable}",
            f"-DCMAKE_BUILD_TYPE={cfg}",
        ]
        
        # Build arguments
        build_args = ['--config', cfg]
        
        # Platform-specific settings
        if sys.platform.startswith("darwin"):
            # macOS
            cmake_args.extend([
                "-DCMAKE_OSX_DEPLOYMENT_TARGET=10.14",
            ])
            
            # Detect Apple Silicon
            import platform
            if platform.machine() == 'arm64':
                print("Building for Apple Silicon (arm64)")
                cmake_args.append("-DCMAKE_OSX_ARCHITECTURES=arm64")
            elif platform.machine() == 'x86_64':
                print("Building for Intel (x86_64)")
                cmake_args.append("-DCMAKE_OSX_ARCHITECTURES=x86_64")
            
            print("Using clang with dynamic_lookup for macOS")
        
        elif sys.platform.startswith("linux"):
            print("Building for Linux")
            
        elif sys.platform.startswith("win"):
            print("Building for Windows")
            cmake_args.extend([
                f"-DCMAKE_LIBRARY_OUTPUT_DIRECTORY_{cfg.upper()}={extdir}",
            ])
        
        # Parallel build
        if hasattr(self, 'parallel') and self.parallel:
            build_args.extend(['--parallel', str(self.parallel)])
        else:
            # Use available CPU cores
            try:
                import multiprocessing
                num_cpus = multiprocessing.cpu_count()
                build_args.extend(['--parallel', str(num_cpus)])
                print(f"Building with {num_cpus} parallel jobs")
            except:
                pass
        
        # Create build directory
        build_temp = Path(self.build_temp)
        build_temp.mkdir(parents=True, exist_ok=True)
        
        # Run CMake configuration
        print("\n" + "="*60)
        print("Running CMake Configuration")
        print("="*60)
        print(f"Source dir:  {ext.sourcedir}")
        print(f"Build dir:   {self.build_temp}")
        print(f"Install dir: {extdir}")
        print(f"CMake args:  {' '.join(cmake_args)}")
        print("="*60 + "\n")
        
        subprocess.check_call(
            ["cmake", ext.sourcedir] + cmake_args,
            cwd=self.build_temp,
            stdout=sys.stdout,
            stderr=sys.stderr
        )
        
        # Run CMake build
        print("\n" + "="*60)
        print("Running CMake Build")
        print("="*60)
        print(f"Build args: {' '.join(build_args)}")
        print("="*60 + "\n")
        
        subprocess.check_call(
            ["cmake", "--build", "."] + build_args,
            cwd=self.build_temp,
            stdout=sys.stdout,
            stderr=sys.stderr
        )
        
        # Run CMake install to copy files to the right location
        print("\n" + "="*60)
        print("Running CMake Install")
        print("="*60 + "\n")
        
        subprocess.check_call(
            ["cmake", "--install", ".", "--prefix", extdir],
            cwd=self.build_temp,
            stdout=sys.stdout,
            stderr=sys.stderr
        )
        
        # Verify the files were created
        so_file = os.path.join(extdir, "_c_arrays.so")
        py_file = os.path.join(extdir, "c_arrays.py")
        
        if os.path.exists(so_file):
            print(f"✓ Found compiled extension: {so_file}")
        else:
            print(f"⚠ Warning: Compiled extension not found at {so_file}")
            # Try to find it in build directory
            build_so = os.path.join(self.build_temp, "_c_arrays.so")
            if os.path.exists(build_so):
                print(f"  Found in build dir, copying...")
                shutil.copy2(build_so, so_file)
        
        if os.path.exists(py_file):
            print(f"✓ Found Python wrapper: {py_file}")
        else:
            print(f"⚠ Warning: Python wrapper not found at {py_file}")
            # Try to find it in build directory
            build_py = os.path.join(self.build_temp, "c_arrays.py")
            if os.path.exists(build_py):
                print(f"  Found in build dir, copying...")
                shutil.copy2(build_py, py_file)


# Read README if it exists
long_description = ""
readme_path = Path("README.md")
if readme_path.exists():
    long_description = readme_path.read_text(encoding="utf-8")

# Setup configuration - NOW WITH CONSISTENT NAMING
setup(
    name="c_arrays",  # Changed from "c-arrays" to "c_arrays"
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="SWIG wrapper for C arrays using CMake 4.0+",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/c_arrays",
    ext_modules=[CMakeExtension("c_arrays")],
    cmdclass={"build_ext": CMakeBuild},
    zip_safe=False,
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: C++",
        "Topic :: Software Development :: Libraries",
    ],
)
