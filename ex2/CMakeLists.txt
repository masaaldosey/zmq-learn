cmake_minimum_required(VERSION 3.10.2)

project(zmqsubex VERSION 0.0.1)

find_package(OpenCV REQUIRED)
find_package(yaml-cpp REQUIRED)
find_package(cppzmq REQUIRED)

add_executable(sub sub.cpp)
target_link_libraries(sub ${OpenCV_LIBS} libzmq cppzmq yaml-cpp)
target_include_directories(sub PUBLIC ${zmq_INCLUDE_DIRS})

