

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
from mbuild.smartservo import smartservo_class
from mbuild import gamepad
import math
import time
import novapi

encode_fl = encoder_motor_class("M1", "INDEX1")
encode_fr = encoder_motor_class("M2", "INDEX1")
encode_rl = encoder_motor_class("M3", "INDEX1")
encode_rr = encoder_motor_class("M4", "INDEX1")

servo_arm = smartservo_class("M5", "INDEX1")

heading = 0  # Used in all program aspects
feedroller = True


novapi_rot = 0
# Test functions #

# Built functions to conpensate missing python functions
def isneg(v):
    return False if v > 0 else False if v == 0 else True

def constrain(v, mn, mx):
    if v < mn : return mn
    if v > mx : return mx
    return v

# Background tasks

def keep_upright(target_rot):
    bot_rot = novapi.get_yaw() # Change this to match your NovaPi placements
    diff = ((target_rot - bot_rot) - 180) % 360 - 180
    return diff

# Class
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
    def pure_pursuit(x:int, y:int, rot:int, heading:int):
        starting_angle = heading
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

class modes:
    def arm():
        power_expand_board.set_power("DC3", gamepad.get_joystick("Ry"))
        if gamepad.is_key_pressed("L1"):
            servo_arm.set_power(50)
        elif gamepad.is_key_pressed("R1"):
            servo_arm.set_power(-50)
        else:
            servo_arm.set_power(0)

    def gun():
        power_expand_board.set_power("BL1", 10)
        power_expand_board.set_power("BL2", 10)

    def feed():
        global feedroller
        if gamepad.is_key_pressed("N4"):
            power_expand_board.set_power("DC2", 100)
        else:
            power_expand_board.stop("DC2")
        if(gamepad.is_key_pressed("N3")):
            if feedroller == True:
                feedroller = False
            else:
                feedroller = True
            while gamepad.is_key_pressed("N3"):
                pass

        if feedroller == True:
            power_expand_board.set_power("DC1", 100)
        else:
            power_expand_board.stop("DC1")

# Necessary for robot's functionality
class challenge_default:
    def __init__ (self):
        self_mode = "default"
    
    # Background task init
    def backgroundProcess():
        pass
        
    def auto(x, y, rot):
        pass

    def manual():
        challenge_default.backgroundProcess()

        x = gamepad.get_joystick("Lx")
        y = gamepad.get_joystick("Ly")
        rot = gamepad.get_joystick("Rx") /2
        heading = 90

        motors.pure_pursuit(x, y, rot, heading)

    def force_manual():
        # Force manual code for automatic stage
        while True:
            challenge_default.manual()

    def challenge_runtime():
        challenge_default.backgroundProcess()
        challenge_default.manual()
        modes.arm()
        modes.feed()
        modes.gun()
                
#challenge_default.challenge_runtime()
while True:
    challenge_default.challenge_runtime()