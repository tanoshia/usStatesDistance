import time
import zmq

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

while True:
    #  Wait for next request from client
    message = socket.recv()
    print("Received request: %s" % message.decode('utf-8'))

    #  Do some 'work'
    time.sleep(1)

    #  Send reply back to client
    print("Sending reply \"CS361\"...")
    socket.send(b"CS361")