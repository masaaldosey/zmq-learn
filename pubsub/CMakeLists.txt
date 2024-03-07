cmake_minimum_required(VERSION 3.15.0)

project(sub)

find_package(OpenCV REQUIRED)
find_package(cppzmq REQUIRED)

add_executable(sub sub.cpp)
target_link_libraries(sub PRIVATE cppzmq ${OpenCV_LIBS})
target_include_directories(sub PRIVATE ${OpenCV_INCLUDE_DIRS} ${cppzmq_INCLUDE_DIRS})