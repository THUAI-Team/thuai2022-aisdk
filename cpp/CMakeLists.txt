cmake_minimum_required(VERSION 3.10)

project(THUAIEgg2021AI)
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED True)

if(CMAKE_BUILD_TYPE MATCHES "Debug")
  add_compile_definitions(DEBUG)
endif()
message("Build type: ${CMAKE_BUILD_TYPE}")

file(GLOB SOURCES "*.cpp")
add_executable(AI ${SOURCES})