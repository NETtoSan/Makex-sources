import math
from time import sleep
import random

# Keep bot position
keep_pos  = False
option = 1
wheel_size = 58 # In millimeters!. Will do it later
starting_pos = [0,0] # Update this using novapi accelerometer (if present)
mode = "2"

# Pure persuit
def pure_persuit(target_pos):
    global starting_pos
    starting_angle = 90  # novapi.get_rot("Y")

    dX = target_pos[0] - starting_pos[0] # Change to gamepad Lx
    dY = target_pos[1] - starting_pos[1] # Change to gamepad Ly
    path = int(math.sqrt((dX * dX) + (dY * dY)))

    target_angle =  starting_angle - math.degrees(math.atan2(dY , dX)) if option == 1 else math.degrees(math.atan2(dY, dX))
    angle_to_rotate = starting_angle + target_angle # Convert this to for loop using novapi accelerometer as reference
    print(f"X:{dX} Y:{dY} ; PATH TO TRAVEL:{path} cm ; target_angle: {target_angle} ; bot angle then: {angle_to_rotate}")

    if keep_pos is True: starting_pos = [target_pos[0], target_pos[1]]

    # Holonomic code
    power = (dX + dY) / 2 
    rot_speed = 0 # gamepad.get_joysticl("Rx")

    # This code calcultes time to run the motors
    duration = power # Dummy code
    '''
    # This code updates novapi location using novapi accelerometers
    novapi_x = 0
    novapi_y = 0
    while novapi_x != dX or novapi_y != dY:
        holonomic(power, [target_angle, dX, dY], rot_speed)
        if novapi_x != dX : novapi_x += 1 #if isneg(dX) is False else - random.randint(0, 3) # Change this to novapi accel FRONT
        if novapi_y != dY : novapi_y += 1 #if isneg(dY) is False else - random.randint(0, 3) # Change this to novapi accel SIDE RIGHT
        sleep(0.01)
        print(f"{novapi_x}: {dX}, {novapi_y}: {dY}")
    '''
    holonomic(power, [target_angle, dX, dY], rot_speed)
    #sleep(duration)

    #sleep(x)

def holonomic(power, packet, rot_speed):

    # -- PACKET REQUIREMENTS -- #
    # packet[0] = target_angle
    # packet[1] = x
    # packet[2] = y
    # -- PACKET REQUIREMENTS -- #

    lx = packet[1]        # gamepad.get_joystick("Lx")
    ly = packet[2]        # gamepad.get_joystick("Ly")
    rot_speed = rot_speed # gamepad.get_joystick("Rx")
    angles = packet[0]    # default_angle, unused!
    theta = math.atan2(ly, lx)
    mPwr = constrain(math.hypot(lx, ly), -100, 100)

    sin = round(math.sin(theta - math.pi / 4))
    cos = round(math.cos(theta - math.pi / 4))
    pmx = max(abs(sin), abs(cos))

    EFl = mPwr * cos/pmx + rot_speed  # Motor front left
    EFr = -mPwr * sin/pmx - rot_speed # Motor front right
    ERl = mPwr * sin/pmx + rot_speed  # Motor back left
    ERr = -mPwr * cos/pmx - rot_speed # Motor back right
    

    # --- OUTPUT --- #
    print(f"------\nACTUAL POWER\nLEFT {EFl} : RIGHT {EFr}\nLEFT {ERl} : RIGHT {ERr}\n--- OUTPUT CODE\nLEFT: {EFl} : RIGHT {-EFr}\nLEFT : {ERl} : RIGHT {-ERr}\n\n")
    # --- OUTPUT --- #

    #print(f"OVERALL POWER\npure_persuit: {power} , holonomic: {mPwr}\nmax: {pmx}")
    #print(f"{angles} : {total} : {total2}")
    #print(f"{angles} : {theta}\n{angles} : {mPwr}\n{angles} : {sin}\n{angles} : {cos}\n{angles} : {pmx}")

def isneg(v):
    return False if v > 0 else False if v == 0 else True

def constrain(v,mn,mx):
    if v < mn : return mn
    if v > mx : return mx
    return v

def run(x,y):
    global starting_pos, mode
    print("\n")
    pure_persuit([x,y])
    print(f"Expected position: {starting_pos}")
    print("-------")

while True:
    try:
        pos = input("Enter coordinates to simulate ")
        pos = pos.split(" ")
        run(int(pos[0]),int(pos[1]))
    except SyntaxError:
        print("Error")