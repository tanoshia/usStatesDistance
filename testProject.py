import zmq

context = zmq.Context()

#  Socket to talk to server
print("Connecting to zeroMQ test server…")
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

print("Sending request \"A message from who\"...")
socket.send(b"A message from who")

message = socket.recv()
print("A message from %s" % message.decode('utf-8'))
