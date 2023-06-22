 

################################################
 #         A HOLONOMIC MECANUM SOLUTIONS        # 
 # - (C) 2023, NETtoSan                         #
 # - Thai Nichi Institute of Technology         #
 #                                              #
 # This is to provide a solution in which to    #
 # drive mecanum wheel with holonomic aspects   #
 # This is made suitable for odometry purposes  #
 ################################################
 # For Piboonbumpen demonstration school Burapha#
 # University ONLY!                             #
 ################################################



from mbuild.encoder_motor import encoder_motor_class
from mbuild import gamepad
import math

encode_fl = encoder_motor_class("M1", "INDEX1")
encode_fr = encoder_motor_class("M2", "INDEX1")
encode_rl = encoder_motor_class("M3", "INDEX1")
encode_rr = encoder_motor_class("M4", "INDEX1")


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

# Find relative path
def pure_persuit():
    starting_angle = 90  # novapi.get_rot("Y")

    dX = gamepad.get_joystick("Lx")
    dY = gamepad.get_joystick("Ly")
    rX = gamepad.get_joystick("Rx")

    target_angle =  starting_angle - math.degrees(math.atan2(dY , dX))
    power = constrain(math.sqrt((dX * dX) + (dY * dY)) * 10, -100, 100)
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

while True:
    pure_persuit()
    pass