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

### Get the Values for the geolocation
latValues = []
lonValues = []
for childNode in geolocation:
    latValues.append(childNode.attributes['lat'].value)
    lonValues.append(childNode.attributes['lon'].value)
latValues = list(map(float,latValues))
lonValues = list(map(float,lonValues))

### Get the Values for the time in list
def to_date(s):
    return datetime.strptime(s, '%Y-%m-%dT%H:%M:%S+00:00')

timeValues = []
for childNode in time:
    timeValues.append(childNode.firstChild.data)
timeValues = list(map(to_date,timeValues))

lenTimeValues = len(timeValues)
timeDeltas = []
for i in range(lenTimeValues):
    if i == lenTimeValues-1:
        break
    timeDeltas.append(timeValues[i+1]-timeValues[i])

def duration_10km(start_i):
    dist_10k = 0.0
    duration_10k = timedelta(0, 0)
    for i in range(start_i,len(latValues)):
        if i == len(latValues) -1 :
            break
        point1 = (latValues[i], lonValues[i])
        point2 = (latValues[i+1], lonValues[i+1])
        dist_10k = dist_10k + geopy.distance.distance(point1, point2).km
        duration_10k = duration_10k + timeDeltas[i]
        if dist_10k >= 10.0:
            break
    if dist_10k < 10.0:
        return None
    return duration_10k


all_10k = []
for i in range(len(latValues)):
    all_10k.append(duration_10km(i))

all_10k_values = [i for i in all_10k if i != None]
fastest_10km = min(all_10k_values)
print(fastest_10km)