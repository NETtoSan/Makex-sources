# codes make you happy
import novapi
from mbuild import gamepad
from mbuild.smartservo import smartservo_class
from mbuild.encoder_motor import encoder_motor_class

# new class
smartservo_1 = smartservo_class("M1", "INDEX1")
smartservo_2 = smartservo_class("M2", "INDEX1")
encoder_motor_M1 = encoder_motor_class("M1", "INDEX1")
encoder_motor_M2 = encoder_motor_class("M2", "INDEX1")
encoder_motor_M3 = encoder_motor_class("M3", "INDEX1")
encoder_motor_M4 = encoder_motor_class("M4", "INDEX1")
shootstat = False

# motors config
# M1, M3 = MOTOR FACING FORWARD ( FRONT , BACK ) , M2, M4 = MOTOR FACING SIDEWAYS ( LEFT , RIGHT ) 


def LoadMe():
    pass


def Moving():
    # Code for bot rotation. Suppose Rx is turning your joystick left to right

    motor_front_1 = 0.8 * (gamepad.get_joystick("Lx")
                           + gamepad.get_joystick("Rx"))
    motor_front_2 = -0.8 * (gamepad.get_joystick("Ly")
                            - gamepad.get_joystick("Rx"))
    motor_sides_1 = 0.8 * (gamepad.get_joystick("Lx")
                           + gamepad.get_joystick("Rx"))
    motor_sides_2 = -0.8 * (gamepad.get_joystick("Ly")
                            - gamepad.get_joystick("Rx"))

    encoder_motor_M1.set_power(motor_front_1)
    encoder_motor_M2.set_power(motor_sides_1)
    encoder_motor_M3.set_power(motor_front_2)
    encoder_motor_M4.set_power(motor_sides_2)

    #encoder_motor_M1.set_power(
    #    0.8 * ((gamepad.get_joystick("Ly") + gamepad.get_joystick("Lx"))))
    #encoder_motor_M2.set_power(-0.8
    #                           * ((gamepad.get_joystick("Ly") - gamepad.get_joystick("Lx"))))
    #encoder_motor_M3.set_power(
    #    0.8 * ((gamepad.get_joystick("Ly") + gamepad.get_joystick("Lx"))))
    #encoder_motor_M4.set_power(-0.8
    #                           * ((gamepad.get_joystick("Ly") - gamepad.get_joystick("Lx"))))


def MoveForward():
    encoder_motor_M1.set_power(50)
    encoder_motor_M2.set_power(0)
    encoder_motor_M3.set_power(-50)
    encoder_motor_M4.set_power(0)


def MoveBackward():
    encoder_motor_M1.set_power(-50)
    encoder_motor_M2.set_power(0)
    encoder_motor_M3.set_power(50)
    encoder_motor_M4.set_power(0)


def MoveRight():
    encoder_motor_M1.set_power(0)
    encoder_motor_M2.set_power(50)
    encoder_motor_M3.set_power(0)
    encoder_motor_M4.set_power(-50)


def MoveLeft():
    encoder_motor_M1.set_power(0)
    encoder_motor_M2.set_power(-50)
    encoder_motor_M3.set_power(0)
    encoder_motor_M4.set_power(50)


def StopMoving():
    encoder_motor_M1.set_power(0)
    encoder_motor_M2.set_power(0)
    encoder_motor_M3.set_power(0)
    encoder_motor_M4.set_power(0)


LoadMe()
while True:
    time.sleep(0.001)
    Moving()

    # Ball bldc
    if shootstat == True:
        power_expand_board.set_power("BL1", 10)
        power_expand_board.set_power("Bl2", 10)
    else:
        power_expand_board.stop("BL1")
        power_expand_board.stop("BL2")

    if gamepad.is_key_pressed("Up"):
        MoveForward()
        while not not gamepad.is_key_pressed("Up"):
            pass
    elif gamepad.is_key_pressed("Down"):
        MoveBackward()
        while not not gamepad.is_key_pressed("Down"):
            pass

    elif gamepad.is_key_pressed("Right"):
        MoveRight()
        while not not gamepad.is_key_pressed("Right"):
            pass

    elif gamepad.is_key_pressed("Left"):
        MoveLeft()
        while not not gamepad.is_key_pressed("Left"):
            pass

    # Suppose L1 controls the arm servo
    elif gamepad.is_key_pressed("L1"):
        smartservo_1.move_to(110, 0)
        smartservo_2.move_to(60, 0)
        while not not gamepad.is_key_pressed("L1"):
            # Move this underneath while() if it doesnt work
            smartservo_1.move_to(110, 0)
            smartservo_2.move_to(60, 0)
            pass
        
    # Suppose R1 controls the shooting cylinder
    elif gamepad.is_key_pressed("R1"):
        if shootstat == False:
            shootstat = True
        else:
            shootstat = False
        while not not gamepad.is_key_pressed("R1"):
            pass

    # Supose R2 controls the ball loading motor
    elif gamepad.is_key_pressed("R2"):
        power_expand_board.set_power("DC1", 50)
        while not not gamepad.is_key_pressed("R2"):
            # Move this underneath while() if it doesnt work
            power_expand_board.stop("DC1")
            pass
    else:
        StopMoving()
        
        # - Parameters for future coding potentials - 
        #smartservo_1.move(90, 10)
        #smartservo_1.move_to(90, 10)
        #smartservo_1.set_power(50)
        #power_expand_board.set_power("BL1", 50)
        #power_expand_board.set_power("DC1", 50)
        #power_expand_board.stop("BL1")
        #power_expand_board.stop("DC1")
