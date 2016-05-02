import dbconnection
from datetime import timedelta
import pickle
"""Class definition to details of trips
"""
class RideDetails:
    def __init__(self, trip_id, medallion, passenger_count, pickup_datetime, trip_duration_from_source, trip_distance_from_source,
                  dropoff_lattitude, dropoff_longitude, willing_to_walk):
        self.trip_id = trip_id
        self.medallion = medallion
        self.passenger_count = passenger_count
        self.pickup_datetime = pickup_datetime
        self.trip_duration_from_source = trip_duration_from_source
        self.trip_distance_from_source = trip_distance_from_source
        self.dropoff_lattitude = dropoff_lattitude
        self.dropoff_longitude = dropoff_longitude
        self.willing_to_walk = willing_to_walk
        
def get_trip_details():
    trip_details_dictionary = {}
    connection_object = dbconnection.open_db_connection()
    cursor = connection_object.cursor()
    cursor.execute("select * from original_trip_data order by pickup_datetime")
    first_record = cursor.fetchone()
    limit = first_record[3]+ timedelta(minutes=1)
    query = "select * from original_trip_data where passenger_count between 1 and 4 order by pickup_datetime"
    cursor.execute(query)
    for record in cursor:
        if(record[3] <= limit):
            rideDetails = RideDetails(record[0], record[1], record[2], record[3], record[4], record[6], record[7], record[8], record[10])
            print((record[0], record[1], record[2], record[3], record[4], record[6], record[7], record[8], record[10]))
            if record[2] in trip_details_dictionary.keys():
                rides_list = trip_details_dictionary[record[2]]
                rides_list.append(rideDetails)
                trip_details_dictionary[record[2]] = rides_list
            else:
                rides_list = [rideDetails]
                trip_details_dictionary[record[2]] = rides_list
        else:
            break
    dbconnection.close_db_connection(connection_object)
    #for i in range(4):
    #   temp=str(i+1)
    #   f=open(temp,"wb")
    #   pickle.dump(trip_details_dictionary[1],f)
    #   f.close()
    
    return trip_details_dictionary

    

        