import zmq

context = zmq.Context()

socket = context.socket(zmq.REP)
socket.bind("tcp://127.0.0.1:6001")

while True:
    message = socket.recv().decode("utf-8")
    print(f"Sending {message} World")
    socket.send(f"{message} World".encode("utf-8"))
