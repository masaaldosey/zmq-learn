#include <yaml-cpp/yaml.h>
#include <opencv2/opencv.hpp>
#include <zmq.hpp>
#include <iostream>
#include <chrono>

int main() {

    // load yaml config
    YAML::Node config = YAML::LoadFile("config.yaml");
    std::string zmqEndPoint = config["zmqEndPoint"].as<std::string>();
    std::cout << "zmqEndPoint: " << zmqEndPoint << std::endl;

    // create a zmq context
    zmq::context_t context(1);
    // create a zmq socket
    zmq::socket_t socket(context, ZMQ_SUB);
    // connect to the server
    socket.connect(zmqEndPoint);
    socket.setsockopt(ZMQ_SUBSCRIBE, "", 0);

    int rows, cols, nchannels, data_type, data_size;
    double timestamp;

    while(true) {

        // Receive the metadata and image data through ZMQ
        zmq::message_t metadata_msg, image_msg;
        socket.recv(metadata_msg);
        socket.recv(image_msg);
        auto current_time = std::chrono::system_clock::now();


        // Unpack the metadata from the struct
        const uchar* metadata_ptr = static_cast<const uchar*>(metadata_msg.data());
        std::memcpy(&rows, metadata_ptr, sizeof(int));
        std::memcpy(&cols, metadata_ptr + sizeof(int), sizeof(int));
        std::memcpy(&nchannels, metadata_ptr + 2 * sizeof(int), sizeof(int));
        std::memcpy(&data_type, metadata_ptr + 3 * sizeof(int), sizeof(int));
        std::memcpy(&timestamp, metadata_ptr + 4 * sizeof(int), sizeof(double));

        // // Create a cv::Mat from the received data
        auto image = cv::Mat(rows, cols, nchannels == 3 ? CV_8UC3 : CV_8U, image_msg.data());

        int queue_size = socket.get(zmq::sockopt::rcvhwm);
        std::cout << "Current queue size: " << queue_size << std::endl;

        auto clock = std::chrono::duration_cast<std::chrono::nanoseconds>(current_time.time_since_epoch()).count() / 1000000.0;
        double latency = clock - timestamp * 1000.0;

        // Print the received metadata
        std::cout << "Rows: " << rows << std::endl;
        std::cout << "Cols: " << cols << std::endl;
        std::cout << "nchannels: " << nchannels << std::endl;
        std::cout << "Latency: " << latency << " ms" << std::endl;
        std::cout << "=============================" << std::endl;

        // Display the received image
        cv::imshow("Received Image", image);
        cv::waitKey(1);
    }

    return 0;
}
