import opensky_api
import time
import numpy as np


hour_to_sec = 60*60

class Flight():
   def __init__(self, lat_deg=(0.0, 1.0), lon_deg=(0.0, 1.0), alt_m=(10000, 10000), time_s=hour_to_sec):
      # will create a linear flight path between start and end points
      self.lat_deg = lat_deg
      self.lon_deg = lon_deg
      self.alt_m = alt_m
      self.time_s = (0, time_s)
      self.position = [self.lat_deg[0], self.lon_deg[0], self.alt_m[0]] # initial position

   def update_position(self, time_s):
      self.position[0] = np.interp(time_s, self.time_s, self.lat_deg)
      self.position[1] = np.interp(time_s, self.time_s, self.lon_deg)
      self.position[2] = np.interp(time_s, self.time_s, self.alt_m)
      

def create_flight(flight: str) -> Flight:
   #opensky = opensky_api.OpenSkyApi()
   #flights = opensky.get_flights_from_interval(time.time() - hour_to_sec, time.time())
   
   return Flight()