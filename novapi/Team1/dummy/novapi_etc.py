# codes make you happy
import novapi
from mbuild.led_matrix import led_matrix_class
from mbuild.smartservo import smartservo_class
from mbuild import gamepad
from mbuild import power_expand_board
from mbuild.encoder_motor import encoder_motor_class

# initialize variables
auto_stage = 0
x_pos = 0
y_pos = 0
xy_positive = 0
xy_negative = 0
direction_code = 0
speed = 0
last_direction_code = 0
speed_start = 0
DC1_1 = 0
brushless = 0
encodeMotor = 0
Feed = 0
speed_DC1 = 0
DC2 = 0
speed_DC2 = 0
DC1_2 = 0

# new class
led_matrix_1 = led_matrix_class("PORT1", "INDEX1")
smartservo_1 = smartservo_class("M5", "INDEX1")
smartservo_2 = smartservo_class("M6", "INDEX1")
smartservo_3 = smartservo_class("M5", "INDEX2")
encoder_motor_M1 = encoder_motor_class("M1", "INDEX1")
encoder_motor_M2 = encoder_motor_class("M2", "INDEX1")
encoder_motor_M3 = encoder_motor_class("M3", "INDEX1")
encoder_motor_M4 = encoder_motor_class("M4", "INDEX1")

def Manual ():
    global auto_stage, x_pos, y_pos, xy_positive, xy_negative, direction_code, speed, last_direction_code, speed_start, DC1_1, brushless, encodeMotor, Feed, speed_DC1, DC2, speed_DC2, DC1_2
    xy_positive = 20
    xy_negative = -20
    while not (gamepad.is_key_pressed("≡")):
        time.sleep(0.001)
        MovingJoystick()
        led_matrix_1.show(smartservo_1.get_value("angle"), wait = False)

        # Toggle brushless motors
        if gamepad.is_key_pressed("L1"):
            if brushless == 0:
                brushless = 1

            else:
                brushless = 0

            while not not gamepad.is_key_pressed("L1"):
                pass

        if brushless == 1:
            power_expand_board.set_power("BL1", 60)
            power_expand_board.set_power("BL2", 60)

        else:
            power_expand_board.stop("BL1")
            power_expand_board.stop("BL2")


        if gamepad.is_key_pressed("N1"):
            if DC1_1 == 0:
                DC1_1 = 1

            else:
                DC1_1 = 0

            while not not gamepad.is_key_pressed("N1"):
                pass

        if DC1_1 == 1:
            power_expand_board.set_power("DC1", -50)

        else:
            power_expand_board.stop("DC1")

        if gamepad.is_key_pressed("N2"):
            while not (not gamepad.is_key_pressed("N2")):
                time.sleep(0.001)
                power_expand_board.set_power("DC1", 50)

            power_expand_board.stop("DC1")

        if gamepad.is_key_pressed("R1"):
            if DC2 == 0:
                DC2 = 1

            else:
                DC2 = 0

            while not not gamepad.is_key_pressed("R1"):
                pass

        if DC2 == 1:
            power_expand_board.set_power("DC2", -100)

        else:
            power_expand_board.stop("DC2")

        if gamepad.is_key_pressed("+"):
            while not (not gamepad.is_key_pressed("+")):
                time.sleep(0.001)
                power_expand_board.set_power("DC2", 100)

            power_expand_board.stop("DC2")

        if gamepad.is_key_pressed("Left"):
            smartservo_2.move(10, 60)

        if gamepad.is_key_pressed("Right"):
            smartservo_2.move(-10, 60)

        if gamepad.is_key_pressed("Up"):
            smartservo_1.move(10, 60)

        if gamepad.is_key_pressed("Down"):
            smartservo_1.move(-10, 60)

        if gamepad.is_key_pressed("N3"):
            while not (not gamepad.is_key_pressed("N3")):
                time.sleep(0.001)
                power_expand_board.set_power("DC3", -69)

            power_expand_board.stop("DC3")

        if gamepad.is_key_pressed("N4"):
            while not (not gamepad.is_key_pressed("N4")):
                time.sleep(0.001)
                power_expand_board.set_power("DC3", 69)

            power_expand_board.stop("DC3")

        if gamepad.is_key_pressed("L2"):
            smartservo_3.move(10, 60)

        if gamepad.is_key_pressed("R2"):
            smartservo_3.move(-10, 60)

    while not not gamepad.is_key_pressed("≡"):
        pass

    StopMoving()

def LoadMe ():
    global auto_stage, x_pos, y_pos, xy_positive, xy_negative, direction_code, speed, last_direction_code, speed_start, DC1_1, brushless, encodeMotor, Feed, speed_DC1, DC2, speed_DC2, DC1_2
    DC1_1 = 0
    DC1_2 = 0
    DC2 = 0
    brushless = 0

def MovingJoystick ():
    global auto_stage, x_pos, y_pos, xy_positive, xy_negative, direction_code, speed, last_direction_code, speed_start, DC1_1, brushless, encodeMotor, Feed, speed_DC1, DC2, speed_DC2, DC1_2
    x_pos = gamepad.get_joystick("Lx")
    y_pos = gamepad.get_joystick("Ly")

    if gamepad.get_joystick("Rx") > xy_positive or gamepad.get_joystick("Rx") < xy_negative:
        if gamepad.get_joystick("Rx") < xy_negative:
            direction_code = 'SL'

        else:
            if gamepad.get_joystick("Rx") > xy_positive:
                direction_code = 'SR'

            else:
                direction_code = 'S'

    else:
        if y_pos < xy_negative:
            if x_pos < xy_negative:
                direction_code = 'FL'

            else:
                if x_pos > xy_positive:
                    direction_code = 'FR'

                else:
                    direction_code = 'F'

        else:
            if y_pos > xy_positive:
                if x_pos < xy_negative:
                    direction_code = 'BL'

                else:
                    if x_pos > xy_positive:
                        direction_code = 'BR'

                    else:
                        direction_code = 'B'

            else:
                if x_pos < xy_negative:
                    direction_code = 'L'

                else:
                    if x_pos > xy_positive:
                        direction_code = 'R'

                    else:
                        direction_code = 'S'

    if not direction_code == last_direction_code:
        ControlDirections_S(direction_code)
        last_direction_code = direction_code

def ControlDirections_S (code):
    global auto_stage, x_pos, y_pos, xy_positive, xy_negative, direction_code, speed, last_direction_code, speed_start, DC1_1, brushless, encodeMotor, Feed, speed_DC1, DC2, speed_DC2, DC1_2
    if code == 'F':
        DriveEncoderMotors_N_N_N_N(1, 1, 1, 1)

    if code == 'B':
        DriveEncoderMotors_N_N_N_N(-1, -1, -1, -1)

    if code == 'L':
        DriveEncoderMotors_N_N_N_N(-1, 1, 1, -1)

    if code == 'R':
        DriveEncoderMotors_N_N_N_N(1, -1, -1, 1)

    if code == 'SL':
        DriveEncoderMotors_N_N_N_N(-1, 1, -1, 1)

    if code == 'SR':
        DriveEncoderMotors_N_N_N_N(1, -1, 1, -1)

    if code == 'S':
        StopMoving()

def DriveEncoderMotors_N_N_N_N (EM1, EM2, EM3, EM4):
    global auto_stage, x_pos, y_pos, xy_positive, xy_negative, direction_code, speed, last_direction_code, speed_start, DC1_1, brushless, encodeMotor, Feed, speed_DC1, DC2, speed_DC2, DC1_2
    speed_start = 0
    while not (speed_start == speed):
        time.sleep(0.001)
        speed_start = (speed_start + 5)
        encoder_motor_M1.set_power(-1 * (EM1 * speed_start))
        encoder_motor_M2.set_power(EM2 * speed_start)
        encoder_motor_M3.set_power(-1 * (EM3 * speed_start))
        encoder_motor_M4.set_power(EM4 * speed_start)

def StopMoving ():
    encoder_motor_M1.set_power(0)
    encoder_motor_M2.set_power(0)
    encoder_motor_M3.set_power(0)
    encoder_motor_M4.set_power(0)

def AutoStart ():
    global auto_stage, x_pos, y_pos, xy_positive, xy_negative, direction_code, speed, last_direction_code, speed_start, DC1_1, brushless, encodeMotor, Feed, speed_DC1, DC2, speed_DC2, DC1_2
    smartservo_1.move_to(105, 60)
    DC1()
    feed1()
    for i in range(1):
        move_S_for_N_secs('B', 0.1)
        move_S_for_N_secs('R', 2.1)
        move_S_for_N_secs('B', 1.2)
        move_S_for_N_secs('L', 2)

    feed2()
    time.sleep(0.5)
    feed1()
    for i in range(1):
        move_S_for_N_secs('R', 0.8)
        move_S_for_N_secs('L', 0.5)

    time.sleep(0.5)
    move_S_for_N_secs('SR', 0.25)
    time.sleep(0.2)
    move_S_for_N_secs('SR', 0.2)
    smartservo_1.move_to(110, 10)
    time.sleep(0.5)
    move_S_for_N_secs('SR', 0.1)

def feed2 ():
    global auto_stage, x_pos, y_pos, xy_positive, xy_negative, direction_code, speed, last_direction_code, speed_start, DC1_1, brushless, encodeMotor, Feed, speed_DC1, DC2, speed_DC2, DC1_2
    power_expand_board.set_power("DC2", 100)
    power_expand_board.set_power("DC1", 100)

def feed1 ():
    global auto_stage, x_pos, y_pos, xy_positive, xy_negative, direction_code, speed, last_direction_code, speed_start, DC1_1, brushless, encodeMotor, Feed, speed_DC1, DC2, speed_DC2, DC1_2
    power_expand_board.set_power("DC2", -100)
    power_expand_board.set_power("DC1", -100)

def DC1 ():
    global auto_stage, x_pos, y_pos, xy_positive, xy_negative, direction_code, speed, last_direction_code, speed_start, DC1_1, brushless, encodeMotor, Feed, speed_DC1, DC2, speed_DC2, DC1_2
    power_expand_board.set_power("BL2", 80)
    power_expand_board.set_power("BL1", 80)

def move_S_for_N_secs (directions, timing):
    global auto_stage, x_pos, y_pos, xy_positive, xy_negative, direction_code, speed, last_direction_code, speed_start, DC1_1, brushless, encodeMotor, Feed, speed_DC1, DC2, speed_DC2, DC1_2
    ControlDirections_S(directions)
    time.sleep(float(timing))
    StopMoving()
    time.sleep(0.1)

# auto_stage = 0
# Moves to Manual Stage
#
# auto_stage = 1
# Starts Program Automatic Missionsq
auto_stage = 0
speed = 40
last_direction_code = ''

smartservo_2.move_to(-40, 10)

LoadMe()
time.sleep(0.25)

while True:
    time.sleep(0.001)
    if gamepad.is_key_pressed("N1"):
        AutoStart()

    if gamepad.is_key_pressed("N2"):
        Manual()

