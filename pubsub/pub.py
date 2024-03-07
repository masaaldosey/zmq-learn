import zmq
import cv2
import numpy as np
import time
import struct

context = zmq.Context()

socket = context.socket(zmq.PUB)
socket.bind("ipc://@camera")

image = cv2.imread("test.jpg", cv2.IMREAD_UNCHANGED).tobytes()
dummy = np.zeros((11608, 8708, 3), "uint8").tobytes()

while True:
    timepart = struct.pack('<d', time.time())
    socket.send_multipart([timepart, dummy], copy=False, track=False)
    print("===Published image===")
