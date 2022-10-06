# codes make you happy
import novapi
from mbuild import gamepad
from mbuild.smartservo import smartservo_class
from mbuild.encoder_motor import encoder_motor_class

# new class
smartservo_1 = smartservo_class("M1", "INDEX1")
smartservo_2 = smartservo_class("M2", "INDEX1")
# smartservo_3 is servo arm
smartservo_3 = smartservo_class("M3", "INDEX1")

encoder_motor_M1 = encoder_motor_class("M1", "INDEX1")
encoder_motor_M2 = encoder_motor_class("M2", "INDEX1")
encoder_motor_M3 = encoder_motor_class("M3", "INDEX1")
encoder_motor_M4 = encoder_motor_class("M4", "INDEX1")
shootstat = False
servo_l = 110
servo_r = 60
servo_a = 90  # Suppose the arm servo is facing down

# motors config
# M1, M3 = MOTOR FACING FORWARD ( FRONT , BACK ) , M2, M4 = MOTOR FACING SIDEWAYS ( LEFT , RIGHT )


def LoadMe():
    pass


def Moving():
    # Code for bot rotation. Suppose Rx is turning your joystick left to right
    # Swap Rx with Ry on ServoArm(a) if controls inverted
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


def ServoHand(l, r):
    smartservo_1.move_to(l, 0)
    smartservo_2.move_to(r, 0)


def ServoArm(a):
    smartservo_3.move_to(a, 0)


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
    ServoHand(servo_l, servo_r)
    ServoArm(servo_a)
    # Servo arm
    # Fix this if Ry goes from left to right
    servo_a = servo_a + (0.05 * gamepad.get_joystick("Ry"))
    # Ball bldc
    if shootstat is True:
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
        servo_l = 110
        servo_r = 60
        smartservo_1.move_to(servo_l, 0)
        smartservo_2.move_to(servo_r, 0)
        while not not gamepad.is_key_pressed("L1"):
            # Move this underneath while() if it doesnt work
            servo_l = 60
            servo_r = 110
            smartservo_1.move_to(servo_l, 0)
            smartservo_2.move_to(servo_r, 0)
            pass

    # N1 N3 controls arm servo angles (Reconfig this once we have gamepad on hand)
    elif gamepad.is_key_pressed("N1"):
        servo_l = servo_l + 2
        servo_r = servo_r - 2
    elif gamepad.is_key_pressed("N3"):
        servo_l = servo_l - 2
        servo_r = servo_r + 2

    # Suppose R1 controls the shooting cylinder
    elif gamepad.is_key_pressed("R1"):
        if shootstat is False:
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
