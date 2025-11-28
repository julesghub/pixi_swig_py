cmake_minimum_required(VERSION 4.0)
project(c_arrays_wrapper LANGUAGES CXX)

# Set C++ standard
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# Find Python3
find_package(Python3 COMPONENTS Interpreter Development.Module REQUIRED)
message(STATUS "Python3 found: ${Python3_EXECUTABLE}")
message(STATUS "Python3 version: ${Python3_VERSION}")
message(STATUS "Python3 include dirs: ${Python3_INCLUDE_DIRS}")

# Find SWIG
find_package(SWIG 4.0 REQUIRED)
include(UseSWIG)
message(STATUS "SWIG found: ${SWIG_EXECUTABLE}")
message(STATUS "SWIG version: ${SWIG_VERSION}")

# Configure SWIG options (don't include -python, it's automatic)
set(CMAKE_SWIG_FLAGS -c++ -Wall)

# Platform-specific configuration
if(APPLE)
    message(STATUS "Configuring for macOS")
    
    # macOS: Use undefined dynamic_lookup for Python extensions
    set(CMAKE_SHARED_LINKER_FLAGS 
        "${CMAKE_SHARED_LINKER_FLAGS} -undefined dynamic_lookup")
    
    # Suppress new linker warnings in Xcode 15+
    if(CMAKE_CXX_COMPILER_VERSION VERSION_GREATER_EQUAL 15.0)
        set(CMAKE_SHARED_LINKER_FLAGS 
            "${CMAKE_SHARED_LINKER_FLAGS} -Wl,-w")
    endif()
    
    # Set minimum macOS version
    if(NOT CMAKE_OSX_DEPLOYMENT_TARGET)
        set(CMAKE_OSX_DEPLOYMENT_TARGET "10.14" CACHE STRING 
            "Minimum macOS deployment version")
    endif()
    message(STATUS "macOS deployment target: ${CMAKE_OSX_DEPLOYMENT_TARGET}")
    
elseif(UNIX AND NOT APPLE)
    message(STATUS "Configuring for Linux")
    
elseif(WIN32)
    message(STATUS "Configuring for Windows")
endif()

# Set SWIG module properties
set_property(SOURCE c_arrays.i PROPERTY CPLUSPLUS ON)
set_property(SOURCE c_arrays.i PROPERTY SWIG_MODULE_NAME c_arrays)

# Create SWIG library
swig_add_library(c_arrays
    TYPE MODULE
    LANGUAGE python
    SOURCES c_arrays.i
)

# Set target properties
set_target_properties(c_arrays PROPERTIES
    OUTPUT_NAME "_c_arrays"
    PREFIX ""
)

# Include Python headers
target_include_directories(c_arrays PRIVATE 
    ${Python3_INCLUDE_DIRS}
)

# Link Python libraries (platform-specific)
if(APPLE)
    # On macOS, we use dynamic_lookup
    message(STATUS "Using dynamic_lookup for Python symbols (macOS)")
else()
    # On Linux, Windows, link against Python
    target_link_libraries(c_arrays PRIVATE Python3::Module)
    message(STATUS "Linking against Python3::Module")
endif()

# Compiler warnings
#target_compile_options(c_arrays PRIVATE
#    $<$<CXX_COMPILER_ID:GNU,Clang,AppleClang>:-Wall -Wextra>
#    $<$<CXX_COMPILER_ID:MSVC>:/W4>
#)

# CRITICAL: Set the output directory properly
# This ensures the .so file goes where setup.py expects it
if(CMAKE_LIBRARY_OUTPUT_DIRECTORY)
    # If setup.py set this, use it
    set_target_properties(c_arrays PROPERTIES
        LIBRARY_OUTPUT_DIRECTORY "${CMAKE_LIBRARY_OUTPUT_DIRECTORY}"
    )
else()
    # Otherwise use the build directory
    set_target_properties(c_arrays PROPERTIES
        LIBRARY_OUTPUT_DIRECTORY "${CMAKE_CURRENT_BINARY_DIR}"
    )
endif()

# Installation rules - install both the .so and .py files
install(TARGETS c_arrays 
    LIBRARY DESTINATION ${CMAKE_INSTALL_PREFIX}
    RUNTIME DESTINATION ${CMAKE_INSTALL_PREFIX}
)

# Install the generated Python wrapper
install(FILES "${CMAKE_CURRENT_BINARY_DIR}/c_arrays.py" 
    DESTINATION ${CMAKE_INSTALL_PREFIX}
)

# Print configuration summary
message(STATUS "")
message(STATUS "========================================")
message(STATUS "Configuration Summary")
message(STATUS "========================================")
message(STATUS "CMake version:        ${CMAKE_VERSION}")
message(STATUS "System:               ${CMAKE_SYSTEM_NAME}")
message(STATUS "Processor:            ${CMAKE_SYSTEM_PROCESSOR}")
message(STATUS "C++ Compiler:         ${CMAKE_CXX_COMPILER_ID} ${CMAKE_CXX_COMPILER_VERSION}")
message(STATUS "Python version:       ${Python3_VERSION}")
message(STATUS "Python executable:    ${Python3_EXECUTABLE}")
message(STATUS "SWIG version:         ${SWIG_VERSION}")
message(STATUS "Build type:           ${CMAKE_BUILD_TYPE}")
message(STATUS "Output directory:     ${CMAKE_LIBRARY_OUTPUT_DIRECTORY}")
if(APPLE)
    message(STATUS "macOS target:         ${CMAKE_OSX_DEPLOYMENT_TARGET}")
endif()
message(STATUS "========================================")
message(STATUS "")
