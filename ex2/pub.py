import zmq
import cv2
import time
import struct
import numpy as np

context = zmq.Context()

socket = context.socket(zmq.REP)
# socket = context.socket(zmq.PUB)

# IPC and TCP
# socket.bind("inproc://@camera")               # For communication between threads within the same process
socket.bind("ipc:///tmp/camera")              # Make sure folders are created (/tmp)
# socket.bind("ipc://@camera")                  # Automatically use an abstract namespace
# socket.bind("tcp://127.0.0.1:6868")             # Over network

# load image from webcam
cap = cv2.VideoCapture(0)
while True:
    socket.recv()

    ret, frame = cap.read()
    if not ret:
        break
    
    # Webcam, 5MP and 100MP
    # image = frame.astype('uint8')                                 # Webcam
    image = np.zeros((2592, 1944, 3), 'uint8')                      # 5MP
    # image = np.zeros((11608, 8708, 3), 'uint8')                   # 100MP
    image[0:frame.shape[0], 0:frame.shape[1]] = frame               # Copy to the top-left corner
    bytesStream = image.tobytes()
    rows, cols, nchannels = image.shape
    data_type = image.dtype.itemsize

    timestamp = time.time()                                                        # Assuming capture time
    metadata = struct.pack('<IIIId', rows, cols, nchannels, data_type, timestamp)  # Lazyman's serialization. Use protobuf, msgpack or rapidjson for production
    
    # Copy and no copy. Track and no track (careful of False and False)
    tracker = socket.send_multipart([metadata, bytesStream], copy=False, track=False)
    if tracker is not None:
        tracker.wait()
    new = time.time()
    print("Message is sent in ms: ", (new - timestamp) * 1000)
cap.release()
