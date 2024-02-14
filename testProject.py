import time
import zmq
import json

context = zmq.Context()

#  Socket to talk to server
print("Connecting to zeroMQ test server…")
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")



def main():
    multiTest()


def repeatSingleTest():
    while True:
        print("SENDING:  \"A message from Alpha\"")
        states = ["California", "Washington"]

        # serialize data to JSON string and send
        socket.send_json(states)

        message = socket.recv()
        print("RECIEVED:  A message from %s" % message.decode('utf-8'),"\n")

        time.sleep(4)

def multiTest():
    print("SENDING:  \"A message from Alpha\"")
    testCases = [
        ["California","California"],
        ["California","Oregon"],
        ["California","Washington"],
        ["California","Nevada"],
        ["California","New York"],
        ["New York","California"],
        ["Minnesota","Texas"],
        ["Florida","Washington"],
        ["Florida","Narnia"],
        ["Narnia","Florida"],
        ["Narnia","Middle Earth"]
    ]
    for testCases in testCases:
        # serialize data to JSON string and send
        socket.send_json(testCases)

        message = socket.recv()
        print("RECIEVED:  A message from %s" % message.decode('utf-8'),"\n")

        time.sleep(4)



main()