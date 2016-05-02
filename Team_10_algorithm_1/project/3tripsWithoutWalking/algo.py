import requests
import pickle
import sys
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
class graph(object):
    def __init__(self, trips, n):
        self.trips=trips
        self.n=n
    def calculate_distance(self):
        graph=[[0 for x in range(self.n+1)] for x in range(self.n+1)]
        for i in range(self.n+1):
            for j in range(self.n+1):
                if(i==j):
                    graph[i][j]=0
                    url=None
#                elif(i!=0 and j!=0):
#                    url='http://localhost:5000/route/v1/driving/'+self.trips[i-1].dropoff_longitude+','+self.trips[i-1].dropoff_lattitude+';'+self.trips[j-1].dropoff_longitude+','+self.trips[j-1].dropoff_lattitude+'?overview=false'
                elif(i==0):
                    url='http://localhost:5000/route/v1/driving/'+'-73.7781,40.6413'+';'+self.trips[j-1].dropoff_longitude+','+self.trips[j-1].dropoff_lattitude+'?overview=false'
                elif(j==0):
                    url='http://localhost:5000/route/v1/driving/'+self.trips[i-1].dropoff_longitude+','+self.trips[i-1].dropoff_lattitude+';'+'-73.7781,40.6413'+'?overview=false'
                else:
                    url='http://localhost:5000/route/v1/driving/'+self.trips[i-1].dropoff_longitude+','+self.trips[i-1].dropoff_lattitude+';'+self.trips[j-1].dropoff_longitude+','+self.trips[j-1].dropoff_lattitude+'?overview=false'                 
                if(url!=None):
                    r=requests.get(url)
                    try:
                        json_data=r.json()
                    except:
                        pass
                    data=dict(json_data['routes'][0])
                    graph[i][j]=data['distance']
        return graph
        
    def calculate(self):
        graph=[[0 for x in range(self.n+1)] for x in range(self.n+1)]
        lat=[]
        long=[]
        for i in self.trips:
            lat.append(i.dropoff_lattitude)
            long.append(i.dropoff_longitude)
        url="http://localhost:5000/table/v1/driving/-73.7781,40.6413;"
        for i in range(len(self.trips)):
            url=url+long[i]+','+lat[i]+';'
        url=url[:len(url)-1]
        url=url+'?sources='
        for i in range(len(self.trips)+1):
            url=url+str(i)+';'
        url=url[:len(url)-1]
        url=url+'&destinations='
        for i in range(len(self.trips)+1):
            url=url+str(i)+';'
        url=url[:len(url)-1]
        r=requests.get(url)
        json_data=r.json()
        graph=json_data['durations']
        return graph
#  http://localhost:5000/table/v1/driving/-73.7781,40.6413;-73.9712,40.7831?sources=0;1&destinations=0;1

def merge2(trips):
    n=len(trips)
    g=graph(trips,n)
    matrix=g.calculate()
    distance_matrix=g.calculate_distance()
    i = min(j for j in matrix[0] if j > 0) 
    i= matrix[0].index(i)
    q = min(j for j in matrix[i] if j > 0)
    q= matrix[i].index(q)
    delay = (matrix[0][i]+matrix[i][q])-matrix[0][q]
    try:
        delay = delay/matrix[0][q]
    except:
        return True,0,0
        
    delay = delay*100
    distance_of_merged_trips=distance_matrix[0][i]+distance_matrix[i][q]
    distance_if_not_merged=distance_matrix[0][i]+distance_matrix[0][q]
    saved=distance_if_not_merged-distance_of_merged_trips
    if(delay>20):
        return False,0,0
    else:
        return True,saved,distance_of_merged_trips
        
def merge3(merged,new):
    trips=merged
    trips.append(new)
    n=len(trips)
    g=graph(trips,n)
    matrix=g.calculate()
    distance_matrix=g.calculate_distance()
    i = min(j for j in matrix[0] if j > 0) 
    i= matrix[0].index(i)
    q = min(j for j in matrix[i] if j > 0)
    q= matrix[i].index(q)
    t = min(j for j in matrix[q] if j > 0)
    t = matrix[q].index(t)
    
    delay = (matrix[0][i]+matrix[i][q]+matrix[q][t])-matrix[0][t]
    try:
        delay = delay/matrix[0][t]
    except:
        return True,0
        
    delay = delay*100
    distance_of_merged_trips=distance_matrix[q][t]
    distance_if_not_merged=distance_matrix[0][t]
    saved=distance_if_not_merged-distance_of_merged_trips
    if(delay>20):
        return False,0,0
    else:
        return True,saved,distance_of_merged_trips
 
def main(pool1,pool2,pool3,pool4,k):
    dic_one={}
    dic_two={}
    dic_three={}
    dic_four={}
    for i in pool1:
        dic_one[i.trip_id]=i
    for i in pool2:
        dic_two[i.trip_id]=i
    for i in pool3:
        dic_three[i.trip_id]=i
    for i in pool1:
        dic_four[i.trip_id]=i
    saved_final=0
    total_distance_of_merged_trips=0
#    f=open("one","rb")
#    pool1=pickle.load(f)
#    f.close()
#    g=open("two","rb")
#    pool2=pickle.load(g)
#    g.close()
#    h=open("three","rb")
#    pool3=pickle.load(h)
#    h.close()
#    i=open("four","rb")
#    pool4=pickle.load(i)
#    i.close()
    initial=len(pool1)+len(pool2)+len(pool3)+len(pool4)
    #print(pool4)
    total=0
    three_to_one={}
    # Merging pool3 with pool1------------------------------------------------------------
    for i in range(len(pool1)):
        for j in range(len(pool3)):
            if((pool3[j].trip_id not in three_to_one.keys()) and (pool1[i].trip_id not in three_to_one.values())):
                boolean,saved,distance_of_merged_trips=merge2([pool1[i],pool3[j]])                
                if(boolean==True):
                    three_to_one[pool3[j].trip_id]=pool1[i].trip_id
                    saved_final=saved_final+saved
                    total_distance_of_merged_trips+=distance_of_merged_trips             
    total=total+len(three_to_one)
    temp=[]
    for i in pool3:  #delete the unmergable pool3 and merge it with pool4
        if(i.trip_id in three_to_one.keys()):
            pass
        else:
            temp.append(i)
    pool3=temp
    del temp
    pool4.extend(pool3)
    if(pool4==None):
        sys.exit("Pool4 is None pool3")
    del pool3
    temp=[]
    for i in pool1:
        if(i.trip_id in three_to_one.values()):
            pass
        else:
            temp.append(i)
    pool1=temp
    del temp
    
    #Merge pool2 with pool2
    two_to_two={}
    for i in range(len(pool2)):
        for j in range(len(pool2)):
            if(i!=j and pool2[i].trip_id not in two_to_two.keys() and pool2[i].trip_id not in two_to_two.values() and pool2[j].trip_id not in two_to_two.keys() and pool2[j].trip_id not in two_to_two.values()):
                boolean,saved,distance_of_merged_trips=merge2([pool2[i],pool2[j]])                
                if(boolean==True):
                    two_to_two[pool2[i].trip_id]=pool2[j].trip_id
                    saved_final=saved+saved_final
                    total_distance_of_merged_trips+=distance_of_merged_trips
    total=total+len(two_to_two)
    temp=[]
    for i in pool2:
        if(i.trip_id in two_to_two.keys() or i.trip_id in two_to_two.values()):
            pass
        else:
            temp.append(i)
    pool2=temp  #keep the unmergable pool2 trips to further merge with pool1 trips
    del temp
    
    #merge two with one
    two_to_one={}
    for i in range(len(pool1)):
        for j in range(len(pool2)):
            if((pool2[j].trip_id not in two_to_one.keys()) and (pool1[i].trip_id not in two_to_one.values())):
                boolean,saved,distance_of_merged_trips=merge2([pool1[i],pool2[j]])              
                if(boolean==True):
                    two_to_one[pool2[j].trip_id]=pool1[i].trip_id
                    saved_final=saved_final+saved
                    total_distance_of_merged_trips+=distance_of_merged_trips
    total=total+len(two_to_one)
    temp=[]
    for i in pool2:  #delete the unmergable pool2 and merge it with pool4
        if(i.trip_id in two_to_one.keys()):
            pass
        else:
            temp.append(i)
    pool2=temp
    del temp
    if(pool4==None):
        sys.exit("pool4 is none pool2")
    pool4.extend(pool2)
    del pool2
    temp=[]
    for i in pool1:
        if(i.trip_id in three_to_one.values()):
            pass
        else:
            temp.append(i)
    pool1=temp
    del temp
    total=total+len(two_to_one)
    
    
    #Merge one with one
    one_to_one={}
    for i in range(len(pool1)):
        for j in range(len(pool1)):
            if(i!=j and pool1[i].trip_id not in one_to_one.keys() and pool1[i].trip_id not in one_to_one.values() and pool1[j].trip_id not in one_to_one.keys() and pool1[j].trip_id not in one_to_one.values()):
                boolean,saved,distance_of_merged_trips=merge2([pool1[i],pool1[j]])               
                if(boolean==True):
                    one_to_one[pool1[i].trip_id]=pool1[j].trip_id
                    saved_final=saved_final+saved
                    total_distance_of_merged_trips+=distance_of_merged_trips
    total=total+len(one_to_one)
                    
    temp=[]
    for i in pool1:
        if(i.trip_id in one_to_one.keys() or i.trip_id in one_to_one.values()):
            pass
        else:
            temp.append(i)
    pool1=temp  #keep the unmergable pool1 trips
    del temp
    
    #merging for 3 trips with the previously calculated data
    for i in two_to_one.keys():
        two_to_one[i]=[two_to_one[i]]
    for i in one_to_one.keys():
        one_to_one[i]=[one_to_one[i]]
    temp=[]            
    for i in pool1:
        for j in two_to_one.keys():
            boolean,saved,distance_of_merged_trips=merge3([dic_two[j],dic_one[two_to_one[j][0]]],i)
            if(boolean==True):
                two_to_one[j].append(i.trip_id)
                saved_final=saved_final+saved
                total_distance_of_merged_trips+=distance_of_merged_trips
            else:
                temp.append(i)
    pool1=temp
    temp=[]
    for i in pool1:
        for j in one_to_one.keys():   
            boolean,saved,distance_of_merged_trips=merge3([dic_one[j],dic_one[one_to_one[j][0]]],i)
            if(boolean==True):
                one_to_one[j].append(i.trip_id)
                saved_final=saved_final+saved
                total_distance_of_merged_trips+=distance_of_merged_trips
            else:
                temp.append(i)
    pool1=temp
    
    pool4.extend(pool1)
    total=total+len(pool4)
    total_distance_after_merging=total_distance_of_merged_trips
    for i in pool4:
        total_distance_after_merging+=i.trip_distance_from_source
    return initial,total,saved_final,total_distance_after_merging

    
    
    
    
    
    
    
    

    
