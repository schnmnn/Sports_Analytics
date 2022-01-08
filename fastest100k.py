from xml.dom import minidom
from datetime import datetime, timedelta
import statistics
import matplotlib.pyplot as plt
import math
from geopy import distance
import geopy

mydoc = minidom.parse('data/3483926185.gpx')
geolocation = mydoc.getElementsByTagName('trkpt')
elevation = mydoc.getElementsByTagName('ele')
time = mydoc.getElementsByTagName('time')


# New comment

### Get the Values for the geolocation

#print(geolocation[0].firstChild.data)
    ### list of latitude
latValues = []
lonValues = []
for childNode in geolocation:
    #print((childNode.attributes['lat'].value))
    latValues.append(childNode.attributes['lat'].value)
    lonValues.append(childNode.attributes['lon'].value)
latValues = list(map(float,latValues))
lonValues = list(map(float,lonValues))
#print(latValues)
#print(lonValues)

### Get distance of two geolocations
distance = 0.0
for i in range(len(latValues)):
    if i == (len(latValues)-1):
        break
    point1 = (latValues[i], lonValues[i])
    point2 = (latValues[i+1], lonValues[i+1])
    #print(geopy.distance.distance(point1, point2).m)
    distance = distance + geopy.distance.distance(point1, point2).km
#print(distance)

### Get the Values for the time in list
def to_date(s):
    return datetime.strptime(s, '%Y-%m-%dT%H:%M:%S+00:00')

timeValues = []
for childNode in time:
    timeValues.append(childNode.firstChild.data)
timeValues = list(map(to_date,timeValues))
#print(timeValues)

lenTimeValues = len(timeValues)
timeDeltas = []
for i in range(lenTimeValues):
    if i == lenTimeValues-1:
        break
    timeDeltas.append(timeValues[i+1]-timeValues[i])
#print(timeDeltas)

lenTimeDeltas  = len(timeDeltas)
activityLength = timedelta(0, 0)

for i in range(lenTimeDeltas):
    activityLength = activityLength + timeDeltas[i]
#print(activityLength)

#print("Your activity duration is: " + str(activityLength) +(" h\n") + "with a distance of " + str(round(distance,2)) + " km")

def duration_10km(start_i):
    dist_10k = 0.0
    count = 0
    duration_10k = timedelta(0, 0)
    for i in range(start_i,len(latValues)):
        if i == len(latValues) -1 :
            break
        point1 = (latValues[i], lonValues[i])
        point2 = (latValues[i+1], lonValues[i+1])
        #print(geopy.distance.distance(point1, point2).m)
        dist_10k = dist_10k + geopy.distance.distance(point1, point2).km
        count = i
        duration_10k = duration_10k + timeDeltas[i]
        if dist_10k >= 10.0:
            break

        duration_10k_seconds = duration_10k.total_seconds()
    #print(dist_10k)
    #((dist_10k / duration_10k_seconds) * 3600)
    if dist_10k < 10.0:
        return None
    return duration_10k

print(duration_10km(3000))

all_10k = []
for i in range(len(latValues)):
    all_10k.append(duration_10km(i))

all_10k_values = [i for i in all_10k if i != None]
#print(all_10k_values)
fastest_10km = min(all_10k_values)
print(fastest_10km)


#count=0
#for i in all_10k:
#    if i == None:
#        count = count +1
#print(i)

#neue Liste bauen ohne None

#fastest_10km = min(all_10k)
#print(fastest_10km)