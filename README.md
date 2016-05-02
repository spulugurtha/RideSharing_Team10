README - SOURCE CODE RE-RUN

Please follow the below steps in order to run the code :

14.1 DATABASE PROCESSING

1. Make sure that the mysql database is present in the system.
2. The database ridesharing can be created by running the command create database ridesharing.
3. Navigate to the database by running command use ridesharing.
The create script for the table original_trip_data is as follows,
create table original_trip_data(ID serial, medallion int(11), passenger_count int(5), pickup_datetime datetime,trip_duration_from_source double,
trip_distance_original double(10,8), trip_distance_from_source double(10,8), dropoff_latitude varchar(15), dropoff_longitude varchar(15),
original_average_speed double, willing_to_walk int(1), primary key(ID));

14.2 RIDEHSARING PREPROCESSING

1. Make sure that the osrm routing web services server for driving is running and the dataset to be used in the same folder as the distanceosrm.py python script.
2. You can start by typing the command osrm-routed new-york_new-york.osrm by navigating to the path where we have the routing service is present.
3. Modify the dataset name in the script mentioned at line number 33 (# Replace the dataset name here). The dataset and the script file 4. should be placed in the same location.
4. Navigate to the terminal path where you have the python script and execute the following command python3 distanceosrm.py. This will load the dataset into the database.

14.3 MAX MATCHING ALGORITHM

1. Make sure that the following script files dbconnection.py and maxmatching.py are copied to the local file system.
2. Make sure that the osrm routing web services server for driving and osrm routing web services server for walking are running.
3. You can start by typing the command osrm-routed new-york_new-york.osrm by navigating to the path where we have the routing service is present.
4. You can start by typing the command osrm-routed -p 5001 new-york_new-york.osrm by navigating to the path where we have the walking service is present.
5. In the maxmatching.py script file, you can modify the input parameters to the algorithm. In line number 317, (#Replace input parameter to the algorithm here) the input parameters to the algorithm can be modified. The call to the function perform_max_matching takes four parameters where the first parameter is the passenger count which is fixed(4). The second parameter is the threshold parameter which can be varied between 0.1 and 0.4(i.e, 10% and 40%). The third parameter is for considering the willingness to walk parameter(True or False).
6. The pool window has to modified at line numbers 298, 319 and 321 (#Replace time window).
7. Navigate to the terminal path where you have the python script and execute the following command python3 maxmatching.py.

14.4 ALGORITHM 1

1. This Package is for implementing our own algorithm to share rides starting from JFK airport with various destinations spread over new york. 
2. The dependencies for the Algorithm - 1 which are common are the foot server, OSRM server has to be started in prior to the execution of this package.
3. The database dependencies should be loaded using python scripts distanceosrm.py, dbconnection.py.
4. The main script run.py is executed from command line as python3 run.py after loading the mysql database

