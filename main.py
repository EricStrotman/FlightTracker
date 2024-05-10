import argparse
import create_flight
import create_radar
import pandas as pd
import plotting
import numpy as np

def create_arg_parse() -> argparse.ArgumentParser:
   description_file = "./README.md"
   fid = open(description_file, "r")
   description_text = ''
   for line in fid:
      description_text = description_text + line + '\n'
   parser = argparse.ArgumentParser('Flight Tracker', description=description_text)
   parser.add_argument("-r", "--RadarLocation", action="store", default="start")
   parser.add_argument("-f", "--Flight", action="store")
   return parser

def run(flight, radar):

   # initialize plotting vars
   plotting_vars = {"scan_az": [], "scan_el": [], "detect": [],
                    "true_az": [], "true_el": [], "time": []}

   current_time_sec = flight.time_s[0]
   tic_sec = 1/radar.prf * radar.nPulses
   while current_time_sec < flight.time_s[1]:
      flight.update_position(current_time_sec)
      radar.update_scan_center(flight.position)
      detect, s_az, s_el, t_az, t_el = radar.send_beam(flight.position)
      # log vars
      plotting_vars["scan_az"].append(s_az)
      plotting_vars["scan_el"].append(s_el)
      plotting_vars["detect"].append(detect)
      plotting_vars["true_az"].append(t_az)
      plotting_vars["true_el"].append(t_el)
      plotting_vars["time"].append(current_time_sec)
      #increment time
      current_time_sec = current_time_sec + tic_sec

   # turn logged vars in a dataframe and plot
   log_df = pd.DataFrame(plotting_vars)
   # create scan visualization
   plotting.create_sim_plot(log_df, radar.beam_width_rad*180/np.pi)


if __name__ == "__main__":
   parser = create_arg_parse()
   args = parser.parse_args()
   print(parser.description)
   print("Your arguements are \n")
   print(f"RadarLocation \t {args.RadarLocation}")
   print(f"Flight \t {args.Flight}")

   flight = create_flight.create_flight(args.Flight)

   radar = create_radar.create_radar(flight, args.RadarLocation)

   # now that we have a flight and a radar postioned, fly it forward

   run(flight, radar)
