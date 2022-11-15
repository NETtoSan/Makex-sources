from mbuild.encoder_motor import encoder_motor_class
from mbuild.smartservo import smartservo_class
from mbuild.dual_rgb_sensor import dual_rgb_sensor_class
from mbuild import power_expand_board
from mbuild import gamepad
import novapi
import time

# initialize the variables
auto_stage = 1
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
    dual_rgb_sensor_1.set_led_color("blue")
    dual_rgb_sensor_2.set_led_color("blue")
    time.sleep(5)
    pass

def Manual():
    dual_rgb_sensor_1.set_led_color("red")
    dual_rgb_sensor_2.set_led_color("red")



while True:
    time.sleep(0.001)

    dual_rgb_sensor_1.set_led_color("green")
    dual_rgb_sensor_2.set_led_color("red")
    while not gamepad.is_key_presed("L1"):
        pass

    if auto_stage == 1:
        AutoStart()
        auto_stage = 0

    else:
        Manual()
