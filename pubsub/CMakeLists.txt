cmake_minimum_required(VERSION 3.15.0)

project(sub)

find_package(OpenCV REQUIRED)
find_package(cppzmq REQUIRED)

add_executable(sub sub.cpp)
target_link_libraries(sub PUBLIC cppzmq ${OpenCV_LIBS})
target_include_directories(sub PUBLIC ${OpenCV_INCLUDE_DIRS})