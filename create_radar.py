import numpy as np
import pymap3d as pm

class RRRadar():
   def __init__(self, flight, location: str):
      location = str.lower(location)
      if location == "start":
         self.location = "start"
      elif location == "stop":
         self.locaiton = "stop"
      elif location == "midcourse":
         self.location = "midcourse"
      else:
         raise Exception("One of the three location options was not provided. Try again with either 'start', 'stop', or 'midcourse'")

      # calculate the location of the radar
      self.location_lla = [0, 0, 0]
      self.beam_width_rad = 3*np.pi/180 # 3 degrees
      self.scan_width = 3 * self.beam_width_rad
      self.scan_offsets = self.calculate_scan_offsets()
      self.scan_idx = 0 # this will cycle throughout the sim, but never go above len(self.scan_offsets)
      self.scan_center_rad = [0.0, 0.0] # az and el

      # calculate radar parameters, assume detection range of 50km
      # assume RCS of 50dbsm
      # assume coherent integration time of 1 second
      # solve for P*Gt*Gr
      self.min_snr = 10**(10/10)
      self.rcs = 10**(50/10)
      self.P_Gt_Gr = (self.min_snr*4*np.pi*50000**4)/ (self.rcs*1.0)
      self.prf = 3e8/(2*20000) # 20km unambiguous range 
      self.nPulses = 1.0 * self.prf # to keep the coherent integration time at 1 second

   def calculate_scan_offsets(self)->list:
      """Based on the scan_width and beam_width, calculate the az/el offsets for a our scan 
      pattern """
      offsets = []
      for az in np.arange(-self.scan_width, self.scan_width, self.beam_width_rad):
         for el in np.arange(-self.scan_width, self.scan_width, self.beam_width_rad):
            offsets.append((az, el))
      return offsets
   
   def update_scan_center(self, position: set):
      if self.scan_idx != 0:
         return
      # convert from lla to ecef and calculate an az and el
      aer = pm.geodetic2aer(position[0], position[1], position[2], 
                     self.location_lla[0], self.location_lla[1], self.location_lla[2])
      self.scan_center_rad = np.multiply(aer[0:2], np.pi/180)
      return
   
   def send_beam(self, position):

      detect = "No Detect"
      az_scan = self.scan_center_rad[0] + self.scan_offsets[self.scan_idx][0]
      el_scan = self.scan_center_rad[1] + self.scan_offsets[self.scan_idx][1]

      # convert position from lla to ecef and calculate an az and el
      aer = pm.geodetic2aer(position[0], position[1], position[2], 
                     self.location_lla[0], self.location_lla[1], self.location_lla[2])
      az_true = aer[0] * np.pi/180
      el_true = aer[1] * np.pi/180
      # check if we are within beamwidth
      if az_true > az_scan - self.beam_width_rad/2 and az_true < az_scan + self.beam_width_rad/2:
         if el_true > el_scan - self.beam_width_rad/2 and el_true < el_scan + self.beam_width_rad/2:
            # if we are, calculate an SNR
            snr = self.P_Gt_Gr*self.rcs * (1/self.prf) * self.nPulses / ((4*np.pi**2) * aer[2]**4)
            snr_db = 10*np.log10(snr)
            # if the SNR is high enough, detect
            if snr_db > 10:
               detect = "Detect"

      self.scan_idx = (self.scan_idx + 1) % len(self.scan_offsets)

      return detect, az_scan, el_scan, az_true, el_true


def create_radar(flight, location)->RRRadar:
   radar = RRRadar(flight, location)
   return radar