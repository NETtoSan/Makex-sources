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
vl = 0.7

# new class
smartservo_1 = smartservo_class("M6", "INDEX1")
smartservo_2 = smartservo_class("M6", "INDEX2")
smartservo_3 = smartservo_class("M5", "INDEX1")
distance_sensor_1 = ranging_sensor_class("PORT5", "INDEX1")
dual_rgb_sensor_1 = dual_rgb_sensor_class("PORT4", "INDEX1")

# Encoder motors
EFl = encoder_motor_class("M1", "INDEX1")
EFr = encoder_motor_class("M2", "INDEX1")
ERl = encoder_motor_class("M3", "INDEX1")
ERr = encoder_motor_class("M4", "INDEX1")

def RangingLED():
    if distance_sensor_1.get_distance() > 200:
        dual_rgb_sensor_1.set_led_color("green")

    if distance_sensor_1.get_distance() < 200:
        dual_rgb_sensor_1.set_led_color("blue")
def MovementCode():
    global vl
    Lx = gamepad.get_joystick("Lx")
    Ly = gamepad.get_joystick("Ly")

    EFl.set_power(vl * (Ly - Lx))
    EFr.set_power(vl * (-Ly - Lx))
    ERl.set_power(-vl * (-Ly + Lx))
    ERr.set_power(-vl * (Ly + Lx))
    
def Manual():
    while True:
        time.sleep(0.001)
        RangingLED()
        MovementCode()

        if gamepad.is_key_pressed("L2"):
            smartservo_3.move(90, 50)
            time.sleep(1)
            steps = 180
            while steps <= 180:
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

    
        if gamepad.is_key_pressed("R1"):
            if BL_SPEED is 50:
                BL_SPEED = 100
            elif BL_SPEED is 100:
                BL_SPEED = 0
            else:
                BL_SPEED = 50
            while not not gamepad.is_key_pressed("R1"):
                pass
    


        power_expand_board.set_power("BL1", BL_SPEED)
        power_expand_board.set_power("BL2", BL_SPEED)

        smartservo_1.set_power(0.1 * gamepad.get_joystick("Rx"))
        smartservo_2.move(0.1 * gamepad.get_joystick("Ry"), 0.1 * 0)

Manual()