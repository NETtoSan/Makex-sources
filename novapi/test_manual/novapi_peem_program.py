from mbuild.encoder_motor import encoder_motor_class
from mbuild.smartservo import smartservo_class
from mbuild.dual_rgb_sensor import dual_rgb_sensor_class
from mbuild import power_expand_board
from mbuild import gamepad
import novapi
import time

# initialize the variables
auto_stage = 0
shoot = 0
invert = 0
feeddc = 1
lrmode = 0  # Differentiate between shoot and arm control mode
bp = 50

# DC motors
dc1_variable = "DC1"
dc2_variable = "DC2"
dc3_variable = "DC3"
dc4_variable = "DC4"
dc5_variable = "DC5"

# Arm
smartservo_arm = smartservo_class("M6", "INDEX1")

# Hand
smartservo_hand_left = smartservo_class("M6", "INDEX2")
smartservo_hand_left = smartservo_class("M6", "INDEX3")

# Bot motors
encoder_motor_M1 = encoder_motor_class("M1", "INDEX1")
encoder_motor_M2 = encoder_motor_class("M2", "INDEX1")
encoder_motor_M3 = encoder_motor_class("M3", "INDEX1")
encoder_motor_M4 = encoder_motor_class("M4", "INDEX1")


def AutoStart():
    global auto_stage
    pass


def Manual():
    global auto_stage
    global invert
    global lrmode
    global feeddc
    global bp
    LoadMe()
    while True:
        time.sleep(0.001)
        JoyRes.MovingJoystick(invert)
        JoyRes.ArmControl()


def LoadMe():
    global auto_stage

    smartservo_arm.set_power(50)
    smartservo_arm.move(30, 10)

    if gamepad.is_key_pressed("up"):
        ManualRes.MoveForward()
    if gamepad.is_key_pressed("down"):
        ManualRes.MoveBackward()
    if gamepad.is_key_pressed("left"):
        ManualRes.MoveLeft()
    if gamepad.is_key_pressed("right"):
        ManualRes.MoveRight()


class JoyRes:
    def __init__(self):
        pass

    def MovingJoystick(invert):
        global auto_stage

        # Code for bot movement from left to right.
        # If the bot starts slipping to unwanted direction. Tune variables here
        Lx = gamepad.get_joystick("Lx")  # literally Lx variable
        Fl = 0   # Front left
        Fr = 0   # Front right
        Rl = 0   # Rear left
        Rr = 0   # Rear right

        # Adjust LR slide tuning here
        if gamepad.get_joystick("Lx") != 0:

            # if gamepad.get_joystick("Lx") < 0:
            #    Rl = Lx
            #    Rr = Lx

            # if gamepad.get_joystick("Lx") > 10:
            #    Rl = Lx + Lx
            #    Rr = Lx - Lx
            Fl = Lx + 20
            Fr = Lx + 20
            # Bring this back in case things wont go well
            # Fr = Lx + Fr
        # Fl = Lx
        # Fr = Lx
        Rl = Lx
        Rr = Lx
        # Encoder values. If the encoder motors config are changed even the
        # slightest. change this one first then the inverted controls

        vl = 0.8

        EFl = vl * (gamepad.get_joystick("Ly") - Rl
                    - gamepad.get_joystick("Rx"))
        EFr = -vl * (gamepad.get_joystick("Ly") + Rr
                     + gamepad.get_joystick("Rx"))
        ERl = vl * (gamepad.get_joystick("Ly")
                    + Fl - gamepad.get_joystick("Rx"))
        ERr = -vl * (gamepad.get_joystick("Ly") - Fr
                     + gamepad.get_joystick("Rx"))

        if invert == 1:
            # If the controls are inverted The arms are now the bot's front
            EFr = vl * (gamepad.get_joystick("Ly")
                        - Fl - gamepad.get_joystick("Rx"))
            EFl = -vl * (gamepad.get_joystick("Ly") + Fr
                         + gamepad.get_joystick("Rx"))
            ERr = vl * (gamepad.get_joystick("Ly") + Rl
                        - gamepad.get_joystick("Rx"))
            ERl = -vl * (gamepad.get_joystick("Ly") - Rr
                         + gamepad.get_joystick("Rx"))
        encoder_motor_M1.set_power(EFl)
        encoder_motor_M2.set_power(EFr)
        encoder_motor_M3.set_power(ERl)
        encoder_motor_M4.set_power(ERr)
    
    def ArmControl():
        smartservo_arm.move(gamepad.get_joystick("Ry") / 2, 20)
        if gamepad.is_key_pressed("L1"):
            smartservo_hand_left.move(2,10)
            smartservo_hand_right.move(2,10)
        else:
            smartservo_hand_left.move(-2,10)
            smartservo_hand_right.move(-2,10)          

class ManualRes:
    def __init__(self):
        pass

    # Movement
    def MoveBackward():
        global auto_stage
        encoder_motor_M1.set_power(-50)
        encoder_motor_M2.set_power(50)
        encoder_motor_M3.set_power(-50)
        encoder_motor_M4.set_power(50)

    def MoveForward():
        global auto_stage
        encoder_motor_M1.set_power(50)
        encoder_motor_M2.set_power(-50)
        encoder_motor_M3.set_power(50)
        encoder_motor_M4.set_power(-50)

    def MoveLeft():
        global auto_stage
        encoder_motor_M1.set_power(-50)
        encoder_motor_M2.set_power(-50)
        encoder_motor_M3.set_power(50)
        encoder_motor_M4.set_power(50)

    def MoveRight():
        global auto_stage
        encoder_motor_M1.set_power(50)
        encoder_motor_M2.set_power(50)
        encoder_motor_M3.set_power(-50)
        encoder_motor_M4.set_power(-50)

    def StopMoving():
        global auto_stage
        encoder_motor_M1.set_power(0)
        encoder_motor_M2.set_power(0)
        encoder_motor_M3.set_power(0)
        encoder_motor_M4.set_power(0)


auto_stage = 1
while True:
    time.sleep(0.001)
    if auto_stage == 1:
        AutoStart()
        auto_stage = 0

    else:
        smartservo_arm.move_to(0, 10)
        Manual()