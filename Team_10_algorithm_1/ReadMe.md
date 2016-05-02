This Package is for implementing our own algorithm to share rides starting from JFK airport with various destinations spread over new york. 

1) There are three modules
	a) 2tripsWithoutWalking 
		This module merges two trips at once by the assumption that no passenger is willing to walk. 
	b) 2tripsWithWalking
		This module merges two trips at once by the assumption that random passengers walk. This random decision is self generated by 			by us and stored in the database. 
	c) 3tripsWithoutWalking
		This module merges three trips at once by the assumption that no passenger is willing to walk. 
		
2) Every module is constructed in the same manner. 
	1) dbconnection.py
		This script opens and closes a connection with the MySQL database before and after the execution of the algorithm. 
	2) dataprovider.py
		This script queries the database using the open connection generated in the dbconnection.py. It queries the data in a loop 			based on the time window. Basically all the records that come under the next 'x' minutes (x is the size of the window) are 			queried. 
	3) algo.py 
		This script implements the algorithm by getting the data from run.py in the form of a python dictionary. 
	4) run.py 
		This is the main script that connects the algorithm and the database. User trying to run this project should execute this 			script after loading the mysql database. 
3) distanceosrm.py
	1) This script loads the database from the final.csv file kept in this same directory. 
	2) A user trying to run this project should execute the distanceosrm.py file first after keeping the necessary csv file in the same 
	   directory. This should be followed after creating the database in the mysql server of your system. 
4) Dependencies
	1) OSRM
		This package is kept in the parent directory, which should be run using the following Linux command in the kernel 
			osrm-routed <filename.osm> 
	2) Foot server: 
		
