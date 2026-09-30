cmake_minimum_required(VERSION 3.24)

project(CubeSE VERSION 1.0.0 LANGUAGES CXX)

include(FetchContent)

FetchContent_Declare(
  rapidjson
  GIT_REPOSITORY https://github.com/Tencent/rapidjson.git
  GIT_TAG f54b0e47a08782a6131cc3d60f94d038fa6e0a51
  GIT_SHALLOW TRUE
  # RapidJSON is used as a header-only dependency. Avoid configuring its
  # examples and tests as part of the CubeSE build.
  SOURCE_SUBDIR cmake/headers-only
)
FetchContent_MakeAvailable(rapidjson)

add_executable(cubese-engine CubeSE.cpp)
set_target_properties(cubese-engine PROPERTIES OUTPUT_NAME CubeSE)

target_compile_features(cubese-engine PRIVATE cxx_std_20)
target_include_directories(
  cubese-engine
  PRIVATE "${rapidjson_SOURCE_DIR}/include/rapidjson"
)

if(MSVC)
  target_compile_options(cubese-engine PRIVATE /W3 /permissive-)
else()
  target_compile_options(cubese-engine PRIVATE -Wall -Wextra -Wpedantic)
endif()
