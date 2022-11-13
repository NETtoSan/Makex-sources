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
dc1_variable = "DC1"
dc2_variable = "DC2"
dc3_variable = "DC3"
dc4_variable = "DC4"
dc5_variable = "DC5"

# Sensors
dual_rgb_sensor_1 = dual_rgb_sensor_class("PORT2", "INDEX1")
dual_rgb_sensor_2 = dual_rgb_sensor_class("PORT2", "INDEX2")

# Arm
smartservo_arm = smartservo_class("M6", "INDEX1")

# Turret
smartservo_updown = smartservo_class("M5", "INDEX1")

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
        ManualRes.InvertLED(invert)
        ManualRes.ControlLED(lrmode)
        JoyRes.ButtonControl()
        JoyRes.MultiControl(lrmode, bp)
        
        # Dc feed
        if feeddc == 1:
            power_expand_board.set_power(dc2_variable, -100)
        else:
            power_expand_board.stop(dc2_variable)


def LoadMe():
    global auto_stage

    smartservo_arm.set_power(50)
    smartservo_arm.move(30, 10)
    # power_expand_board.set_power("BL1", 50)
    # power_expand_board.set_power(dc1_variable, 50)
    # power_expand_board.stop("BL1")
    # power_expand_board.stop(dc1_variable)


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
        #if gamepad.get_joystick("Lx") != 0:

        #    if gamepad.get_joystick("Lx") < 0:
        #        Fl = Lx - 20
        #        Fr = Lx - 20

        #    if gamepad.get_joystick("Lx") > 10:
        #        Fl = Lx + 20
        #        Fr = Lx + 20

            # Bring this back in case things wont go well
            # Fr = Lx + Fr
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
        encoder_motor_M1.set_power(EFl)
        encoder_motor_M2.set_power(EFr)
        encoder_motor_M3.set_power(ERl)
        encoder_motor_M4.set_power(ERr)

    def TurretControl():
        global auto_stage
        # > 40 < 60
        # if smartservo_updown.get_value("angle") > -43:
        #    smartservo_updown.move(-1, 10)

        # if smartservo_updown.get_value("angle") < -60:
        #    smartservo_updown.move(1, 10)
        # else:
        if smartservo_updown.get_value("angle") < -56:
            servo_value = smartservo_updown.get_value("angle")
            while servo_value < -55:
                smartservo_updown.move(3, 10)
                servo_value = smartservo_updown.get_value("angle")

        relative_angle = gamepad.get_joystick("Ry") / 3

        smartservo_updown.move(relative_angle, 10)

    def FeedControl():
        if gamepad.is_key_pressed("L1"):
            power_expand_board.set_power(dc1_variable, -100)
        elif gamepad.is_key_pressed("L2"):
            power_expand_board.set_power(dc1_variable, 100)
        else:
            power_expand_board.stop("DC1")

    def ShootControl():
        if gamepad.is_key_pressed("R1"):
            power_expand_board.set_power(dc3_variable, -100)
        else:
            power_expand_board.stop(dc3_variable)

    def GrabControl():
        # DC4 L1 release R1 grab
        if gamepad.is_key_pressed("L1"):
            power_expand_board.set_power("DC4", 50)

        elif gamepad.is_key_pressed("R1"):
            power_expand_board.set_power("DC4", -50)
        else:
            power_expand_board.stop("DC4")
        pass

    def HandControl():
        power_expand_board.set_power("DC6", gamepad.get_joystick("Ry"))
        power_expand_board.set_power("DC7", gamepad.get_joystick("Ry"))
        # smartservo_arm.move(gamepad.get_joystick("Ry"), 10)
        pass

    def ButtonControl():
        
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

    def MoveRight():
        global auto_stage
        encoder_motor_M1.set_power(50)
        encoder_motor_M2.set_power(50)
        encoder_motor_M3.set_power(-50)
        encoder_motor_M4.set_power(-50)

    def MoveLeft():
        global auto_stage
        encoder_motor_M1.set_power(-50)
        encoder_motor_M2.set_power(-50)
        encoder_motor_M3.set_power(50)
        encoder_motor_M4.set_power(50)

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
