from mbuild.encoder_motor import encoder_motor_class
from mbuild.smartservo import smartservo_class
from mbuild.dual_rgb_sensor import dual_rgb_sensor_class
from mbuild import power_expand_board
from mbuild import gamepad
import math

encode_fl = encoder_motor_class("M1", "INDEX1")
encode_fr = encoder_motor_class("M2", "INDEX1")
encode_rl = encoder_motor_class("M3", "INDEX1")
encode_rr = encoder_motor_class("M4", "INDEX1")


def holonomic(power, travelAngle, rotateRate):
    pass

# Keep bot position
keep_pos  = False
option = 1
# Trigonometry
def pure_persuit(target_pos):
    global starting_pos
    starting_angle = 90  # novapi.get_rot("Y")

    dX = target_pos[0] - starting_pos[0]
    dY = target_pos[1] - starting_pos[1]
    path = int(math.sqrt((dX * dX) + (dY * dY)))

    target_angle =  starting_angle - math.degrees(math.atan2(dY , dX)) if option == 1 else math.degrees(math.atan2(dY, dX))
    angle_to_rotate = starting_angle + target_angle # Convert this to for loop using novapi accelerometer as reference
    print(f"X:{dX} Y:{dY} ; PATH TO TRAVEL:{path} cm ; target_angle: {target_angle} ; bot angle then: {angle_to_rotate}")

    if keep_pos is True: starting_pos = [target_pos[0], target_pos[1]]
    else: pass


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