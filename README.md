# US States Distance
this service calculates the distance smallest between the two states in miles +/- 1 mile, and the cardinal direction from state1 to state2 <br>

Input: [state1,state2] <br>
Output: [distance,direction] <br>

Example input: ['California','Washington'] <br>
Example output: [589,'North'] <br>

required libraries:
- pyzmq      (ZeroMQ for communication) <br>
- geopandas  (to read and interpret the US states map) <br>
    - pip install pyzmq geopandas <br>

Notes:
- invalid (non-US state name) input will result in [None,None] output <br>
- input is case insensative <br>
- test this code out locally via testProject.py which provides an example client to the microservice, run after microservice is running <br>
<br>

## Request
Requesting data from this microservice requires opening the socket locally for zeroMQ to connect to: 
```
    import zmg
    import json
    context = zmq.Context()  
    socket = context.socket(zmq.REQ)  
    socket.connect("tcp://localhost:5555")  
    ...
    socket.send_json(["state1", "state2"])
```
<br>

## Receive
Receiving data from this microservice requires this socket command: 
```
    message = socket.recv()
```
Which could be decoded with 
```
    % message.decode('utf-8')
```
<br>

## UML:
<img width="1326" alt="Simple UML Sequence Diagram" src="https://github.com/tanoshia/usStatesDistance/assets/123522018/9ceccd01-87b8-4e70-b59a-7487d08005d3">

## UML (detailed):
<img width="997" alt="Screenshot 2024-02-21 at 7 29 18 PM" src="https://github.com/tanoshia/usStatesDistance/assets/123522018/13a60997-7a77-4905-baaf-53048151056f">
