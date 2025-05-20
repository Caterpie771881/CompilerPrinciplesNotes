cmake_minimum_required(VERSION 3.10)

project(ezVM VERSION 1.0.0)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED True)

set(SOURCE_DIR "src")
set(INCLUDE_DIR "include")

include_directories(${INCLUDE_DIR})

file(GLOB SOURCE_FILES "${SOURCE_DIR}/*.cpp")

add_executable(${PROJECT_NAME} ${SOURCE_FILES})

# target_compile_options(${PROJECT_NAME} PRIVATE -Wall -Wextra -Wpedantic)

# target_link_libraries(${PROJECT_NAME} PRIVATE some_library)
