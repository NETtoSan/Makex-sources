import math
def vel_from_angle_distance(number1, number2): # arg1: angle (degrees) arg2: distance (meters) 
    #global x, y, velocity, _E0_B9_81, c, a, xf, yf, theta2, x_, mps, velocity_back
    x_ = number2 * (1 / math.cos(number1 / 180.0 * math.pi))
    x = x_
    velocity = math.sqrt((4.9 * (x * x)) / ((math.cos(4 / 180.0 * math.pi) * math.cos(4 / 180.0 * math.pi)) * ((math.tan(4 / 180.0 * math.pi) * x + ))))
    return velocity

def power_to_velocity(power): #Returns m/s from Brushless power precentage
    return 0.2284 * power

def velocity_to_power(velocity): #Returns Brushless power percentage from velocity
    return velocity / 0.2284

def rpm_to_mps(rpm): #Reurns m/s from RPM and Wheel Radius
    #global mps
    mps = (2 * (3.1452 * (0.029 * rpm))) / 60
    return mps

def mps_to_rpm(mps):
    rpm = 60*mps/(2 * (3.1452 * 0.029))
    return rpm

def angle_to_distance(angle,blength) : #for the wheels
    return ( angle / 180 ) * math.pi * blength

def distance_and_time_to_speed(x,t) : 
    return x / t
#y = 0.19
print(angle_to_distance(90,0.5))
print(distance_and_time_to_speed(angle_to_distance(90,0.5),3))
print(mps_to_rpm(distance_and_time_to_speed(angle_to_distance(90,0.5),3)))


print(vel_from_angle_distance(37,180))