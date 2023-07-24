

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

encode_arm = encoder_motor_class("M6", "INDEX1")
encode_aim = encoder_motor_class("M5", "INDEX1")
# Test functions #
smart_cam = smart_camera_class("PORT5", "INDEX1")
smart_cam.set_mode("color")
rot_spd = 0
degs = 0     # For rotary motor, debug purposes
heading = 0  # Used in all program aspects
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
def updatePosition():
    global novapi_travelled_x, novapi_travelled_y, novapi_rot, heading, last_time

    # # Test all of these!
    acel_x = round(novapi.get_acceleration("x")) * 100 # in centimeters dipshit # inverted because y is in side
    acel_y = round(novapi.get_acceleration("y")) * 100 # also in centimeters    # inverted because x is in front
    heading = (novapi.get_yaw() + 180) % 360 - 180 # =+ if get_yaw doesnt return a current heading. Only d0/dT

    rheading = ((90 - heading) * math.pi) / 180
    delta_time =  0.2

    vx = acel_x * delta_time
    vy = acel_y * delta_time

    # Convert to relative frame
    vx_world = (vx * math.cos(rheading)) - (vy * math.sin(rheading))
    vy_world = (vx * math.sin(rheading)) + (vy * math.cos(rheading))

    novapi_travelled_x += vx_world * delta_time
    novapi_travelled_y += vy_world * delta_time
    novapi_rot = heading

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
        v = pixel / track_while_scan.get_cam_ppd(320, 65)
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
        global degs
        degs = 0
        if smart_cam.get_sign_x(signature):
            degs = - (smart_cam.get_sign_x(signature) - 160)
        else:
            degs = 0

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

# Necessary for robot's functionality
class challenge_default:
    def __init__ (self):
        self_mode = "default"
    
    # Background task init
    def backgroundProcess():
        challenge_default.rotarydebug()
        track_while_scan.find_target_x(1)
        track_while_scan.lock_target(1)
        updatePosition()

    def rotarydebug():
        global degs
        encode_aim.move_to(degs, 100)

    def gun():
        global track
        power_expand_board.set_power("BL1", 50)
        power_expand_board.set_power("BL2", 50)
        power_expand_board.set_power("DC1", 100)
        if gamepad.is_key_pressed("L1"):
            power_expand_board.set_power("DC3", 100)
        elif gamepad.is_key_pressed("L2"):
            power_expand_board.set_power("DC3", -100)
        else:
            power_expand_board.set_power("DC3", 0)

        if track == True:
            pass
            #rot = rot_spd
    def arm():
        power_expand_board.set_power("BL1", 0)
        power_expand_board.set_power("BL2", 0)
        power_expand_board.set_power("DC1", 0)
        if gamepad.is_key_pressed("L1"):
            encode_arm.set_power(100)
        elif gamepad.is_key_pressed("L2"):
            encode_arm.set_power(-100)
        else:
            encode_arm.set_power(0)
        

    def btn_preferences(buttons, variable:str): # Test this function
        if gamepad.is_key_pressed(buttons):
            if variable == True:
                variable = False
            else:
                variable = True
            pass
            while gamepad.is_key_pressed(buttons):
                pass
        
        return variable

    def auto(x, y, rot):
        global novapi_travelled_x,novapi_travelled_y,novapi_rot
        updatePosition()
        time.sleep(1)
        x_dest = x
        y_dest = y
        rot_dest = rot
        avg = math.sqrt((x * x) + (y * y))
        steps = (avg * 0.01) * 100
        if rot_dest != 0 or novapi_rot != 0:
            steps = steps * 1.1
        heading = 90 - novapi_rot

        counts = 0 # Count if bot stay stationary
        if (x_dest == 0) and (y_dest == 0):
            updatePosition()
            if novapi_rot == rot_dest:
                pass
            elif novapi_rot != rot_dest:
                while novapi_rot != rot_dest:
                    updatePosition()
                    rot_error = keep_upright(rot_dest)
                    heading = 90 - novapi_rot
                    motors.pure_pursuit(0, 0, rot_error, 90) # motors.throttle_curve(rot_error, 0.007, 2)

                    # If the robot stays stationary after course correction
                    if rot_error != 0 or novapi.get_gyroscope("z") == 0:
                        counts += 1
                    if counts == 500:   
                        novapi_rot = rot_dest
                        novapi_travelled_x = x_dest
                        novapi_travelled_y = y_dest
            motors.pure_pursuit(0, 0, 0, heading)

        # course correction
        if (counts < steps):

            while (counts < steps):
                time.sleep(0.01)
                counts += 1
                updatePosition() # novapi_travelled_x and novapi_travelled_y gets updated
                x_error = constrain(x_dest - novapi_travelled_x, -100, 100)
                y_error = constrain(y_dest - novapi_travelled_y, -100, 100)
                rot_error = keep_upright(rot_dest)
                heading = 90 + novapi_rot
                motors.pure_pursuit(-x_error, y_error, rot_error, heading) #motors.throttle_curve(rot_error, 0.007, 2)
                pass
            motors.pure_pursuit(0,0,0, heading) 
            counts = 0
            novapi_travelled_x = x_dest
            novapi_travelled_y = y_dest

    def manual():
        global rot_spd, track, gun
        challenge_default.backgroundProcess()

        x = gamepad.get_joystick("Lx")
        y = gamepad.get_joystick("Ly")
        rot = gamepad.get_joystick("Rx")
        heading = 90

        motors.pure_pursuit(x, y, rot, heading)

        if gamepad.is_key_pressed("N1"):
            if track == False:
                track = True
            else:
                track = False
            while gamepad.is_key_pressed("N1"):
                pass


        # Moved from challenge_runtime
        
        gun = challenge_default.btn_preferences("N4", gun)
        if gun == True:
            challenge_default.gun()
        else:
            challenge_default.arm()

    def challenge_runtime():
        challenge_default.backgroundProcess()
        mode = "select" # select = selectmenu; program = run; anything else = ?

        while mode == "select":
            if gamepad.is_key_pressed("N1"):
                smart_cam_rear = smart_camera_class("PORT5", "INDEX2")
                smart_cam_rear.set_mode("color")

                while True:
                    x_error = 0
                    y_error = 0
                    if(smart_cam_rear.detect_sign(1)):
                        pos_x = smart_cam_rear.get_sign_x(1) - 160
                        pos_y = smart_cam_rear.get_sign_y(1) - 120

                        x_error = motors.throttle_curve(0 - pos_x, 0.005, 2)
                        y_error = motors.throttle_curve(0 - pos_y, 0.005, 2)
                    else:
                        x_error = 0
                        y_error = 0
                    
                    motors.pure_pursuit(0, -y_error, x_error, 90)
            if gamepad.is_key_pressed("N4"):
                mode = "program"
                challenge_default.auto(30, 200, 90)
                challenge_default.auto(-50, 40, 90)
                challenge_default.auto(0, 0, 0)
                while True:
                    challenge_default.manual()
            if gamepad.is_key_pressed("N3"):
                mode = "program"
                while True:
                    challenge_default.manual()
            # Test this
                
challenge_default.challenge_runtime()
#while True:
#    challenge_default.manual()