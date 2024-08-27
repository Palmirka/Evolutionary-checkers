cmake_minimum_required(VERSION 3.12)
project(checkers_and_minimax_python_module)

# Znajdź pakiet pybind11
find_package(pybind11 REQUIRED)
find_package(TBB REQUIRED)

# Znajdź pakiet Python
find_package(Python3 COMPONENTS Development REQUIRED)


# Utwórz rozszerzenie
pybind11_add_module(checkers_and_minimax_python_module 
    src/checkers_and_minimax_python_module.cpp
    ../game/minimax_agent/engine.cpp
    ../game/minimax_agent/minimax.cpp
)

target_link_libraries(checkers_and_minimax_python_module PRIVATE TBB::tbb)