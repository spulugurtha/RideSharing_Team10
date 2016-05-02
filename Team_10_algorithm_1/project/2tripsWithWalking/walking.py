from math import cos, sin, atan2, radians, degrees
from urllib.request import urlopen
import json
def calculate_bearing(to_lattitude, to_longitude, from_lattitude, from_longitude):
    to_lattitude, to_longitude, from_lattitude, from_longitude = float(to_lattitude), float(to_longitude), float(from_lattitude), float(from_longitude)
    diff_longitude =  radians(from_longitude - to_longitude)
    to_lattitude = radians(to_lattitude)
    to_longitude = radians(to_longitude)
    from_lattitude = radians(from_lattitude)
    from_longitude = radians(from_longitude)
    y = cos(from_lattitude) * sin(diff_longitude)
    x = (cos(to_lattitude) * sin(from_lattitude)) - (sin(to_lattitude) * cos(from_lattitude) * cos(diff_longitude))
    bearing = atan2(y, x)
    bearing = degrees(bearing)
    if bearing < 0:
        bearing = bearing + 180
    return bearing
    
def lat_long(angle,lat,long):
    basic_url = "http://10.9.209.247:5001/nearest/v1/foot/"
    sub_url = "?number=1000&bearings="
    radius_url = ",180&radiuses=1342"
    url = basic_url + str(long)+","+str(lat) + sub_url + str(int(angle))
    url = url + radius_url
    print(url)
    response = urlopen(url)
    string = response.read().decode('utf-8')
    json_obj = json.loads(string)
    if json_obj is not None:
        last_point = len(json_obj)
        drop_off_lattitude = str(json_obj['waypoints'][last_point-1]['location'][1])
        drop_off_longitude = str(json_obj['waypoints'][last_point-1]['location'][0])
    return drop_off_lattitude,drop_off_longitude

        
    