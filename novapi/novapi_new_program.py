# codes make you happy
import novapi
from mbuild import gamepad
from mbuild import power_expand_board
from mbuild.smartservo import smartservo_class
from mbuild.encoder_motor import encoder_motor_class

# initialize variables
auto_stage = 0
shoot = 0
# new class
smartservo_1 = smartservo_class("M1", "INDEX1")
smartservo_2 = smartservo_class("M2", "INDEX1")
encoder_motor_M1 = encoder_motor_class("M1", "INDEX1")
encoder_motor_M2 = encoder_motor_class("M2", "INDEX1")
encoder_motor_M3 = encoder_motor_class("M3", "INDEX1")
encoder_motor_M4 = encoder_motor_class("M4", "INDEX1")


def AutoStart():
    global auto_stage
    pass


def Manual():
    global auto_stage
    LoadMe()
    while True:
        time.sleep(0.001)
        MovingJoystick()
        if gamepad.is_key_pressed("Up"):
            MoveForward()


        if gamepad.is_key_pressed("Down"):
            MoveBackward()


        if gamepad.is_key_pressed("Left"):
            MoveLeft()

        if gamepad.is_key_pressed("Right"):
            MoveRight()

        if gamepad.is_key_pressed("N1"):
            power_expand_board.set_power("DC1", 80)
        elif gamepad.is_key_pressed("N4"):
            power_expand_board.set_power("DC1", -80)
        else:
            power_expand_board.stop("DC1")


        if gamepad.is_key_pressed("N2"):
            pass

        if gamepad.is_key_pressed("N3"):
            pass


        if gamepad.is_key_pressed("R1"):
            power_expand_board.set_power("BL1", 15)
            power_expand_board.set_power("BL2", 15)

        else:
            power_expand_board.stop("BL1")
            power_expand_board.stop("BL2")

def LoadMe():
    global auto_stage

    smartservo_1.move(90, 10)
    smartservo_1.move_to(90, 10)
    smartservo_1.set_power(50)
    power_expand_board.set_power("BL1", 50)
    power_expand_board.set_power("DC1", 50)
    power_expand_board.stop("BL1")
    power_expand_board.stop("DC1")


def MovingJoystick():
    global auto_stage

    # Code for bot rotation. Suppose Rx is turning your joystick left to right
    # Swap Rx with Ry on ServoArm(a) if controls inverted

    encoder_motor_M1.set_power(0.8 * (gamepad.get_joystick("Ly") - gamepad.get_joystick("Lx")
                          - gamepad.get_joystick("Rx")))
    encoder_motor_M2.set_power(-0.8 * (gamepad.get_joystick("Ly") + gamepad.get_joystick("Lx")
                           + gamepad.get_joystick("Rx")))
    encoder_motor_M3.set_power(0.8 * (gamepad.get_joystick("Ly") + gamepad.get_joystick("Lx")
                          - gamepad.get_joystick("Rx")))
    encoder_motor_M4.set_power(-0.8 * (gamepad.get_joystick("Ly") - gamepad.get_joystick("Lx")
                           + gamepad.get_joystick("Rx")))


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
        Manual()
