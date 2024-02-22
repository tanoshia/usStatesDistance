# US States Distance
Input: [state1,state2] <br>
this service calculates the distance between the two states [capital cities] in miles, and the cardinal direction from state1 to state2 <br>
Output: [distance,direction] <br>

Example input: ['California','Washington'] <br>
Example output: [589,'North'] <br>

Notes: <br>
- invalid (non-US state name) input will result in [None,None] output <br>
- input is case insensative <br>
- test this code out locally via testProject.py which provides an example client to the microservice, run after microservice is running <br>


required libraries: <br>
- pyzmq      (ZeroMQ for communication) <br>
- geopandas  (to read and interpret the US states map) <br>
    - pip install pyzmq geopandas <br>

## UML 
<img width="1326" alt="Screenshot 2024-02-21 at 7 13 02 PM" src="https://github.com/tanoshia/usStatesDistance/assets/123522018/9ceccd01-87b8-4e70-b59a-7487d08005d3">
