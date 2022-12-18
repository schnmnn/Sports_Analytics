import gpxpy
import pandas as pd
import geopy.distance
from numpy_ext import rolling_apply
import matplotlib.pyplot as plt
import datetime
from math import floor

gpx_path = ('gpx_files/activities/7833777707.gpx')
with open(gpx_path) as f:
    gpx = gpxpy.parse(f)

points=[]
for segment in gpx.tracks[0].segments:
    for p in segment.points:
        points.append({
            'time': p.time,
            'latitude': p.latitude,
            'longitude': p.longitude,
            'elevation': p.elevation
        })
df = pd.DataFrame.from_records(points)

#Cumulative Distance
coords = [(p.latitude,p.longitude) for p in df.itertuples()]
df["time"] = df["time"].dt.tz_localize(None)
df['distance'] = [0] + [geopy.distance.distance(from_, to).m for from_, to in zip(coords[:-1], coords[1:])]
df['cumulative_distance'] = df.distance.cumsum()

# Timing
df['duration'] = df.time.diff().dt.total_seconds().fillna(0)
df['cumulative_duration'] = df.duration.cumsum()
df['pace_km/h'] = (df.distance/df.duration )* 3.6

#Dataframe for MovingTime 
"Calculation the movement in meteres per duration"
df["dist_dif_per_sec"] = df["distance"]/df["duration"]
"With including movements of more than 0.4 meters comes closest to the avg Speed of the Strava tour"
df_with_timeout = df[df['dist_dif_per_sec'] > 0.4]

#calculation Tour KPI´s
avg_km_h = (sum((df_with_timeout["pace_km/h"] * 
                 df_with_timeout["duration"])) / 
            sum(df_with_timeout["duration"]))

print(floor(60 / avg_km_h), 'minutes',
    round(((60 / avg_km_h - floor(60 / avg_km_h))*60), 0),
    ' seconds')

specific_distance_duration = df.loc[df['cumulative_distance'] >= 10000].reset_index()
duration_format = datetime.timedelta(seconds = specific_distance_duration.loc[0,'cumulative_duration'])

print(duration_format)