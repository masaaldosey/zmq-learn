import zmq

context = zmq.Context()

socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:6001")

socket.send(b"Hello")
response = socket.recv().decode("utf-8")
print(response)
