cmake_minimum_required(VERSION 3.15)
project(pixi_swig_py LANGUAGES C)

# Find SWIG
find_package(SWIG REQUIRED)
include(${SWIG_USE_FILE})

# Find Python
find_package(Python3 REQUIRED COMPONENTS Interpreter Development)

# Set SWIG properties
set(CMAKE_SWIG_FLAGS "")
set_source_files_properties(src/example.i PROPERTIES CPLUSPLUS OFF)

# Include directories
include_directories(${Python3_INCLUDE_DIRS})
include_directories(${CMAKE_CURRENT_SOURCE_DIR}/src)

# Create the SWIG module
swig_add_library(example
    TYPE SHARED
    LANGUAGE python
    SOURCES src/example.i src/example.c
)

# Link Python libraries
target_link_libraries(example ${Python3_LIBRARIES})

# Set output directory
set_target_properties(example PROPERTIES
    LIBRARY_OUTPUT_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/lib
)

# Copy generated Python file to lib directory
add_custom_command(TARGET example POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy
        ${CMAKE_CURRENT_BINARY_DIR}/example.py
        ${CMAKE_CURRENT_SOURCE_DIR}/lib/example.py
)
