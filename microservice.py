import time
import zmq
import json
import math

state_capitals = {
    "Alabama":          ("Montgomery", 32.3792, -86.3077),
    "Alaska":           ("Juneau", 58.3019, -134.4197),
    "Arizona":          ("Phoenix", 33.4484, -112.0740),
    "Arkansas":         ("Little Rock", 34.7465, -92.2896),
    "California":       ("Sacramento", 38.5758, -121.4789),
    "Colorado":         ("Denver", 39.7392, -104.9903),
    "Connecticut":      ("Hartford", 41.7658, -72.6734),
    "Delaware":         ("Dover", 39.1582, -75.5244),
    "Florida":          ("Tallahassee", 30.4383, -84.2807),
    "Georgia":          ("Atlanta", 33.7490, -84.3880),
    "Hawaii":           ("Honolulu", 21.3069, -157.8583),
    "Idaho":            ("Boise", 43.6150, -116.2023),
    "Illinois":         ("Springfield", 39.7980, -89.6544),
    "Indiana":          ("Indianapolis", 39.7684, -86.1581),
    "Iowa":             ("Des Moines", 41.5868, -93.6250),
    "Kansas":           ("Topeka", 39.0489, -95.6780),
    "Kentucky":         ("Frankfort", 38.2009, -84.8733),
    "Louisiana":        ("Baton Rouge", 30.4515, -91.1871),
    "Maine":            ("Augusta", 44.3106, -69.7795),
    "Maryland":         ("Annapolis", 38.9784, -76.4922),
    "Massachusetts":    ("Boston", 42.3601, -71.0589),
    "Michigan":         ("Lansing", 42.7325, -84.5555),
    "Minnesota":        ("Saint Paul", 44.9537, -93.0900),
    "Mississippi":      ("Jackson", 32.2998, -90.1848),
    "Missouri":         ("Jefferson City", 38.5767, -92.1735),
    "Montana":          ("Helena", 46.5884, -112.0245),
    "Nebraska":         ("Lincoln", 40.8136, -96.7026),
    "Nevada":           ("Carson City", 39.1638, -119.7674),
    "New Hampshire":    ("Concord", 43.2081, -71.5376),
    "New Jersey":       ("Trenton", 40.2206, -74.7699),
    "New Mexico":       ("Santa Fe", 35.6870, -105.9378),
    "New York":         ("Albany", 42.6526, -73.7562),
    "North Carolina":   ("Raleigh", 35.7796, -78.6382),
    "North Dakota":     ("Bismarck", 46.8083, -100.7837),
    "Ohio":             ("Columbus", 39.9612, -82.9988),
    "Oklahoma":         ("Oklahoma City", 35.4676, -97.5164),
    "Oregon":           ("Salem", 44.9429, -123.0351),
    "Pennsylvania":     ("Harrisburg", 40.2732, -76.8867),
    "Rhode Island":     ("Providence", 41.8240, -71.4128),
    "South Carolina":   ("Columbia", 34.0007, -81.0348),
    "South Dakota":     ("Pierre", 44.3683, -100.3510),
    "Tennessee":        ("Nashville", 36.1627, -86.7816),
    "Texas":            ("Austin", 30.2672, -97.7431),
    "Utah":             ("Salt Lake City", 40.7608, -111.8910),
    "Vermont":          ("Montpelier", 44.2601, -72.5754),
    "Virginia":         ("Richmond", 37.5407, -77.4360),
    "Washington":       ("Olympia", 47.0379, -122.9007),
    "West Virginia":    ("Charleston", 38.3498, -81.6326),
    "Wisconsin":        ("Madison", 43.0731, -89.4012),
    "Wyoming":          ("Cheyenne", 41.1400, -104.8202),
}

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

def takeRequests():
    lastInput = ["last"]
    while True:
        # wait for next request from client
        statesInput = socket.recv_json()
        lastInput = statesInput
        print("RECIEVED: %s" % statesInput)

        state1 = statesInput[0]
        state2 = statesInput[1]
        print("   State1:", state1)
        print("   State2:", state2)
        
        if statesInput != None and statesInput != lastInput:
            return statesInput


def sendReply(distance, direction, capital = False): # capitals being an optional var until full state lines func done
    # create array in format to send
    result = [distance,direction]
    if capital:
        result.append(capital)
    # do some 'work'
    time.sleep(1)

    # send reply back to client
    print("SENDING: ",result,"\n")
    socket.send_json(result)




def stateCapitalLat(state): # helper
    try:
        _, lat, _ = state_capitals[state]  # _ ignores that column
        return lat
    except KeyError:  # case that state not found
        return None
    
def stateCapitalLon(state): # helper
    try:
        _, _, lon = state_capitals[state]  # _ ignores that column
        return lon
    except KeyError:  # case that state not found
        return None



# state capital distances
    
def calcDistance(state1, state2): # prep states input for haversine formula 
    lat1 = stateCapitalLat(state1)
    lon1 = stateCapitalLon(state1)
    lat2 = stateCapitalLat(state2)
    lon2 = stateCapitalLon(state2)
    
    if lat1 == None:
        print(state1," does not exist")
        return
    if lat2 == None:
        print(state2,"does not exist")
        return
    distance = haversineDistanceFromula(lat1, lon1, lat2, lon2)

    return distance

def haversineDistanceFromula(lat1, lon1, lat2, lon2): # uses Haversine formula 
    R = 3958.8 # Earths radius in miles (6371.0km)

    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    
    # difference in coords
    diffLat = lat2 - lat1
    diffLon = lon2 - lon1
    
    # Haversine formula, don't question it
    a = math.sin(diffLat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(diffLon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    
    return distance




# cardinal directions (bearingToCardinal(calcBearing(lat1, lon1, lat2, lon2)))

def calcBearing(lat1, lon1, lat2, lon2): # helper
    # Convert latitude and longitude from degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    diffLon = lon2 - lon1

    x = math.sin(diffLon) * math.cos(lat2)
    y = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1) * math.cos(lat2) * math.cos(diffLon))

    initialBearing = math.atan2(x, y)

    # Convert from radians to degrees
    initialBearing = math.degrees(initialBearing)
    compassBearing = (initialBearing + 360) % 360

    return compassBearing

def bearingToCardinal(bearing): # helper
    cardinalPoints = ["North", "Northeast", "East", "Southeast", "South", "Southwest", "West", "Northwest", "North"]
    return cardinalPoints[int((bearing + 22.5) // 45)]

def calcCardinal(state1, state2):
    lat1 = stateCapitalLat(state1)
    lon1 = stateCapitalLon(state1)
    lat2 = stateCapitalLat(state2)
    lon2 = stateCapitalLon(state2)

    direction = bearingToCardinal(calcBearing(lat1, lon1, lat2, lon2))

    return direction


def main():
    print("")
    while True:
        # wait for next request from client
        statesInput = socket.recv_json()
        lastInput = statesInput
        print("RECIEVED: %s" % statesInput)

        state1 = statesInput[0]
        state2 = statesInput[1]
        print("   State1:", state1)
        print("   State2:", state2)

        # stateA = "California"    # guess
        # stateB = "Washington"   # answer
        distance = calcDistance(state1, state2)
        direction = calcCardinal(state1, state2)
        # print("From",stateA,"to",stateB,"is", distance,"miles",direction)
        sendReply(distance, direction, True)

        if False:
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
                distance = calcDistance(testCases[0], testCases[1])
                direction = calcDistance(testCases[0], testCases[1])
                print("From",testCases[0],"to",testCases[1],"is", distance,"miles",direction)
        



main()