

 ################################################
 #         A HOLONOMIC MECANUM SOLUTIONS        # 
 # - (C) 2023, NETtoSan                         #
 # - Thai Nichi Institute of Technology         #
 # This is to provide a solutions in which to   #
 # drive mecanum wheel with holonomic aspects   #
 # This is made suitable for odometry purposes  #
 ################################################



from mbuild.encoder_motor import encoder_motor_class
from mbuild.smart_camera import smart_camera_class
from mbuild import gamepad
import math
import novapi

encode_fl = encoder_motor_class("M1", "INDEX1")
encode_fr = encoder_motor_class("M2", "INDEX1")
encode_rl = encoder_motor_class("M3", "INDEX1")
encode_rr = encoder_motor_class("M4", "INDEX1")
smart_cam = smart_camera_class("PORT1", "INDEX1")

# Set smart camera mode to COLOR!
smart_cam.set_mode("color")

rot_spd = int
track = False

# ---- PID ---- #
kp = 0
ki = 0
kd = 0
ks = 0
# ---- PID ---- #


# BACKGROUND PROCESS. PUT STUFFS IN IF YOU NEED TO RUN SOMETHING!
def backgroundProcess():
    lock_target(1) # track ball

# Built functions to conpensate missing python functions
def isneg(v):
    return False if v > 0 else False if v == 0 else True

def constrain(v, mn, mx):
    if v < mn : return mn
    if v > mx : return mx
    return v

def drive(v1, v2, v3, v4):
    encode_fl.set_power(v1)
    encode_fr.set_power(v2)
    encode_rl.set_power(v3)
    encode_rr.set_power(v4)

def throttle_curve(v,s):
    return s * (v ** 2)


# Find relative path
def pure_persuit(x, y, rot, auto:bool):
    starting_angle = 90  # novapi.get_rot("Y") # Subtract starting angle. Which is exactly 90 degrees away.
    sensitivity = 0.005 # 0 <----> 0.01 ; The less the wider, the less sensitive it will be
                        # 0.01 = 1 : 1 input to power ratio. 
                        # 0.00 = 0. No power will be provided. (value * power) ; power = 0, motor_power = 0

    dX = -1 * x
    dY = y
    rX = rot

    target_angle =  starting_angle - math.degrees(math.atan2(dY , dX))
    power = constrain(throttle_curve(math.sqrt((dX * dX) + (dY * dY)), sensitivity) * 10, -100, 100)
    holonomic(power, [target_angle, dX, dY], rX)

# Calculate each motor power to travel
def holonomic(power, packet, rot_speed): # Use this for auto code!

    #power = power/10
    packet[0] = (packet[0] + 180) % 360 - 180
    angle_rad = math.radians(- packet[0])

    vx = round(power * math.cos(angle_rad))
    vy = round(power * math.sin(angle_rad))

    EFl =   constrain((vx - vy) - rot_speed, -100, 100)
    EFr = - constrain((vx + vy) + rot_speed, -100, 100)
    ERl =   constrain((vx + vy) - rot_speed, -100, 100)
    ERr = - constrain((vx - vy) + rot_speed, -100, 100)

    drive(EFl, EFr, ERl, ERr)

# --- TEST ---- #
def find_rot_pid(s, t):

    error = t - s
    integral = integral + (error * 0.25)
    derivative = error - prev_error
    prev_error = error
    start = (s - t)
    tpower = (error * kp) + (integral*ki) + (derivative*kd)  + (start*ks)

    # Limit values between -100 and 100
    tpower = constrain(tpower, -100, 100)
    return int(tpower)

def lock_target(signature): # lock target -> find object -> track target
    global rot_spd
    if find_object(signature):
        rot_spd = track_target(signature)
    else:
        rot_spd = 0
        
def find_object(signature):
    stat = bool
    if not smart_cam: return False # Returns false if a camera is not detected

    if smart_cam.detect_sign(signature): # Change this !. This is a theoretical code
        stat = True
    else:
        stat = False
    
    return stat

def track_target(signature):
    distance = float
    distance = smart_cam.get_sign_x(signature) # Change this !. This is a theoretical code

    # Ways to find PID for rotation speed!
    distance = find_rot_pid(0, distance)                          # Change this if it doesnt work!
    distance = smart_cam.get_sign_diff_speed(signature, "x", 160) # A makeblock's official way
    return distance
# ---- TEST ---- #

def Manual():
    backgroundProcess() # Run process in the background. 1st priority

    x = gamepad.get_joystick("Rx"),
    y = gamepad.get_joystick("Lx"),
    rx = gamepad.get_joystick("Rx")

    # Toggle target tracking mode
    if gamepad.is_key_pressed("N1"):
        if track == True:
            track = False
        else:
            track = True

    
    # Switch to target tracking mode to rotate bot
    if track is True:
        rx = rot_spd # The function is already called in backgroundProcess()
    else:
        rx = gamepad.get_joystick("Rx")

    pure_persuit(x, y, rx, False)

def Auto():
    pure_persuit(0, 100, rot_spd, True)
    pure_persuit(300, 0, rot_spd, True)

    Manual()

while True:
    #Manual()
    #Auto()
    pass