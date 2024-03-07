import zmq
import cv2
import time
import struct
import numpy as np

context = zmq.Context()

socket = context.socket(zmq.PUB)

###### TRY IPC and TCP
# socket.bind("inproc://@camera")  # for communication between threads within the same process
socket.bind("ipc:///tmp/camera")  # make sure folders are created (/tmp)
# socket.bind("ipc://@camera")  # automatically use an abstract namespace
# socket.bind("tcp://127.0.0.1:5555")  # over network

# load image from webcam
cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    if not ret:
        break
    rows, cols, nchannels = frame.shape
    data_type = frame.dtype.itemsize

    ####### TRY webcam, 5MP and 100MP
    bytesStream = frame.tobytes()  # webcam
    # bytesStream = np.zeros((2592, 1944, 3), 'uint8').tobytes()  # 5MP
    # bytesStream = np.zeros((11608, 8708, 3), 'uint8').tobytes()  # 100MP
    
    timestamp = time.time()  # assuming capture time ...
    metadata = struct.pack('<IIIId', rows, cols, nchannels, data_type, timestamp)  # lazyman serialization. Use protobuf, msgpack or rapidjson for production
    
    ###### TRY copy and no copy. TRY track and no track (careful of False and False)
    tracker = socket.send_multipart([metadata, bytesStream], copy=True, track=False)
    if tracker is not None:
        tracker.wait()
    new = time.time()
    print("Message is sent in ms: ", (new - timestamp) * 1000)
cap.release()
