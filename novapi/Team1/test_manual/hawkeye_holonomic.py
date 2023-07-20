

 ################################################
 #         A HOLONOMIC MECANUM SOLUTIONS        # 
 # - (C) 2023, NETtoSan                         #
 # - Thai Nichi Institute of Technology         #
 # This is to provide a solution in which to    #
 # drive mecanum wheel with holonomic aspects   #
 # This is made suitable for odometry purposes  #
 ################################################
 
 # PS:1 This code DOES NOT provide full challenge bot capabilities
 #      This only supplements necessary function to drive all 4 mecanum wheels
 #      If you need full functionality, please use ./hawkeye_main_program.py
 # PS:2 Rapid holonomic code change may occur. View latest holonomic simulation code via
 #      ../simulator/{pid_test or pure_persuit}.py

from mbuild import power_expand_board
from mbuild.encoder_motor import encoder_motor_class
from mbuild.smart_camera import smart_camera_class
from mbuild import gamepad
import math
import time
import novapi

encode_fl = encoder_motor_class("M1", "INDEX1")
encode_fr = encoder_motor_class("M2", "INDEX1")
encode_rl = encoder_motor_class("M3", "INDEX1")
encode_rr = encoder_motor_class("M4", "INDEX1")

# Test functions #
smart_cam = smart_camera_class("PORT5", "INDEX1")
smart_cam.set_mode("color")
rot_spd = 0
heading = 0  # Used in all program aspects
last_time = time.time() # For odometry purposes
track = True
gun = True # True = gun; False = arm

# --- PID --- #
kp = 0
ki = 0
kd = 0
ks = 0
# --- PID --- #

novapi_travelled_x = 0 # Needs to be updated every time. Missing equation!
novapi_travelled_y = 0 # Needs to be updated every time. Missing equation!
# Test functions #

# Built functions to conpensate missing python functions
def isneg(v):
    return False if v > 0 else False if v == 0 else True

def constrain(v, mn, mx):
    if v < mn : return mn
    if v > mx : return mx
    return v

# Background tasks
def updatePosition():
    global novapi_travelled_x, novapi_travelled_y, heading, last_time
    time_now = time.time()

    # Test all of these!
    acel_x += novapi.get_acceleration("x")
    acel_y += novapi.get_acceleration("y")
    heading = (novapi.get_yaw() + 180) % 360 - 180 # =+ if get_yaw doesnt return a current heading. Only d0/dT

    rheading = (heading * math.pi) / 180
    delta_time = time_now - last_time

    vx = acel_x * delta_time
    vy = acel_y * delta_time

    # Convert to relative frame
    vx_world = (vx * math.cos(rheading)) - (vy * math.sin(rheading))
    vy_world = (vx * math.sin(rheading)) + (vy * math.cos(rheading))

    novapi_travelled_x += vx_world * delta_time
    novapi_travelled_y += vy_world * delta_time

    last_time = time_now

def keep_upright(target_rot):
    bot_rot = novapi.get_yaw() # Change this to match your NovaPi placements
    diff = ((target_rot - bot_rot) - 180) % 360 - 180
    return diff

# Class
class track_while_scan:
    def lock_target(signature:int):
        global rot_spd
        if smart_cam.detect_sign(signature):
            rot_spd = ( smart_cam.get_sign_x(signature) - 160 ) * -0.5
        else:
            rot_spd = 0
        
        return rot_spd
    
    # Camera degree thing. Could be useful to lock target with servo
    def get_object_deg(pixel:int):
        v = pixel / track_while_scan.get_cam_ppd(pixel, 65)
        return v 
    def get_cam_ppd(pixel:int, fov_deg:int):
        #ppd = pixel-per-degree
        return pixel / fov_deg
    # Camera degree thing

    # An extra target lock using servos. While using camera to scan for objects
    # Similar to Radar's ACM Mode, (Yes i've played too much War Thunder)
    def find_target(signature:int):
        pass

    def find_target_x(signature:int):
        pass

class motors:
    # Drive all the motors in one go
    def drive(v1:int, v2:int, v3:int, v4:int):
        encode_fl.set_power(v1)
        encode_fr.set_power(v2)
        encode_rl.set_power(v3)
        encode_rr.set_power(v4)
        
    # Calculate motor power using y = x theorem
    def throttle_curve(v:int, s:float, e:int):
        # Using formula y = s * (x-h)^e, but s = a, e = N; N = 2 parabola; N = 3 polynomial
        return s * (v ** e)
    
    # Find relative path
    def pure_pursuit(x:int, y:int, rot:int):
        starting_angle = 90
        dX = (-1 * x * 0.3)
        dY = (y * 0.3)
        rX = rot

        target_angle =  starting_angle - math.degrees(math.atan2(dY , dX))
        power = constrain(motors.throttle_curve(math.sqrt((dX * dX) + (dY * dY)), 0.005, 2) * 10, -100, 100)
        

        motors.holonomic(power, [target_angle, dX, dY], rX)

    # Calculate each motor power to travel
    def holonomic(power:float, packet:list, rot_speed:int): # Use this for auto code!

        #packet = ["angle", "dX", "dY"]
        packet[0] = (packet[0] + 180) % 360 - 180
        angle_rad = math.radians(- packet[0])

        vx = round(power * math.cos(angle_rad))
        vy = round(power * math.sin(angle_rad))

        EFl =   constrain((vx - vy) - rot_speed, -100, 100)
        EFr = - constrain((vx + vy) + rot_speed, -100, 100)
        ERl =   constrain((vx + vy) - rot_speed, -100, 100)
        ERr = - constrain((vx - vy) + rot_speed, -100, 100)

        motors.drive(EFl, EFr, ERl, ERr)

# Necessary for robot's functionality
class challenge_default:
    def __init__ (self):
        self_mode = "default"
    
    # Background task init
    def backgroundProcess():
        track_while_scan.lock_target(1)
        updatePosition()

    
    def gun():
        power_expand_board.set_power("BL1", 20)
        power_expand_board.set_power("BL2", 20)
        
    def arm():
        power_expand_board.set_power("BL1", 0)
        power_expand_board.set_power("BL2", 0)

    def btn_preferences(buttons, variable:str, switching:list): # Test this function
        if gamepad.is_key_pressed(buttons):
            if variable == switching[1]:
                variable = switching[2]
            else:
                variable = switching[1]
            pass

        return variable

    def auto(coords_list:list):

        for coordinate in coords_list:
            updatePosition()

            time.sleep(1)
            motors.pure_pursuit(coordinate[0], coordinate[1], 0)
            x_dest = coordinate[0]
            y_dest = coordinate[1]

            # Loop around until current = dest
            while (novapi_travelled_x != x_dest) and (novapi_travelled_y != y_dest):
                updatePosition() # novapi_travelled_x and novapi_travelled_y gets updated
                x_error = x_dest - novapi_travelled_x
                y_error = y_dest - novapi_travelled_y
                rot_error = keep_upright(0)

                pass


    def manual():
        global rot_spd, track, gun
        challenge_default.backgroundProcess()

        x = gamepad.get_joystick("Lx")
        y = gamepad.get_joystick("Ly")
        rot = gamepad.get_joystick("Rx")

        if gamepad.is_key_pressed("N1"):
            if track == False:
                track = True
            else:
                track = False
            while gamepad.is_key_pressed("N1"):
                pass

        if track == True:
            rot = rot_spd

        motors.pure_pursuit(x, y, rot)


        # Moved from challenge_runtime
        gun = challenge_default.btn_preferences("N4", gun, [True, False])
        if gun == True:
            challenge_default.gun()
        else:
            challenge_default.arm()

    def challenge_runtime():
        challenge_default.backgroundProcess()
        mode = "select" # select = selectmenu; program = run; anything else = ?

        while mode == "select":
            if gamepad.is_key_pressed("N1"):
                mode = "program"

            if gamepad.is_key_pressed("N4"):
                mode = "program"

            if gamepad.is_key_pressed("N3"):
                mode = "program"
                while True:
                    challenge_default.manual()
            # Test this
                
challenge_default.challenge_runtime()