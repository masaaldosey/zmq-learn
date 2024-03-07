#include <zmq.hpp>
#include <iostream>
#include <opencv2/opencv.hpp>

// receive image from publisher
void sub()
{
    zmq::context_t context(1);
    zmq::socket_t socket(context, ZMQ_SUB);
    socket.connect("tcp://localhost:5555");
    socket.setsockopt(ZMQ_SUBSCRIBE, "", 0);

    cv::Mat img;
    zmq::message_t message;
    while (true)
    {
        socket.recv(&message);
        std::string data = std::string(static_cast<char *>(message.data()), message.size());
        img = cv::imdecode(cv::Mat(data), 1);
        cv::imshow("sub", img);
        cv::waitKey(1);
    }
}
int main()
{
}