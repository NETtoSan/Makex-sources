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


# Switch to INDEX1 and INDEX3 if we only have short wires
smartservo_arm = smartservo_class("M6", "INDEX1")
smartservo_turret = smartservo_class("M5", "INDEX1")

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


class AutoAssets:
    def __init__(self):
        pass

    def MoveForward():
        MovementAsset.move(50, -50, 50, -50)
        pass

    def MoveBackward():
        MovementAsset.move(-50, 50, -50, 50)
        pass

    def RotateLeft():
        MovementAsset.move(-50, -50, -50, -50)
        pass

    def RotateRight():
        MovementAsset.move(50, 50, 50, 50)
        pass

    def Shoot():
        pass

    def ShootRoutine():
        # Suppose the bot moves forward with a timed sequence
        AutoAssets.MoveForward()
        time.sleep(1)

        # or according to distance between itself and a ball
        distance = AutoAssets.GetDistance()
        if distance > 5:
            while distance > 1:
                AutoAssets.MoveForward()
                distance = AutoAssets.GetDistance()

        # Rotate bot 90 (suppose the moves 45'/sec)
        AutoAssets.RotateLeft()
        time.sleep(2)
        
        # The actual shooting mode. once the ball is loaded into the compartment
        orientation = AutoAssets.GetSelfAngle()[2]
        while orientation != 0:
            while orientation < 45:
                AutoAssets.RotateRight()
                time.sleep(0.5)
                AutoAssets.shoot()
                time.sleep(1)
                orientation = AutoAssets.getSelfAngle()[2]

        AutoAssets.shoot()

        pass

    def getSelfAngle():
        # GetSelfAngle utilizes its own accelerometer
        # What it does is obtain its own XYZ orientation
        # And returns an orientation value as array

        angle = [0, 0, 0]

        return angle
        pass

    def GetDistance():
        # GetDistance utilizes a ranging sensor Module
        # What it does is detects an object in front of it
        # And returns a distance value as number

        range = 0  # Replace 0 with an appropriate ranging sensor code

        return range
        pass


def AutoStart():
    global auto_stage
    # Move bot 10 secs
    # Measure distance between bot and ball       
    # If near collect ball, rotate 90' and shoot ^ Above code are now inside AutoAssets.ShootRoutine()
    # When done, quit'
    dual_rgb_sensor_1.set_led_color("red")
    dual_rgb_sensor_2.set_led_color("red")

    AutoAssets.MoveForward()
    time.sleep(2)
    AutoAssets.MoveBackward()
    time.sleep(2)
    AutoAssets.RotateRight()
    time.sleep(2)
    AutoAssets.RotateLeft()
    time.sleep(2)

    dual_rgb_sensor_1.set_led_color("green")
    dual_rgb_sensor_2.set_led_color("green")
    time.sleep(5)
    #AutoAssets.ShootRoutine()
    pass


auto_stage = 0
while True:
    time.sleep(0.001)
    if auto_stage == 1:
        AutoStart()
        auto_stage = 0
    else:
        dual_rgb_sensor_1.set_led_color("blue")
        dual_rgb_sensor_2.set_led_color("blue")
        pass
