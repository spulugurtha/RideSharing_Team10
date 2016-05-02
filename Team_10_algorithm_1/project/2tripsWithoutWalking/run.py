import algo
import dataprovider
import datetime

limit=datetime.datetime(1, 1, 1, 0, 0, 1)
original=0
final=0
saved_distance=0
end=False
counter=0
while(end==False):
    print("processing " + str(counter+1) + "th pool")
    counter=counter+1
    end,limit,trip_details_dictionary=dataprovider.get_trip_details(limit)
    limit=limit+datetime.timedelta(0,3)
    pool1=trip_details_dictionary[1]
    pool2=trip_details_dictionary[2]
    pool3=trip_details_dictionary[3]
    pool4=trip_details_dictionary[4]
    initial,total,saved,total_distance_after_merging=algo.main(pool1,pool2,pool3,pool4,2)
    original=original+initial
    final=final+total
    saved_distance=saved_distance+saved

average_original=original/counter
average_final=final/counter
average_saved=saved_distance/counter
total_saved_trips=original-final
print("Total number of trips without ride sharing" + str(original))
print("Total number of trips with ride sharing" + str(final))
print("Average number of trips merged per pool" + str(int((original-final)/counter)))
print("Total number of trips saved: " + str(total_saved_trips))
print("Average number of trips saved: " + str(int(total_saved_trips/counter)))
print("Average number of trips in a pool without ride sharing: " + str(average_original))
print("Average number of trips in a pool with ride sharing: " + str(average_final))
print("Total saved distance: " + str(saved_distance))
print("Average distance saved per pool: " + str(average_saved))




    
