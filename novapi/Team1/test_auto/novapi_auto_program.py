import novapi
import time
from mbuild import gamepad
from mbuild import power_expand_board
from mbuild.dual_rgb_sensor import dual_rgb_sensor_class
from mbuild.smartservo import smartservo_class
from mbuild.encoder_motor import encoder_motor_class
from mbuild.ranging_sensor import ranging_sensor_class


auto_stage = 0
modes = ["index0 pls fix", "shoot", "cube"]
colors = ['0x33FFEC', '0xFF3333', '0xFF333']


# Switch to INDEX1 and INDEX3 if we only have short wires
smartservo_arm = smartservo_class("M6", "INDEX1")
smartservo_turret = smartservo_class("M5", "INDEX1")

# Ranging sensor
distance_sensor_1 = ranging_sensor_class("PORT3", "INDEX1")
distance_sensor_arm = ranging_sensor_class("PORT3", "INDEX2")

# LED Lights. For testing
dual_rgb_sensor_1 = dual_rgb_sensor_class("PORT2", "INDEX1")
dual_rgb_sensor_2 = dual_rgb_sensor_class("PORT2", "INDEX2")

# Motors
motor1 = encoder_motor_class("M1", "INDEX1")
motor2 = encoder_motor_class("M2", "INDEX1")
motor3 = encoder_motor_class("M3", "INDEX1")
motor4 = encoder_motor_class("M4", "INDEX1")


class MovementAsset:
    def __init__(self):
        pass

    def move(v1, v2, v3, v4):
        motor1.set_power(v1)
        motor2.set_power(v2)
        motor3.set_power(v3)
        motor4.set_power(v4)

    def stop():
        motor1.set_power(0)
        motor2.set_power(0)
        motor3.set_power(0)
        motor4.set_power(0)


class AutoAssets:
    def __init__(self):
        pass

    def MoveForward():
        MovementAsset.move(25, -25, 25, -25)
        pass

    def MoveBackward():
        MovementAsset.move(-25, 25, -25, 25)
        pass

    def RotateLeft():
        MovementAsset.move(-50, -50, -50, -50)
        pass

    def RotateRight():
        MovementAsset.move(50, 50, 50, 50)
        pass
    def StopMoving():
        MovementAsset.move(0, 0, 0, 0)
    def Shoot():
        power_expand_board.set_power("DC3", 100)
        pass

    # Return value functions

    def getSelfAngle():

        angle = [novapi.get_pitch(), novapi.get_roll(), novapi.get_yaw()]
        return angle


    def GetDistance():
        # GetDistance utilizes a ranging sensor Module
        # What it does is detects an object in front of it
        # And returns a distance value as number

        range = distance_sensor_1.get_distance()

        return range

    # Presets

    def ShootRoutine():
        dual_rgb_sensor_1.set_led_color("red")
        dual_rgb_sensor_2.set_led_color("red")
        time.sleep(1)    

        power_expand_board.set_power("DC2",70)
        power_expand_board.set_power("DC1",-100)
        power_expand_board.set_power("DC3", 75)
        
        AutoAssets.MoveForward()
        time.sleep(0.5)
        AutoAssets.RotateLeft()
        time.sleep(0.25)

        AutoAssets.MoveForward()
        time.sleep(2)
        AutoAssets.RotateRight()
        time.sleep(0.2)
        
        AutoAssets.MoveForward()
        power_expand_board.set_power("BL1",100)
        power_expand_board.set_power("BL2",100)
        time.sleep(1.25)

        AutoAssets.StopMoving()
        dual_rgb_sensor_2.set_led_color("green")

        time.sleep(10)
        for i in range(10):
            dual_rgb_sensor_1.set_led_color("blue")
            AutoAssets.RotateLeft()
            time.sleep(0.1)
            AutoAssets.StopMoving()
            dual_rgb_sensor_1.set_led_color("red")
            time.sleep(0.2)

        pass

    def EmbraceBallRoutine():

        pass

    def GrabCubeRoutine():

        pass


def AutoStart():
    global auto_stage
    # Move bot 10 secs
    # Measure distance between bot and ball
    # If near collect ball, rotate 90' and shoot ^ Above code are now inside AutoAssets.ShootRoutine()
    # When done, quit' 

    AutoAssets.ShootRoutine()

    dual_rgb_sensor_1.set_led_color("green")
    dual_rgb_sensor_2.set_led_color("green")
    time.sleep(1)
    pass


auto_stage = 1
while True:
    time.sleep(0.001)
    if auto_stage == 1:
        AutoStart()
        #auto_stage = 0
    else:
        dual_rgb_sensor_1.set_led_color("blue")
        dual_rgb_sensor_2.set_led_color("blue")
        pass