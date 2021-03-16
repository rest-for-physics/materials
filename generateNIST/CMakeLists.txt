cmake_minimum_required(VERSION 3.16)
project(generateNIST)

set(CMAKE_CXX_STANDARD 14)

find_package(Geant4 REQUIRED)

add_executable(${PROJECT_NAME} main.cpp)

target_link_libraries(${PROJECT_NAME} ${Geant4_LIBRARIES})
