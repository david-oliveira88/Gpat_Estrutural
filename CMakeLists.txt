cmake_minimum_required(VERSION 3.20)
project(mec5422 LANGUAGES CXX)

# Encontrar Python e suas bibliotecas de desenvolvimento
find_package(Python3 COMPONENTS Development REQUIRED)

# Incluir FetchContent para baixar o pybind11 automaticamente
include(FetchContent)
FetchContent_Declare(
  pybind11
  GIT_REPOSITORY https://github.com/pybind/pybind11
  GIT_TAG        v2.12.0 # Usando uma tag estável para consistência
)
FetchContent_MakeAvailable(pybind11)

# Criar o módulo Python usando o helper do pybind11.
# O nome do módulo importável no Python será "estado_cpp".
pybind11_add_module(estado_cpp SHARED mudar_estado.cpp)

# Definir o padrão do C++
target_compile_features(estado_cpp PRIVATE cxx_std_17)

# Otimizações de compilação para performance
if (MSVC)
  target_compile_options(estado_cpp PRIVATE /O2 /EHsc)
else()
  target_compile_options(estado_cpp PRIVATE -O3 -fvisibility=hidden)
endif()