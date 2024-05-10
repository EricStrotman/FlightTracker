# Objective
Create an command line application that will use a public flight trajectory and a stationary 'Radar' to display search beams

## Requirements
### Technical
* TODO Trajectory request format
* Provide interface for specifing Radar location [Start, Midcourse, End]
* Radar will scale its power to detect the target for ~half of the flight
* Radar will perform a raster scan pattern
* Simple Radar Range calculation will dictate detections
* Coordinate system will be LLA
### Visual
* Will display the trajectory throughout time in LLA coordinates
* Will display search beam positions throughout time in Radar coordinate frame (Az/El) and will color code detections