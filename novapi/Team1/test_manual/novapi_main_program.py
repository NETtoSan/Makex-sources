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
vl = 0.5

# DC motors
dc_gun = "DC1"
dc_front = "DC2"
dc3_variable = "DC3"
dc_hand = "DC4"
dc5_variable = "DC5"

# Sensors
dual_rgb_sensor_1 = dual_rgb_sensor_class("PORT2", "INDEX1")
dual_rgb_sensor_2 = dual_rgb_sensor_class("PORT2", "INDEX2")

# Bot motors
encode_fl = encoder_motor_class("M1", "INDEX1")
encode_fr = encoder_motor_class("M2", "INDEX1")
encode_rl = encoder_motor_class("M3", "INDEX1")
encode_rr = encoder_motor_class("M4", "INDEX1")
encode_feed = encoder_motor_class("M5", "INDEX1")


def AutoStart():
    global auto_stage
    pass


def Manual():
    global auto_stage
    global invert
    global lrmode
    global feeddc
    global bp
    global vl
    LoadMe()
    while True:
        time.sleep(0.001)
        JoyRes.MovingJoystick()
        ManualRes.InvertLED(invert)
        ManualRes.ControlLED(lrmode)
        JoyRes.MultiControl(lrmode, bp)

        if gamepad.is_key_pressed("Up"):
            ManualRes.MoveForward()

        if gamepad.is_key_pressed("Down"):
            ManualRes.MoveBackward()

        if gamepad.is_key_pressed("Left"):
            ManualRes.MoveLeft()

        if gamepad.is_key_pressed("Right"):
            ManualRes.MoveRight()

        if gamepad.is_key_pressed("N1"):
            power_expand_board.set_power("DC5", -20)
        elif gamepad.is_key_pressed("N4"):
            power_expand_board.set_power("DC5", 20)
        else:
            power_expand_board.stop("DC5")

        if gamepad.is_key_pressed("N2"):
            if bp == 50:
                bp = 100
            elif bp == 100:
                bp = 0
            else:
                bp = 50
            while not not gamepad.is_key_pressed("N2"):
                pass
            pass

        if gamepad.is_key_pressed("N3"):
            if feeddc == 0:
                feeddc = 1
            else:
                feeddc = 0
            while not not gamepad.is_key_pressed("N3"):
                pass
            pass

        # Switch shooting to arm control
        if gamepad.is_key_pressed("R2"):
            if lrmode == 0:
                lrmode = 1
            else:
                lrmode = 0
            while not not gamepad.is_key_pressed("R2"):
                pass
        # Control speed

        if gamepad.is_key_pressed("L_Thumb"):
            if vl == 0.5:
                vl = 0.8
            elif vl == 0.8:
                vl = 1
            else:
                vl = 0.5

            while not not gamepad.is_key_pressed("L_Thumb"):
                pass
        # Invert control direction
        if gamepad.is_key_pressed("R_Thumb"):
            if invert == 0:
                invert = 1
            else:
                invert = 0
            while not not gamepad.is_key_pressed("R_Thumb"):
                pass

        # Dc feed
        if feeddc == 1:
            power_expand_board.set_power(dc_front, -100)
        else:
            power_expand_board.stop(dc_front)


def LoadMe():
    global auto_stage


class JoyRes:
    def __init__(self):
        pass

    def MovingJoystick():
        global vl, invert
        # Code for bot movement from left to right.
        # If the bot starts slipping to unwanted direction. Tune variables here
        
        Lx = gamepad.get_joystick("Lx")  # literally Lx variable

        Fl = Lx
        Fr = Lx 
        Rl = Lx 
        Rr = Lx

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
        encode_fl.set_power(EFl)
        encode_fr.set_power(EFr)
        encode_rl.set_power(ERl)
        encode_rr.set_power(ERr)

    def TurretControl():
        global dc_gun
        power_expand_board.set_power(dc_gun, gamepad.get_joystick("Ry") / 2)

    def FeedControl():
        if gamepad.is_key_pressed("L1"):
            encode_feed.set_power(-100)
        elif gamepad.is_key_pressed("L2"):
            encode_feed.set_power(100)
        else:
            encode_feed.set_power(0)

    def ShootControl():
        global dc3_variable
        if gamepad.is_key_pressed("R1"):
            power_expand_board.set_power(dc3_variable, -100)
        else:
            power_expand_board.stop(dc3_variable)

    def GrabControl():
        global dc_hand
        if gamepad.is_key_pressed("L1"):
            power_expand_board.set_power(dc_hand, 50)

        elif gamepad.is_key_pressed("R1"):
            power_expand_board.set_power(dc_hand, -50)
        else:
            power_expand_board.stop(dc_hand)
        pass

    def HandControl():
        power_expand_board.set_power("DC6", gamepad.get_joystick("Ry"))
        power_expand_board.set_power("DC7", gamepad.get_joystick("Ry"))
        # smartservo_arm.move(gamepad.get_joystick("Ry"), 10)
        pass

    def MultiControl(lc, bp):
        if lc == 0:
            # Gun control mode
            JoyRes.TurretControl()
            JoyRes.ShootControl()
            JoyRes.FeedControl()

            # < 15 -- 23 > : 25 max
            power_expand_board.set_power("BL1", bp)
            power_expand_board.set_power("BL2", bp)
        else:
            # Hand control mode
            JoyRes.HandControl()
            JoyRes.GrabControl()
            power_expand_board.stop("BL1")
            power_expand_board.stop("BL2")


class ManualRes:
    def __init__(self):
        pass
    # Miscellaneous

    def InvertLED(i):
        if i != 0:
            dual_rgb_sensor_1.set_led_color("red")
        else:
            dual_rgb_sensor_1.set_led_color("green")

    def ControlLED(k):
        if k != 0:
            dual_rgb_sensor_2.set_led_color("red")
        else:
            dual_rgb_sensor_2.set_led_color("green")
    # Joystick Controls

    def MoveBackward():
        global auto_stage
        encode_fl.set_power(-50)
        encode_fr.set_power(50)
        encode_rl.set_power(-50)
        encode_rr.set_power(50)

    def MoveForward():
        global auto_stage
        encode_fl.set_power(50)
        encode_fr.set_power(-50)
        encode_rl.set_power(50)
        encode_rr.set_power(-50)

    def MoveRight():
        global auto_stage
        encode_fl.set_power(50)
        encode_fr.set_power(50)
        encode_rl.set_power(-50)
        encode_rr.set_power(-50)

    def MoveLeft():
        global auto_stage
        encode_fl.set_power(-50)
        encode_fr.set_power(-50)
        encode_rl.set_power(50)
        encode_rr.set_power(50)

    def StopMoving():
        global auto_stage
        encode_fl.set_power(0)
        encode_fr.set_power(0)
        encode_rl.set_power(0)
        encode_rr.set_power(0)


auto_stage = 1
while True:
    time.sleep(0.001)
    if auto_stage == 1:
        AutoStart()
        auto_stage = 0

    else:
        smartservo_arm.move_to(0, 10)
        Manual()