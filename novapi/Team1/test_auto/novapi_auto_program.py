import novapi
import time
from mbuild import gamepad
from mbuild import power_expand_board
from mbuild.dual_rgb_sensor import dual_rgb_sensor_class
from mbuild.smartservo import smartservo_class
from mbuild.encoder_motor import encoder_motor_class
from mbuild.ranging_sensor import ranging_sensor_class


auto_stage = 0
movement_prefix = {
    "fw": [ 50, -50, 50, -50],
    "bw": [ -50, 50, -50, 50],
    "rl": [ -50, -50, -50, -50],
    "rr": [ 50, 50, 50, 50]
}


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

    # This def controls and linears bot motor power graph
    def TranscodeMotorValues(v1, v2, v3, v4):
        # Set everything to default. Move bot forward
        if not v1:
            v1 = 50
        if not v2:
            v2 = -50
        if not v3:
            v3 = 50
        if not v4:
            v4 = -50
        MovementAsset.move(v1, v2, v3, v4)

    # This def controls and linears bot motor power using provided movement prefixes
    def TranscodeMotorModes(mode):
        v1 = 0 ; v2 = 0 ; v3 = 0 ; v4 = 0

        if movement_prefix[mode]:
            pass

    def stop():
        MovementAsset.TranscodeMotorValues(0, 0, 0, 0)


class AutoAssets:
    def __init__(self):
        pass

    def MoveForward(v1, v2, v3, v4):
        if not v1:
            v1 = 50
        if not v2:
            v2 = -50
        if not v3:
            v3 = 50
        if not v4:
            v4 = -50

        MovementAsset.TranscodeMotorValues(v1, v2, v3, v4)

    def MoveBackward(v1, v2, v3, v4):
        if not v1:
            v1 = -50
        if not v2:
            v2 = 50
        if not v3:
            v3 = -50
        if not v4:
            v4 = 50

        MovementAsset.TranscodeMotorValues(v1, v2, v3, v4)

    def RotateLeft(v1, v2, v3, v4):
        if not v1:
            v1 = -50
        if not v2:
            v2 = -50
        if not v3:
            v3 = -50
        if not v4:
            v4 = -50

        MovementAsset.TranscodeMotorValues(v1, v2, v3, v4)

    def RotateRight(v1, v2, v3, v4):
        if not v1:
            v1 = 50
        if not v2:
            v2 = 50
        if not v3:
            v3 = 50
        if not v4:
            v4 = 50

        MovementAsset.TranscodeMotorValues(v1, v2, v3, v4)

    def StopMoving():
        MovementAsset.TranscodeMotorValues(0, 0, 0, 0)

    def Shoot():
        power_expand_board.set_power("DC3", 100)
        pass

    # Return value functions

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

        range = distance_sensor_1.get_distance()

        return range

    # Presets

    def ShootRoutine():
        # LED STATUS
        # red = done
        # green = doing

        # Enable ball feed fx
        power_expand_board.set_power("DC2", 100)
        power_expand_board.set_power("DC1", -100)
        time.sleep(2)

        # Suppose the bot moves forward with a timed sequence
        AutoAssets.MoveForward(10, 10, 10, 10)
        dual_rgb_sensor_1.set_led_color("green")
        time.sleep(1)
        AutoAssets.StopMoving()

        # or according to distance between itself and a ball
        # distance = AutoAssets.GetDistance()
        # if distance > 5:
        #    while distance > 1:
        #        AutoAssets.MoveForward()
        #        distance = AutoAssets.GetDistance()

        power_expand_board.stop("DC2")
        power_expand_board.stop("DC1")
        dual_rgb_sensor_1.set_led_color("red")

        # Rotate bot 90 (suppose the moves 45'/sec)
        dual_rgb_sensor_1.set_led_color("green")
        AutoAssets.RotateLeft()
        time.sleep(1)
        AutoAssets.StopMoving()
        dual_rgb_sensor_1.set_led_color("red")

        # The actual shooting mode. once the ball is loaded into the compartment
        orientation = 0
        while orientation < 45:

            dual_rgb_sensor_1.set_led_color("green")
            AutoAssets.RotateRight()
            time.sleep(0.5)
            AutoAssets.StopMoving()

            dual_rgb_sensor_1.set_led_color("red")
            time.sleep(0.5)
            dual_rgb_sensor_1.set_led_color("green")
            AutoAssets.shoot()
            time.sleep(0.5)

            power_expand_board.stop("DC3")
            dual_rgb_sensor_1.set_led_color("red")

            orientation = orientation + 10

        pass

    def EmbraceBallRoutine():

        original_angle = AutoAssets.getSelfAngle()
        relative_angle = AutoAssets.getSelfAngle()

        relative_distance = distance_sensor_1.get_distance()

        while relative_distance > 10:
            AutoAssets.MoveForward()
            # Constantly updating relative distance
            relative_distance = distance_sensor_1.get_distance()

        pass

    def GrabCubeRoutine():
        # Constantly avoiding the ball location
        # If found the ball. Rotate 90 <- find radiant/sec the bot gives
        # <- If rotated for 1 sec

        original_angle = AutoAssets.getSelfAngle()
        relative_angle = AutoAssets.getSelfAngle()

        relative_distance = distance_sensor_1.get_distance()

        while relative_distance > 10:
            AutoAssets.MoveForward()
            # Constantly updating relative distance
            relative_distance = distance_sensor_1.get_distance()

        # Pretend its 45'/sec
        # 30cm/sec
        AutoAssets.RotateRight()
        time.sleep(2)
        AutoAssets.MoveForward()
        time.sleep(1)
        AutoAssets.RotateLeft()
        time.sleep(1)
        AutoAssets.MoveForward()
        time.sleep(2)

        # Pretend the servo arm is at its upmost angle. And it's at 0'
        smartservo_arm.move(-90)
        time.sleep(1)
        cube_distance = distance_sensor_arm.get_distance()

        while cube_distance > 10:
            pass
        # Finish the code later, ran out of ideas

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
    time.sleep(1)
    AutoAssets.MoveBackward()
    time.sleep(1)
    AutoAssets.RotateRight()
    time.sleep(1)
    AutoAssets.RotateLeft()
    time.sleep(1)
    AutoAssets.StopMoving()

    dual_rgb_sensor_1.set_led_color("green")
    dual_rgb_sensor_2.set_led_color("green")
    time.sleep(5)
    #AutoAssets.ShootRoutine()
    pass


auto_stage = 1
while True:
    time.sleep(0.001)
    if auto_stage == 1:
        AutoStart()
        auto_stage = 0
    else:
        dual_rgb_sensor_1.set_led_color("blue")
        dual_rgb_sensor_2.set_led_color("blue")
        pass
        pass
