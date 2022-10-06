# codes make you happy
import novapi
from mbuild import gamepad
from mbuild import power_expand_board
from mbuild.smartservo import smartservo_class
from mbuild.encoder_motor import encoder_motor_class

# initialize variables
auto_stage = 0

# new class
smartservo_1 = smartservo_class("M1", "INDEX1")
smartservo_2 = smartservo_class("M2", "INDEX1")
encoder_motor_M1 = encoder_motor_class("M1", "INDEX1")
encoder_motor_M2 = encoder_motor_class("M2", "INDEX1")
encoder_motor_M3 = encoder_motor_class("M3", "INDEX1")
encoder_motor_M4 = encoder_motor_class("M4", "INDEX1")

def AutoStart ():
    global auto_stage
    pass
def Manual ():
    global auto_stage
    LoadMe()
    while True:
        time.sleep(0.001)
        MovingJoystick()
        if gamepad.is_key_pressed("Up"):
            MoveForward()
            while not not gamepad.is_key_pressed("Up"):
                pass

        if gamepad.is_key_pressed("Down"):
            MoveBackward()
            while not not gamepad.is_key_pressed("Down"):
                pass

        if gamepad.is_key_pressed("Left"):
            MoveLeft()
            while not not gamepad.is_key_pressed("Left"):
                pass

        if gamepad.is_key_pressed("Right"):
            MoveRight()
            while not not gamepad.is_key_pressed("Right"):
                pass

        if gamepad.is_key_pressed("N1"):
            power_expand_board.set_power("DC1", 50)
            while not not gamepad.is_key_pressed("N1"):
                pass

            power_expand_board.stop("DC1")

        if gamepad.is_key_pressed("N2"):
            while not not gamepad.is_key_pressed("N2"):
                pass

        if gamepad.is_key_pressed("N3"):
            while not not gamepad.is_key_pressed("N3"):
                pass

        if gamepad.is_key_pressed("N4"):
            power_expand_board.set_power("DC1", -50)
            while not not gamepad.is_key_pressed("N4"):
                pass

            power_expand_board.stop("DC1")

def LoadMe ():
    global auto_stage

    smartservo_1.move(90, 10)
    smartservo_1.move_to(90, 10)
    smartservo_1.set_power(50)
    power_expand_board.set_power("BL1", 50)
    power_expand_board.set_power("DC1", 50)
    power_expand_board.stop("BL1")
    power_expand_board.stop("DC1")

def MovingJoystick ():
    global auto_stage
    if not gamepad.get_joystick("Lx") == 0:
        pass

    encoder_motor_M1.set_power(0.5 * ((gamepad.get_joystick("Ly") + ((0 - gamepad.get_joystick("Rx"))))))
    encoder_motor_M2.set_power(-0.5 * ((gamepad.get_joystick("Ly") - ((0 - gamepad.get_joystick("Rx"))))))
    encoder_motor_M3.set_power(0.5 * ((gamepad.get_joystick("Ly") + ((0 - gamepad.get_joystick("Rx"))))))
    encoder_motor_M4.set_power(-0.5 * ((gamepad.get_joystick("Ly") - ((0 - gamepad.get_joystick("Rx"))))))

def MoveBackward ():
    global auto_stage
    encoder_motor_M1.set_power(-50)
    encoder_motor_M2.set_power(50)
    encoder_motor_M3.set_power(-50)
    encoder_motor_M4.set_power(50)

def MoveForward ():
    global auto_stage
    encoder_motor_M1.set_power(50)
    encoder_motor_M2.set_power(-50)
    encoder_motor_M3.set_power(50)
    encoder_motor_M4.set_power(-50)

def MoveRight ():
    global auto_stage
    encoder_motor_M1.set_power(50)
    encoder_motor_M2.set_power(50)
    encoder_motor_M3.set_power(-50)
    encoder_motor_M4.set_power(-50)

def MoveLeft ():
    global auto_stage
    encoder_motor_M1.set_power(-50)
    encoder_motor_M2.set_power(-50)
    encoder_motor_M3.set_power(50)
    encoder_motor_M4.set_power(50)

def StopMoving ():
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
