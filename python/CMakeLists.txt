# Python bindings for fTetWild
cmake_minimum_required(VERSION 3.20)

# Find Python and pybind11
find_package(Python COMPONENTS Interpreter Development REQUIRED)
find_package(pybind11 CONFIG QUIET)

if(NOT pybind11_FOUND)
    message(STATUS "pybind11 not found, attempting to use pip installed version")
    execute_process(
        COMMAND ${Python_EXECUTABLE} -m pybind11 --cmakedir
        OUTPUT_VARIABLE pybind11_DIR
        OUTPUT_STRIP_TRAILING_WHITESPACE
        RESULT_VARIABLE pybind11_RESULT
    )
    if(pybind11_RESULT EQUAL 0)
        find_package(pybind11 CONFIG REQUIRED PATHS ${pybind11_DIR})
    else()
        message(FATAL_ERROR "pybind11 is required for Python bindings. Install with: pip install pybind11")
    endif()
endif()

# Create the Python module
pybind11_add_module(ftetwild
    ftetwild_pybind.cpp
)

# Link against the fTetWild library
target_link_libraries(ftetwild PRIVATE FloatTetwild)

# Set output directory
set_target_properties(ftetwild PROPERTIES
    LIBRARY_OUTPUT_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}
)

# Install the module
install(TARGETS ftetwild
    LIBRARY DESTINATION .
)
