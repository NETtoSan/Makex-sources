
 ################################################
 #         A HOLONOMIC MECANUM SOLUTIONS        # 
 # - (C) 2023, NETtoSan                         #
 # - Thai Nichi Institute of Technology         #
 # This is to provide a solutions in which to   #
 # drive mecanum wheel with holonomic aspects   #
 # This is made suitable for odometry purposes  #
 ################################################


from mbuild.encoder_motor import encoder_motor_class
from mbuild import gamepad
import math

encode_fl = encoder_motor_class("M1", "INDEX1")
encode_fr = encoder_motor_class("M2", "INDEX1")
encode_rl = encoder_motor_class("M3", "INDEX1")
encode_rr = encoder_motor_class("M4", "INDEX1")

# Keep bot position
option = 1

# Trigonometry
def pure_persuit():
    global starting_pos
    starting_angle = 90  # novapi.get_rot("Y")

    dX = gamepad.get_joystick("Lx")
    dY = gamepad.get_joystick("Ly")
    rX = gamepad.get_josytick("Rx")

    target_angle =  starting_angle - math.degrees(math.atan2(dY , dX)) if option == 1 else math.degrees(math.atan2(dY, dX))
    power = (abs(dX) + abs(dY)) / 2
    holonomic_xy(power, [target_angle, dX, dY], rX)

def holonomic_xy(power:int, packet:list, rot_speed:int): # Use this for manual code!

    # -- PACKET REQUIREMENTS -- #
    # packet[0] = target_angle
    # packet[1] = x
    # packet[2] = y
    # -- PACKET REQUIREMENTS -- #

    lx = packet[1]        # gamepad.get_joystick("Lx") if not specified in pure_persuit
    ly = packet[2]        # gamepad.get_joystick("Ly") if not specified in pure_persuit
    rot_speed = rot_speed # gamepad.get_joystick("Rx") if not specified in pure_persuit

    theta = math.atan2(ly, lx)
    mPwr = constrain(math.hypot(lx, ly), -100, 100)

    sin = round(math.sin(theta - math.pi / 4))
    cos = round(math.cos(theta - math.pi / 4))
    pmx = max(abs(sin), abs(cos))

    EFl =   ((mPwr * cos/pmx) + rot_speed)  # Motor front left
    EFr = - ((mPwr * sin/pmx) - rot_speed)  # Motor front right
    ERl =   ((mPwr * sin/pmx) + rot_speed)  # Motor back left
    ERr = - ((mPwr * cos/pmx) - rot_speed) # Motor back right

    encode_fl.set_power(EFl)
    encode_fr.set_power(EFr)
    encode_rl.set_power(ERl)
    encode_rr.set_power(ERr)

def isneg(v:int):
    return False if v > 0 else False if v == 0 else True

def constrain(v:int, mn:int, mx:int):
    if v < mn : return mn
    if v > mx : return mx
    return v

while True:
    pass