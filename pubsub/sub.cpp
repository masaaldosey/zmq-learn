#include <zmq.hpp>
#include <opencv2/opencv.hpp>
#include <iostream>
#include <chrono>

// receive image from publisher
int main()
{
    zmq::context_t context(1);
    zmq::socket_t subscriber(context, ZMQ_SUB);

    subscriber.connect("ipc://@camera");
    subscriber.setsockopt(ZMQ_SUBSCRIBE, "", 0);

    while (true)
    {
        // Receive the timestamp
        zmq::message_t timestampMsg;
        subscriber.recv(&timestampMsg);

        // Receive the image
        zmq::message_t imageMsg;
        subscriber.recv(&imageMsg);

        double timestamp = 0.0;
        const uchar *metadata_ptr = static_cast<const uchar *>(timestampMsg.data());
        std::memcpy(&timestamp, metadata_ptr, sizeof(double));

        // Access the image data directly
        uchar *imageData = imageMsg.data<uchar>();
        size_t imageSize = imageMsg.size();

        // Get current time_point
        auto currentTimePoint = std::chrono::system_clock::now();

        // Compute the difference in seconds
        auto current = std::chrono::duration_cast<std::chrono::nanoseconds>(currentTimePoint.time_since_epoch()).count() / 1000000.0;
        auto difference = current - timestamp * 1000.0;
        std::cout << "timestamp = " << timestamp * 1000 << " ms" << std::endl;
        std::cout << "current = " << current << " ms" << std::endl;
        std::cout << "Latency = " << difference << " ms" << std::endl;

        std::cout << "received" << std::endl;
    }

    return EXIT_SUCCESS;
}