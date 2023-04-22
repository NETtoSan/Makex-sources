import math
from time import sleep

# Pure persuit
def pure_persuit(target_pos):
    global starting_pos
    starting_angle = 90 # novapi.get_rot("Y")

    dX = target_pos[0] - starting_pos[0]
    dY = target_pos[1] - starting_pos[1]
    path = int(math.sqrt((dX * dX) + (dY * dY)))
    target_angle = starting_angle - math.degrees(math.atan2(dY , dX))
    angle_to_rotate = starting_angle + target_angle # Convert this to for loop using novapi accelerometer as reference
    print(f"X:{dX} Y:{dY} ; PATH TO TRAVEL:{path} cm ; target_angle: {target_angle} ; bot angle then: {angle_to_rotate}")

    starting_pos = [target_pos[0], target_pos[1]]


def run(x,y):
    global starting_pos, mode
    print("\n")
    pure_persuit([x,y])
    print(f"Expected position: {starting_pos}")
    print("-------")

'''
Calculating bot travelled distance can be done by [n] amount of rotation * by circumference of the wheel
or measuring from accelerometer altogether (if present)
'''

wheel_size = 58 # In millimeters!. Will do it later
starting_pos = [0,0] # Update this using novapi accelerometer (if present)
mode = "2"

# First iteration
#run(90,50)

# Second iteration
#run(40,30)


while True:
    try:
        pos = input("Enter coordinates to simulate ")
        pos = pos.split(" ")
        run(int(pos[0]),int(pos[1]))
    except SyntaxError:
        print("Error")