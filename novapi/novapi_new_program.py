# codes make you happy
import novapi
from mbuild import gamepad
from mbuild import power_expand_board
from mbuild.dual_rgb_sensor import dual_rgb_sensor_class
from mbuild.smartservo import smartservo_class
from mbuild.encoder_motor import encoder_motor_class

# initialize variables
auto_stage = 0
shoot = 0
invert = 0
# new class
dual_rgb_sensor_1 = dual_rgb_sensor_class("PORT2", "INDEX1")
smartservo_arm = smartservo_class("M5", "INDEX2")
smartservo_updown = smartservo_class("M5", "INDEX1")
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
    LoadMe()
    while True:
        time.sleep(0.001)
        JoyRes.MovingJoystick()
        JoyRes.FeedControl()
        JoyRes.ArmControl()
        ManualRes.InvertLED(invert)
        if gamepad.is_key_pressed("Up"):
            ManualRes.MoveForward()

        if gamepad.is_key_pressed("Down"):
            ManualRes.MoveBackward()

        if gamepad.is_key_pressed("Left"):
            ManualRes.MoveLeft()

        if gamepad.is_key_pressed("Right"):
            ManualRes.MoveRight()

        if gamepad.is_key_pressed("N1"):
            smartservo_arm.move(10, 10)

        if gamepad.is_key_pressed("N2"):
            pass

        if gamepad.is_key_pressed("N3"):
            pass

        if gamepad.is_key_pressed("N4"):
            smartservo_arm.move(-10, 10)

        if gamepad.is_key_pressed("R2"):
            if invert == 0:
                invert = 1
            else:
                invert = 0
            while not not gamepad.is_key_pressed("R2"):
                pass

        if gamepad.is_key_pressed("R1"):
            power_expand_board.stop("BL1")
            power_expand_board.stop("BL2")

        else:
            power_expand_board.set_power("BL1", 15)
            power_expand_board.set_power("BL2", 15)

        power_expand_board.set_power("DC2", 100)


def LoadMe():
    global auto_stage

    smartservo_arm.set_power(50)
    smartservo_arm.move_to(90, 10)
    power_expand_board.set_power("BL1", 50)
    power_expand_board.set_power("DC1", 50)
    power_expand_board.stop("BL1")
    power_expand_board.stop("DC1")


class JoyRes:
    def __init__(self):
        pass

    def ArmControl():
        global auto_stage
        smartservo_updown.move(gamepad.get_joystick("Ry"), 10)

    def MovingJoystick():
        global auto_stage

        # Code for bot rotation. Suppose Rx is turning your joystick left to right
        # Swap Rx with Ry on ServoArm(a) if controls inverted
        Lx = gamepad.get_joystick("Lx")
        Fl = 0
        Fr = 0
        Rl = 0
        Rr = 0

        # Adjust LR slide tuning here
        if gamepad.get_joystick("Lx") != 0:

            if gamepad.get_joystick("Lx") < 0:
                Fl = Lx + 10
            if gamepad.get_joystick("Lx") > 10:
                Fl = Lx - 10

            Fr = Lx
            Rl = Lx
            Rr = Lx
        # Encoder values
        EFl = 0.7 * (gamepad.get_joystick("Ly")
                     - Fl - gamepad.get_joystick("Rx"))
        EFr = -0.7 * (gamepad.get_joystick("Ly") + Fr
                      + gamepad.get_joystick("Rx"))
        ERl = 0.7 * (gamepad.get_joystick("Ly") + Rl
                     - gamepad.get_joystick("Rx"))
        ERr = -0.7 * (gamepad.get_joystick("Ly") - Rr
                      + gamepad.get_joystick("Rx"))
                      
        encoder_motor_M1.set_power(EFl)
        encoder_motor_M2.set_power(EFr)
        encoder_motor_M3.set_power(ERl)
        encoder_motor_M4.set_power(ERr)

    def FeedControl():
        if gamepad.is_key_pressed("L1"):
            power_expand_board.set_power("DC1", -100)
        elif gamepad.is_key_pressed("L2"):
            power_expand_board.set_power("DC1", 100)
        else:
            power_expand_board.stop("DC1")


class ManualRes:
    def __init__(self):
        pass
    # Miscellaneous

    def InvertLED(i):
        if i != 0:
            dual_rgb_sensor_1.set_led_color("red")
        else:
            dual_rgb_sensor_1.set_led_color("green")
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
