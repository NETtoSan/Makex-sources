# codes make you happy
import novapi
import time
from mbuild.smartservo import smartservo_class
from mbuild.ranging_sensor import ranging_sensor_class
from mbuild.dual_rgb_sensor import dual_rgb_sensor_class
from mbuild import gamepad
from mbuild import power_expand_board
from mbuild.encoder_motor import encoder_motor_class

# initialize variables
BL_SPEED = 0
ranging_data = [] # Each data are 5 degrees apart


# new class
smartservo_1 = smartservo_class("M2", "INDEX1")
smartservo_2 = smartservo_class("M2", "INDEX2")
smartservo_3 = smartservo_class("M4", "INDEX1")
distance_sensor_1 = ranging_sensor_class("PORT3", "INDEX1")
dual_rgb_sensor_1 = dual_rgb_sensor_class("PORT2", "INDEX1")
encoder_motor_M1 = encoder_motor_class("M1", "INDEX1")

BL_SPEED = 50

while True:
    time.sleep(0.001)
    if distance_sensor_1.get_distance() > 200:
        dual_rgb_sensor_1.set_led_color("green")

    if distance_sensor_1.get_distance() < 200:
        dual_rgb_sensor_1.set_led_color("blue")

    if gamepad.is_key_pressed("L2"):
        smartservo_3.move(90, 50)
        time.sleep(1)
        steps = 36
        while steps <= 36:
            smartservo_3.move(-5)
            steps += 1
            time.sleep(0.25)


        smartservo_3.move(90,50)
        while not not gamepad.is_key_pressed("L2"):
            pass


        #smartservo_3.move(-180, 50)
        #time.sleep(1)
        #smartservo_3.move(90, 100)
        #time.sleep(1)

    
    if gamepad.is_key_pressed("N1"):
        if BL_SPEED is 50:
            BL_SPEED = 100
        elif BL_SPEED is 100:
            BL_SPEED = 0
        else:
            BL_SPEED = 50
        while not not gamepad.is_key_pressed("N1"):
            pass
    

    if gamepad.is_key_pressed("R1"):
        power_expand_board.set_power("BL1", BL_SPEED)
        power_expand_board.set_power("BL2", BL_SPEED)


    # Magazine code
    if gamepad.is_key_pressed("Up"):
        encoder_motor_M1.set_power(20)

    else:
        encoder_motor_M1.set_power(0)

    smartservo_1.move(0.3 * gamepad.get_joystick("Rx"), 0.3 * gamepad.get_joystick("Rx"))
    smartservo_2.move(0.1 * gamepad.get_joystick("Ly"), 0.1 * gamepad.get_joystick("Ly"))

