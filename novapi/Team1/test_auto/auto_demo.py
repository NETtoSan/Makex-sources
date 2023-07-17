# auto bot rot code test 

# reserch code, can be adapted competition ready
# thai nichi institute of technology 
# piboonbumpen demonstration school burapha university
# kasetsart university
# kasetsart laboratory school multilanguage program ( bro ur name so long na )

# auto error in rot d

import novapi
import time, math
from mbuild.encoder_motor import encoder_motor_class

# motors
encode_fl = encoder_motor_class("M1", "INDEX1")
encode_fr = encoder_motor_class("M2", "INDEX1")
encode_rl = encoder_motor_class("M3", "INDEX1")
encode_rr = encoder_motor_class("M4", "INDEX1")

# Plot
target_rot = 0
bot_rot = (novapi.get_yaw() + 180) % 360 - 180

def isneg(v):
    return False if v > 0 else False if v == 0 else True

def constrain(v, mn, mx):
    if v < mn : return mn
    if v > mx : return mx
    return v

def drive(x,y,rot): # โค้ด holonomic 
    heading = math.degrees(math.atan2(y, x))
    power = constrain(math.sqrt((x * x) + (y * y)), -100, 100)

    radians = math.radians((heading + 180) % 360 - 180)
    vx = round(power * math.cos(radians))
    vy = round(power * math.sin(radians))

    encode_fl.set_power(  constrain((vx - vy) - rot, -100, 100))
    encode_fr.set_power(- constrain((vx + vy) + rot, -100, 100))
    encode_rl.set_power(  constrain((vx + vy) - rot, -100, 100))
    encode_rr.set_power(- constrain((vx - vy) + rot, -100, 100))

def update_bot_rot():
    global bot_rot
    bot_rot = (novapi.get_yaw() + 180) % 360 - 180 #(novapi.get_yaw() + 180) % 360 - 180

def rot_bot_dest(rot):
    global bot_rot

    while bot_rot != rot:
        error = constrain(round(rot - bot_rot), -100, 100) # diff between bot and rot dest
        drive(0,0, error/ 2)                               # drive
        update_bot_rot()                                   # update bot rot

    drive(0,0,0)
    time.sleep(1)


# Test bot rotation in sequences
#rot_bot_dest(90)   # หมุนรอบที่ 1

drive(0,30,0)
time.sleep(1)
drive(0,0,0)