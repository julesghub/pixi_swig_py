cmake_minimum_required(VERSION 4.0)
project(c_arrays_wrapper LANGUAGES CXX)

# -fPIC -c++ added automatically 
set(CMAKE_CXX_STANDARD 11)
#set(CMAKE_CXX_COMPILER g++)

# Find dependencies
find_package(Python3 COMPONENTS Interpreter Development REQUIRED)
find_package(SWIG 4.0 REQUIRED)
include(UseSWIG)

# Configure SWIG
set(CMAKE_SWIG_FLAGS)
set_property(SOURCE c_arrays.i PROPERTY CPLUSPLUS ON)

# Build SWIG module - this creates a CMake `target`
swig_add_library(mytarget
    TYPE MODULE
    LANGUAGE python
    SOURCES c_arrays.i
)

# Configure target
set_target_properties(mytarget PROPERTIES
    OUTPUT_NAME "_c_arrays"
    PREFIX ""
)
target_include_directories(mytarget PRIVATE ${Python3_INCLUDE_DIRS})

if(APPLE)
# link to python here, not needed for linux, but required for macOS
  target_link_libraries(mytarget PRIVATE Python3::Module)
endif()
