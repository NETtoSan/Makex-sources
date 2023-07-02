

 ################################################
 #         A HOLONOMIC MECANUM SOLUTIONS        # 
 # - (C) 2023, NETtoSan                         #
 # - Thai Nichi Institute of Technology         #
 # This is to provide a solutions in which to   #
 # drive mecanum wheel with holonomic aspects   #
 # This is made suitable for odometry purposes  #
 ################################################



import math
import random
import keyboard
import os
from time import sleep

# Keep bot position
keep_pos  = False
wheel_size = 58 # In millimeters!. Will do it later
starting_pos = [0,0] # Update this using novapi accelerometer (if present)

def isneg(v:int):
    return False if v > 0 else False if v == 0 else True

def constrain(v:int, mn:int, mx:int):
    if v < mn : return mn
    if v > mx : return mx
    return v

def throttle_curve(v,s):
    return s * (v ** 2)

# Pure persuit
def get_target(sA:int, dX:int, dY:int):
    target_angle = sA - math.degrees(math.atan2(dY , dX))
    return target_angle

def pure_persuit(target_pos, auto):
    global starting_pos
    starting_angle = 90  # novapi.get_rot("Y")
    sensitivity = 0.005

    x = target_pos[0] # Change to gamepad Lx
    y = target_pos[1] # Change to gamepad Ly
    dX = -1 * x
    dY = y 
    rot_speed = 0
    power = constrain(throttle_curve(math.sqrt((dX * dX) + (dY * dY)), sensitivity), -100, 100)
    path = int(math.sqrt((dX * dX) + (dY * dY)))

    target_angle =  get_target(starting_angle, dX, dY)
    angle_to_rotate = starting_angle + target_angle # Convert this to for loop using novapi accelerometer as reference
    print(f"X:{dX} Y:{dY} ; PATH TO TRAVEL:{path} cm ; target_angle: {target_angle} ; bot angle then: {angle_to_rotate}")

    # Holonomic code
    if(auto == True):
        while starting_pos[0] != x or starting_pos[1] != y:
            
            xX = starting_pos[0]
            xY = starting_pos[0]
            print(f"{starting_pos[0]} : {starting_pos[1]}")
            #holonomic_angles(power, [target_angle, dX, dY], rot_speed)
            pass
    else:
        holonomic_angles(power, [target_angle, dX, dY], rot_speed)
    #holonomic_xy(power, [target_angle, dX, dY], rot_speed)

# Angle based holonomic
def holonomic_angles(power:int, packet:list, rot_speed:int): # Use this for auto code!

    #power = power/10
    packet[0] = (packet[0] + 180) % 360 - 180
    angle_rad = math.radians(- packet[0])

    vx = round(power * math.cos(angle_rad))
    vy = round(power * math.sin(angle_rad))

    #if(isneg(packet[0])): vy = -vy
    #if(isneg(packet[0]) or isneg(angle_rad)): vx = -vx

    EFl =   constrain((vx - vy) - rot_speed, -100, 100)
    EFr = - constrain((vx + vy) + rot_speed, -100, 100)
    ERl =   constrain((vx + vy) - rot_speed, -100, 100)
    ERr = - constrain((vx - vy) + rot_speed, -100, 100)

    # --- OUTPUT --- #
    print(f"({vx}) ({vy});   LEFT {EFl} : RIGHT {-EFr} LEFT {ERl} : RIGHT {-ERr}")
    # --- OUTPUT --- #
    
def run(x:int ,y:int, auto:bool):
    global starting_pos, mode
    pure_persuit([x,y], auto)
    print(f"Expected position: {starting_pos}")
    print("-------")
    if(keep_value == True):
        print("KEEP VALUE ON!")

pos = [0, 0]
keep_value = False

mode = "2" # 1 = WASD Manual mode ; 2 = Pure persuit Auto code
# WASD Manual mode
while mode == "1":
    try:
        if keyboard.is_pressed('w') or keyboard.is_pressed('a') or keyboard.is_pressed('s') or keyboard.is_pressed('d'):
            if keyboard.is_pressed('w'):
                pos[1] = pos[1] + 1
            if keyboard.is_pressed('s'):
                pos[1] = pos[1] - 1
            if keyboard.is_pressed('a'):
                pos[0] = pos[0] - 1
            if keyboard.is_pressed('d'):
                pos[0] = pos[0] + 1
        else:
            if keep_value == True:
                pass
            else:
                pos[0] = 0
                pos[1] = 0
        if keyboard.is_pressed("q"):
            if keep_value == False:
                keep_value = True
            else:
                keep_value = False

        if keyboard.is_pressed("r"):
            os.system('clear')
            print("# ---------- ! Reset ! ---------- #")
            pos = [0, 0]
            keep_value = False
            sleep(3)

        run(int(pos[0]),int(pos[1]))
        os.system('cls')
    except SyntaxError:
        print("Error")

# Pure persuit Auto mode 
while mode == "2":
    try:
        pos = input("Enter coordinates to simulate ")
        pos = pos.split(" ")
        run(int(pos[0]),int(pos[1]), True)
    except SyntaxError:
        print("Error")