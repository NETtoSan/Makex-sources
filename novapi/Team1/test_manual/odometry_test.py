 ################################################
 #                 -ODOMETRY-                   # 
 # - (C) 2023, NETtoSan                         #
 # - Thai Nichi Institute of Technology         #
 ################################################
 
 # DISCLAIMER: Code drafed for PBU iRobot 
 # PS:1 This code is for MakeX Challenge 2023

import math
import time

def get_data():
    d = dict()
    d["novapi_x"] = 0
    d["novapi_y"] = 0
    d["novapi_z"] = 0
    d["novapi_gyro_x"] = 0
    d["novapi_gyro_y"] = 0
    d["novapi_gyro_z"] = 0
    d["time"] = time.time()

    return d

x = 0
y = 0
heading = 0
last_time = 0

sensor_data = get_data()


delta_time = sensor_data["time"] - last_time

acel_x = sensor_data["novapi_x"] # Where it faces through 5 mbuild connectors
acel_y = sensor_data["novapi_y"] # Where it faces through 3 encoder motor connectors
yaw = sensor_data["novapi_gyro_z"] # yes

delta_heading = yaw * delta_time
heading += delta_heading

# integrate accel to get change in velocity
vx = acel_x * delta_time
vy = acel_y * delta_time

# velocity to world frame
vx_world = (vx * math.cos(heading)) - (vy * math.sin(heading))
vy_world = (vx * math.sin(heading)) + (vy * math.cos(heading))

x += vx_world * delta_time
y += vy_world * delta_time

# Update timestamp
last_time = sensor_data["time"]

    
