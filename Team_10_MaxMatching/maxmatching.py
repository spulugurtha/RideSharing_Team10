import dataprovider
from urllib.request import urlopen
import json
import networkx as nx
from math import cos, sin, atan2, radians, degrees
import dbconnection
from datetime import timedelta

jfk_latitude = "40.6413"
jfk_longitude = "-73.7781"

list_of_mergeable_trips = []
trips_merged_metadata = dict()
distance_possible_merge = dict()
input_trips_for_algorithm = set()
input_trips_for_max_matching = set()
distance_dictionary = dict()

#===============================================================================
# Function to 
#===============================================================================
def perform_max_matching(passenger_constraint, threshold_value_trip_duration, consider_willing_to_walk, trip_details_dictionary):
    list_of_mergeable_trips[:] = []
    trips_merged_metadata.clear()
    distance_possible_merge.clear()
    input_trips_for_algorithm.clear()
    input_trips_for_max_matching.clear()
    distance_dictionary.clear()
    trip_details_list = []
    no_of_trips = 0
    if trip_details_dictionary is not None:
        if trip_details_dictionary.get(1) is not None:
            no_of_trips += len(trip_details_dictionary.get(1))
            trip_details_list.extend(trip_details_dictionary.get(1))
        if trip_details_dictionary.get(2) is not None:
            no_of_trips += len(trip_details_dictionary.get(2))
            trip_details_list.extend(trip_details_dictionary.get(2))
        if trip_details_dictionary.get(3) is not None:
            no_of_trips += len(trip_details_dictionary.get(3))
            trip_details_list.extend(trip_details_dictionary.get(3))
        if trip_details_dictionary.get(4) is not None:
            no_of_trips += len(trip_details_dictionary.get(4))
            trip_details_list.extend(trip_details_dictionary.get(4))
    # initialize the trip distance matrix to -1 which denotes that the trips are yet to be processed
    # trips are set to be processed only when value at [i][j] position is not -1 
    trip_distance_matrix = [[-1 for x in range(no_of_trips)] for y in range(no_of_trips)]
    i = 0
    print("Processing matrix information")
    total_distance = 0
    while i < len(trip_details_list):
        j = i + 1
        trip_1 = trip_details_list[i]
        total_distance += trip_1.trip_distance_from_source
        input_trips_for_algorithm.add(trip_1.trip_id)
        while j < len(trip_details_list) :
            trip_2 = trip_details_list[j]
            # Trips are processed only when the two are not same and the two trips are not previously processed
            if (trip_1.trip_id != trip_2.trip_id) and (trip_distance_matrix[i][j] == -1):
                passenger_count = trip_1.passenger_count + trip_2.passenger_count
                if ((passenger_count <= passenger_constraint) and (are_trips_mergeable(trip_1, trip_2, threshold_value_trip_duration, consider_willing_to_walk))):
                    trip_distance_matrix[i][j] = 1
                    trip_distance_matrix[j][i] = 1
                else:
                    trip_distance_matrix[i][j] = 0
                    trip_distance_matrix[j][i] = 0
            else:
                trip_distance_matrix[i][j] = 0
                trip_distance_matrix[j][i] = 0
            j = j + 1
        trips_merged_metadata[str(trip_1.trip_id) + "-" + str(trip_1.trip_id)] = [trip_1]
        i = i + 1
    max_matching(total_distance)

#===============================================================================
# Function to perform the max_matching algorithm by calling the networkx api
#===============================================================================
    
def max_matching(total_distance):
    graph = nx.Graph()
    graph.add_weighted_edges_from(list_of_mergeable_trips)
    matching_dictionary = nx.max_weight_matching(graph, maxcardinality=True)
    trip_set = set()
    distance_saved = 0
    for key in matching_dictionary:
        if (key in trip_set) and (matching_dictionary[key] in trip_set):
            continue
        else:
            trip_set.add(key)
            trip_set.add(matching_dictionary[key])
            keyvalue = str(key) + "-" + str(matching_dictionary[key])
            keyvalue1 = str(matching_dictionary[key]) + "-" + str(key)
            if keyvalue in trips_merged_metadata.keys():
                trips = trips_merged_metadata[keyvalue]
                # print(str(trips[0].trip_id) + "," + str(trips[0].passenger_count) + "," + str(trips[0].trip_duration_from_source) + "," + str(trips[0].trip_distance_from_source) + "," + str(trips[0].dropoff_lattitude) + "," + str(trips[0].dropoff_longitude) + "," + str(trips[0].willing_to_walk))
                # print(str(trips[1].trip_id) + "," + str(trips[1].passenger_count) + "," + str(trips[1].trip_duration_from_source) + "," + str(trips[1].trip_distance_from_source) + "," + str(trips[1].dropoff_lattitude) + "," + str(trips[1].dropoff_longitude) + "," + str(trips[1].willing_to_walk))
                print(str(trips[0].trip_id) + "," + str(trips[0].passenger_count) + "," + str(trips[0].dropoff_lattitude) + "," + str(trips[0].dropoff_longitude))
                print(str(trips[1].trip_id) + "," + str(trips[1].passenger_count) + "," + str(trips[1].dropoff_lattitude) + "," + str(trips[1].dropoff_longitude))
                print("---------------------------------------------------------------------------------------------")
                distance_saved += distance_dictionary[keyvalue]
            elif keyvalue1 in trips_merged_metadata.keys():
                trips = trips_merged_metadata[keyvalue1]
                # print(str(trips[0].trip_id) + "," + str(trips[0].passenger_count) + "," + str(trips[0].trip_duration_from_source) + "," + str(trips[0].trip_distance_from_source) + "," + str(trips[0].dropoff_lattitude) + "," + str(trips[0].dropoff_longitude) + "," + str(trips[0].willing_to_walk))
                # print(str(trips[1].trip_id) + "," + str(trips[1].passenger_count) + "," + str(trips[1].trip_duration_from_source) + "," + str(trips[1].trip_distance_from_source) + "," + str(trips[1].dropoff_lattitude) + "," + str(trips[1].dropoff_longitude) + "," + str(trips[1].willing_to_walk))
                print(str(trips[0].trip_id) + "," + str(trips[0].passenger_count) + "," + str(trips[0].dropoff_lattitude) + "," + str(trips[0].dropoff_longitude))
                print(str(trips[1].trip_id) + "," + str(trips[1].passenger_count) + "," + str(trips[1].dropoff_lattitude) + "," + str(trips[1].dropoff_longitude))
                print("---------------------------------------------------------------------------------------------")
                distance_saved += distance_dictionary[keyvalue1]
            else :
                print("no there")
                print("---------------------------------------------------------------------------------------------")
    print("-----------------------------------------------------------------------------------")
    print("input_trips_for_algorithm ", str(len(input_trips_for_algorithm)))
    print("input_trips_for_max_matching ", str(len(input_trips_for_max_matching)))
    print("lone_trip ", input_trips_for_max_matching.difference(matching_dictionary.keys()))
    no_trips_saved = len(input_trips_for_algorithm) - len(matching_dictionary.keys()) / 2 - len(input_trips_for_max_matching.difference(matching_dictionary.keys()))
    print("no of trips saved " + str(no_trips_saved))
    print("total_distance " + str(total_distance))
    print("distance saved " + str(total_distance - distance_saved))
    print("Total_trips_without_ridesharing " + str(len(input_trips_for_algorithm)))
    unmergeable_trips = len(input_trips_for_algorithm) - len(input_trips_for_max_matching)
    print("unmergeable trips " + str(unmergeable_trips))
    total_trips_due_to_ridesharing = len(matching_dictionary.keys()) / 2 + len(input_trips_for_max_matching.difference(matching_dictionary.keys())) + unmergeable_trips
    print("Total_trips_due_to_ridesharing " + str(total_trips_due_to_ridesharing))
    print("Merged_trips_only_after_ridesharing(without unmergeable trips and lone trips) " + str(len(matching_dictionary.keys()) / 2))
    print("-----------------------------------------------------------------------------------")

                
def are_trips_mergeable(trip_1, trip_2, threshold_value_trip_duration, consider_willing_to_walk): 
    if consider_willing_to_walk:
        return are_trips_mergeable_with_walking(trip_1, trip_2, threshold_value_trip_duration)
    else:
        return are_trips_mergeable_without_walking(trip_1, trip_2, threshold_value_trip_duration)
   
  
def are_trips_mergeable_without_walking(trip_1, trip_2, threshold_value_trip_duration):   
    url = "http://localhost:5000/route/v1/driving/" + trip_1.dropoff_longitude + "," + trip_1.dropoff_lattitude + ";" + trip_2.dropoff_longitude + "," + trip_2.dropoff_lattitude
    response = urlopen(url)
    string = response.read().decode('utf-8')
    json_obj = json.loads(string)
    if json_obj is not None:
        duration_between_two_trips = json_obj['routes'][0]['duration']
        distance_between_two_trips = json_obj['routes'][0]['distance'] * float(0.000621371)
        edge_one = 0
        edge_two = 0
        distance_one = 0
        if trip_1.trip_duration_from_source <= trip_2.trip_duration_from_source:
            edge_one = trip_1.trip_duration_from_source
            edge_two = trip_2.trip_duration_from_source
            distance_one = trip_1.trip_distance_from_source
        else:
            edge_one = trip_2.trip_duration_from_source
            edge_two = trip_1.trip_duration_from_source
            distance_one = trip_2.trip_distance_from_source
        valid_edges = validate_edges(edge_one, edge_two, duration_between_two_trips, threshold_value_trip_duration)
        if valid_edges:
            input_trips_for_max_matching.add(trip_1.trip_id)
            input_trips_for_max_matching.add(trip_2.trip_id)
            edge_details_for_max_matching = (trip_1.trip_id, trip_2.trip_id, duration_between_two_trips)
            list_of_mergeable_trips.append(edge_details_for_max_matching)
            key = str(trip_1.trip_id) + "-" + str(trip_2.trip_id)
            distance_with_ridesharing = calculate_distance(distance_one, distance_between_two_trips)
            trips_merged_metadata[key] = [trip_1, trip_2]
            distance_dictionary[key] = distance_with_ridesharing  
            # print(key+"-"+str(valid_edges))
            # print("---------------------------------------------------")
            distance_possible_merge[str(trip_1.trip_id) + "-" + str(trip_2.trip_id)] = edge_one + distance_between_two_trips
    return valid_edges

def are_trips_mergeable_with_walking(trip_1, trip_2, threshold_value_trip_duration):
    if trip_1.willing_to_walk == 0 and trip_2.willing_to_walk == 0:
        return are_trips_mergeable_without_walking(trip_1, trip_2, threshold_value_trip_duration)
    else:
        bearing = 0
        basic_url = "http://localhost:5001/nearest/v1/foot/"
        sub_url = "?number=1000&bearings="
        radius_url = ",180&radiuses=1342"
        temp_trip1 = dataprovider.RideDetails(trip_1.trip_id, trip_1.medallion, trip_1.passenger_count, trip_1.pickup_datetime, trip_1.trip_duration_from_source, trip_1.trip_distance_from_source,
                  trip_1.dropoff_lattitude, trip_1.dropoff_longitude, trip_1.willing_to_walk)
        temp_trip2 = dataprovider.RideDetails(trip_2.trip_id, trip_2.medallion, trip_2.passenger_count, trip_2.pickup_datetime, trip_2.trip_duration_from_source, trip_2.trip_distance_from_source,
                  trip_2.dropoff_lattitude, trip_2.dropoff_longitude, trip_2.willing_to_walk)
            
        if trip_1.trip_duration_from_source <= trip_2.trip_duration_from_source:
            if trip_1.willing_to_walk == 1:
                bearing = calculate_bearing(float(trip_1.dropoff_lattitude), float(trip_1.dropoff_longitude), float(jfk_latitude), float(jfk_longitude))
                bearing = str(int(bearing))
                # print("1", trip_1.dropoff_lattitude, trip_1.dropoff_longitude, jfk_latitude, jfk_longitude, bearing)
                url = basic_url + trip_1.dropoff_longitude + "," + trip_1.dropoff_lattitude + sub_url + bearing
                url = url + radius_url
                temp_trip1 = get_nearest_drop_off_point(temp_trip1, url)
            if trip_2.willing_to_walk == 1:
                bearing = calculate_bearing(float(temp_trip1.dropoff_lattitude), float(temp_trip1.dropoff_longitude), float(trip_2.dropoff_lattitude), float(trip_2.dropoff_longitude))
                bearing = str(int(bearing))
                # print("2", temp_trip1.dropoff_lattitude, temp_trip1.dropoff_longitude, trip_2.dropoff_lattitude, trip_2.dropoff_longitude, bearing)
                url = basic_url + trip_2.dropoff_longitude + "," + trip_2.dropoff_lattitude + sub_url + bearing
                url = url + radius_url
                temp_trip2 = get_nearest_drop_off_point(temp_trip2, url)
        else:
            if trip_2.willing_to_walk == 1:
                bearing = calculate_bearing(float(trip_2.dropoff_lattitude), float(trip_2.dropoff_longitude), float(jfk_latitude), float(jfk_longitude))
                bearing = str(int(bearing))
                # print("3", trip_2.dropoff_lattitude, trip_2.dropoff_longitude, jfk_latitude, jfk_longitude, bearing)
                url = basic_url + trip_2.dropoff_longitude + "," + trip_2.dropoff_lattitude + sub_url + bearing
                url = url + radius_url
                temp_trip2 = get_nearest_drop_off_point(temp_trip2, url)
            if trip_1.willing_to_walk == 1:
                bearing = calculate_bearing(float(temp_trip2.dropoff_lattitude), float(temp_trip2.dropoff_longitude), float(trip_1.dropoff_lattitude), float(trip_1.dropoff_longitude))
                bearing = str(int(bearing))
                # print("4", temp_trip2.dropoff_lattitude, temp_trip2.dropoff_longitude, trip_1.dropoff_lattitude, trip_1.dropoff_longitude, bearing)
                url = basic_url + trip_1.dropoff_longitude + "," + trip_1.dropoff_lattitude + sub_url + bearing
                url = url + radius_url
                temp_trip1 = get_nearest_drop_off_point(temp_trip1, url)
        url = "http://localhost:5000/route/v1/driving/" + temp_trip1.dropoff_longitude + "," + temp_trip1.dropoff_lattitude + ";" + temp_trip2.dropoff_longitude + "," + temp_trip2.dropoff_lattitude
        response = urlopen(url)
        string = response.read().decode('utf-8')
        json_obj = json.loads(string)
        if json_obj is not None:
            duration_between_two_trips = json_obj['routes'][0]['duration']
            distance_between_two_trips = json_obj['routes'][0]['distance'] * float(0.000621371)
            edge_one = 0
            edge_two = 0
            distance_one = 0
            if temp_trip1.trip_duration_from_source <= temp_trip2.trip_duration_from_source:
                edge_one = temp_trip1.trip_duration_from_source
                edge_two = temp_trip2.trip_duration_from_source
                distance_one = temp_trip1.trip_distance_from_source
            else:
                edge_one = temp_trip2.trip_duration_from_source
                edge_two = temp_trip1.trip_duration_from_source
                distance_one = temp_trip2.trip_distance_from_source
            valid_edges = validate_edges(edge_one, edge_two, duration_between_two_trips, threshold_value_trip_duration)
            if valid_edges:
                input_trips_for_max_matching.add(temp_trip1.trip_id)
                input_trips_for_max_matching.add(temp_trip2.trip_id)
                edge_details_for_max_matching = (temp_trip1.trip_id, temp_trip2.trip_id, duration_between_two_trips)
                list_of_mergeable_trips.append(edge_details_for_max_matching)
                key = str(temp_trip1.trip_id) + "-" + str(temp_trip2.trip_id)
                trips_merged_metadata[key] = [temp_trip1, temp_trip2]
                distance_possible_merge[str(trip_1.trip_id) + "-" + str(trip_2.trip_id)] = edge_one + distance_between_two_trips
                distance_with_ridesharing = calculate_distance(distance_one, distance_between_two_trips)
                trips_merged_metadata[key] = [trip_1, trip_2]
                distance_dictionary[key] = distance_with_ridesharing   
    return valid_edges
    
    
def calculate_bearing(to_lattitude, to_longitude, from_lattitude, from_longitude):
    diff_longitude = radians(from_longitude - to_longitude)
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

def get_nearest_drop_off_point(trip_data, url):
    response = urlopen(url)
    string = response.read().decode('utf-8')
    json_obj = json.loads(string)
    if json_obj is not None:
        last_point = len(json_obj)
        drop_off_lattitude = str(json_obj['waypoints'][last_point - 1]['location'][1])
        drop_off_longitude = str(json_obj['waypoints'][last_point - 1]['location'][0])
        trip_data.dropoff_lattitude = drop_off_lattitude
        trip_data.dropoff_longitude = drop_off_longitude
        url = "http://localhost:5000/route/v1/driving/" + drop_off_longitude + "," + drop_off_lattitude + ";" + jfk_longitude + "," + jfk_latitude
        response = urlopen(url)
        string = response.read().decode('utf-8')
        json_obj = json.loads(string)
        if json_obj is not None:
            duration_between_two_trips = json_obj['routes'][0]['duration']
            distance_between_two_trips = json_obj['routes'][0]['distance'] * float(0.000621371)
            trip_data.trip_duration_from_source = duration_between_two_trips
            trip_data.trip_distance_from_source = distance_between_two_trips
    return trip_data
    

def validate_edges(edge_one, edge_two, inter_trip_edge, threshold_value_trip_duration):
    increased_duration = (((edge_one + inter_trip_edge) - edge_two) / edge_two) 
    valid_edges_for_merging = False
    if increased_duration <= threshold_value_trip_duration:
        valid_edges_for_merging = True
    return valid_edges_for_merging

def calculate_distance(distance_one, distance_two):
    return distance_one + distance_two


def main():
    connection_object = dbconnection.open_db_connection()
    cursor = connection_object.cursor()
    cursor.execute("select * from original_trip_data order by pickup_datetime")
    first_record = cursor.fetchone()
    startdate = first_record[3]
    #Replace time window
    enddate = first_record[3] + timedelta(minutes=1)
    while(True):
        query = "select * from original_trip_data where pickup_datetime between ('%s') and ('%s')" % (startdate, enddate)
        cursor.execute(query)
        if cursor == None:
            break
        else:
            trip_details_dictionary = {}
            for record in cursor:
                rideDetails = dataprovider.RideDetails(record[0], record[1], record[2], record[3], record[4], record[6], record[7], record[8], record[10])
                if record[2] in trip_details_dictionary.keys():
                    rides_list = trip_details_dictionary[record[2]]
                    rides_list.append(rideDetails)
                    trip_details_dictionary[record[2]] = rides_list
                else:
                    rides_list = [rideDetails]
                    trip_details_dictionary[record[2]] = rides_list
            #Replace input parameter to the algorithm here
            perform_max_matching(4, 0.2, True, trip_details_dictionary)
            #Replace time window
            startdate = enddate + timedelta(seconds=1)
            #Replace time window
            enddate = startdate + timedelta(minutes=1)
    
if __name__ == "__main__":
    main()
    


        
        
        
        
