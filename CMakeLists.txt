cmake_minimum_required(VERSION 3.15...3.29)
project(pybind11_entry LANGUAGES CXX)

set(PYBIND11_FINDPYTHON ON)

# Find and include pybind11
find_package(pybind11 CONFIG REQUIRED)
find_package(Python3 ${PYBIND11_PYTHON_VERSION} COMPONENTS Interpreter Development)

message("Python_FOUND:${Python_FOUND}")
message("Python_VERSION:${Python_VERSION}")
message("Python_Development_FOUND:${Python_Development_FOUND}")
message("Python_LIBRARIES:${Python_LIBRARIES}")

include_directories(${PYBIND11_INCLUDE_DIRS}
                    /usr/include/python${PYBIND11_PYTHON_VERSION})

# Add the executable (your C++ module)
# add_executable(bfs_module src/cpp/bfs_module.cpp)
pybind11_add_module(bfs_module src/cpp/bfs_module.cpp)

# Link against pybind11 libraries
target_link_libraries(bfs_module PRIVATE ${PYBIND11_LIBRARIES})

# Set C++ standard and flags
set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++14")

# Ensure the output is a shared library for Python import
set_target_properties(bfs_module PROPERTIES
    PREFIX ""
    SUFFIX ".so"
)
install(TARGETS bfs_module DESTINATION .)
