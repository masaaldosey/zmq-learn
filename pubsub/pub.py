import zmq
import cv2
from datetime import datetime

context = zmq.Context()

socket = context.socket(zmq.PUB)
socket.connect("tcp://localhost:6001")

image = cv2.imread("test.jpg", cv2.IMREAD_UNCHANGED)

while True:
    socket.send(image.tobytes())
    print(f"{datetime.now()} | Published image")
