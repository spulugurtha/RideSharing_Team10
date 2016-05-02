from urllib.request import urlopen
from random import randint
import json
import csv
import pymysql

jfk_latitude = "40.6413"
jfk_longitude = "-73.7781"

"""Function to open the database connection
"""
def open_db_connection():
    host_name = 'localhost'
    port_number = 3306
    user_name = 'root'
    password = 'root'
    database_name = 'ridesharing'
    connection_object = pymysql.connect(host=host_name, port=port_number, 
                                        user=user_name, passwd=password, db=database_name)
    return connection_object

"""Function to close the database connection
"""
def close_db_connection(connection_object):
    if connection_object is  not None:
        connection_object.commit()
        connection_object.close()

connection_object = open_db_connection()
if connection_object is not None:
    cursor = connection_object.cursor()
    # Replace the dataset name here
    with open('trip_data_1.csv',"rt", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader, None)
        for row in reader:
            latitude = row[13].strip()
            longitude = row[12].strip()
            trip_distance_original = row[9].strip()
            trip_time_original = row[8].strip()
            url = "http://localhost:5000/route/v1/driving/"+jfk_longitude+","+jfk_latitude+";"
            if((trip_distance_original!=0) and (latitude !="0") and (longitude !="0") and (trip_time_original!="0")):
                url += longitude + "," + latitude
                response = urlopen(url)
                string = response.read().decode('utf-8')
                json_obj = json.loads(string)
                # trip distance in miles
                trip_distance_from_source = json_obj['routes'][0]['distance'] * float(0.000621371)
                # trip duration in seconds
                trip_duration_from_source = json_obj['routes'][0]['duration']
                # average_speed in miles per second
                average_speed = float(trip_distance_original)/int(trip_time_original)
                
                willing_to_walk = randint(0,1)
                
                sql_query_part_one = "insert into original_trip_data(medallion,passenger_count,pickup_datetime,trip_duration_from_source,"
                sql_query_part_two = " trip_distance_original,trip_distance_from_source,dropoff_latitude,dropoff_longitude,original_average_speed,willing_to_walk)"
                sql_query_part_three = " values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                sql_query = sql_query_part_one + sql_query_part_two + sql_query_part_three
                tuple_record = (row[0].strip(), row[7].strip(), row[5].strip(), trip_duration_from_source, row[9].strip(), trip_distance_from_source, 
                                latitude, longitude, average_speed, willing_to_walk)
                cursor.execute(sql_query, tuple_record)
                connection_object.commit()
        cursor.close()
        close_db_connection(connection_object)
        
        
        