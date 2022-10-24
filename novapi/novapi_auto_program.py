import novapi
import time
from mbuild import gamepad
from mbuild import power_expand_board
from mbuild.dual_rgb_sensor import dual_rgb_sensor_class
from mbuild.smartservo import smartservo_class
from mbuild.encoder_motor import encoder_motor_class


auto_stage = 0
modes = ["index0 pls fix", "shoot", "cube"]
colors = ['0x33FFEC', '0xFF3333', '0xFF333']


#Switch to INDEX1 and INDEX3 if we only have short wires
smartservo_arm = smartservo_class("M6", "INDEX1")
smartservo_turret = smartservo_class("M5", "INDEX1")

#Motors
motor1 = encoder_motor_class("M1", "INDEX1")
motor2 = encoder_motor_class("M2", "INDEX1")
motor3 = encoder_motor_class("M3", "INDEX1")
motor4 = encoder_motor_class("M4", "INDEX1")


class AutoAssets:
    def __init__(self):
        pass

    def MoveForward():
        pass

    def MoveBackward():
        pass

    def RotateLeft():
        pass

    def RotateRight():
        pass

    def Shoot():
        pass

    def GetDistance():
        pass


def AutoStart():
    global auto_stage
    #Move bot 10 secs
    #Measure distance between bot and ball
    #If near collect ball, rotate 90' and shoot
    #When done, quit
    pass


auto_stage = 0
while True:
    time.sleep(0.001)
    if auto_stage == 1:
        AutoStart()
        auto_stage = 0
    else:
        pass
