import zmq
from time import sleep
from datetime import datetime

context = zmq.Context()

socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:6001")

while True:
    sleep(0.2)
    socket.send(b"Hello")
    response = socket.recv().decode("utf-8")
    print(f"{datetime.now()} | {response}")
