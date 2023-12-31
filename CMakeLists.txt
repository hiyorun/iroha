cmake_minimum_required(VERSION 3.12)
project(iroha)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++17")
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

file(GLOB_RECURSE SRCFILES CONFIGURE_DEPENDS "src/*.cpp" "src/engine/*.cpp")

add_library(inja INTERFACE)
add_library(nlohmann_json INTERFACE)
add_subdirectory(third-party/google-mcu)

add_executable(iroha ${SRCFILES})

find_package(absl CONFIG REQUIRED)
find_package(ImageMagick COMPONENTS Magick++ REQUIRED)

include_directories(${ImageMagick_INCLUDE_DIRS})

target_include_directories(inja INTERFACE third-party/inja)
target_include_directories(nlohmann_json INTERFACE third-party/json)
target_link_libraries(iroha PRIVATE MaterialColorUtility absl::flat_hash_map ${ImageMagick_LIBRARIES} nlohmann_json inja)