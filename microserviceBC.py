import time
import zmq
import json
import math
import geopandas as gpd
from shapely.ops import nearest_points

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

# load the shapefile of the US states
states_gdf = gpd.read_file('./usStatesShapefile-shp/usStatesShapefile.shp')

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


def inputValidation(state):
    # US state names to check input against, uppercase for case insensitive comparison
    validStatesUpper = [
        'ALABAMA', 'ALASKA', 'ARIZONA', 'ARKANSAS', 'CALIFORNIA', 'COLORADO',
        'CONNECTICUT', 'DELAWARE', 'FLORIDA', 'GEORGIA', 'HAWAII', 'IDAHO',
        'ILLINOIS', 'INDIANA', 'IOWA', 'KANSAS', 'KENTUCKY', 'LOUISIANA',
        'MAINE', 'MARYLAND', 'MASSACHUSETTS', 'MICHIGAN', 'MINNESOTA',
        'MISSISSIPPI', 'MISSOURI', 'MONTANA', 'NEBRASKA', 'NEVADA',
        'NEW HAMPSHIRE', 'NEW JERSEY', 'NEW MEXICO', 'NEW YORK',
        'NORTH CAROLINA', 'NORTH DAKOTA', 'OHIO', 'OKLAHOMA', 'OREGON',
        'PENNSYLVANIA', 'RHODE ISLAND', 'SOUTH CAROLINA', 'SOUTH DAKOTA',
        'TENNESSEE', 'TEXAS', 'UTAH', 'VERMONT', 'VIRGINIA', 'WASHINGTON',
        'WEST VIRGINIA', 'WISCONSIN', 'WYOMING'
    ]
    # normalize input to uppercase for case insensitive comparison
    stateUpper = state.upper()
    valid = stateUpper in validStatesUpper
    if not(valid):
        print("Invalid state name("+state+")")
    return valid # True for valid, False for not


def sendReply(distance, direction, capital = False): # capitals being an optional var until full state lines func done
    # create array in format to send
    result = [distance,direction]
    if capital:
        result.append("Capitals")
    # do some 'work'
    time.sleep(1)

    # send reply back to client
    print("SENDING: ",result,"\n")
    socket.send_json(result)




def findNearestPoints(state1, state2):
    # format that the shp has the statenames in
    state1 = state1.upper()
    state2 = state2.upper()

    # extract the geometry for state1 using 'State_Name' shp column name
    state1Geo = states_gdf[states_gdf['State_Name'].str.upper() == state1].geometry.values[0]
    state2Geo = states_gdf[states_gdf['State_Name'].str.upper() == state2].geometry.values[0]

    point1, point2 = nearest_points(state1Geo, state2Geo)

    # extract latitude and longitude from the points
    lat1 = point1.y
    lon1 = point1.x
    lat2 = point2.y
    lon2 = point2.x

    # print("\t\t\t;;",state1," lat1:",lat1," lon1:",lon1,"(",point1.y,",",point1.x,")")
    # print("\t\t\t;;",state2," lat2:",lat2," lon2:",lon2,"(",point2.y,",",point2.x,")")
    return [lat1, lon1, lat2, lon2]


# for capitals
def stateCapitalLat(state): # helper for capital distance calulation
    try:
        _, lat, _ = state_capitals[state]  # _ ignores that column
        return lat
    except KeyError:  # case that state not found
        return None

# for capitals 
def stateCapitalLon(state): # helper for capital distance calulation
    try:
        _, _, lon = state_capitals[state]  # _ ignores that column
        return lon
    except KeyError:  # case that state not found
        return None



# state distances
    
# for capitals
def calcDistance(state1, state2): # prep states input for haversine formula for capital distance calulation
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
    distance = haversineDistanceFormula(lat1, lon1, lat2, lon2)

    return distance

def haversineDistanceFormula(lat1, lon1, lat2, lon2): # uses Haversine formula 
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
    direction = round(bearing / 45) % 8
    return cardinalPoints[direction]


# for capitals and bordering states
def calcCardinal(state1, state2): # for capital distance calulation
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
        print("RECIEVED: %s" % statesInput)

        state1 = statesInput[0]
        state2 = statesInput[1]
        print("   State1:", state1)
        print("   State2:", state2)

        if inputValidation(state1) and inputValidation(state2):
            [lat1, lon1, lat2, lon2] = findNearestPoints(state1, state2)

            distance  = round(haversineDistanceFormula(lat1, lon1, lat2, lon2))
            if (distance < 1) and (state1 != state2): # if a bordering state and not itself
                direction = calcCardinal(state1, state2)
            else:
                direction = (bearingToCardinal(calcBearing(lat1, lon1, lat2, lon2)))
            print("From",state1,"to",state2,"is", distance,"miles",direction)
            sendReply(distance, direction)
        else: # on invalid statename input
            print("not valid input")
            sendReply(None,None)
            
        # for capitals
        # distance = round(calcDistance(state1, state2))
        # direction = calcCardinal(state1, state2)
        # sendReply(distance, direction, True)
            



main()