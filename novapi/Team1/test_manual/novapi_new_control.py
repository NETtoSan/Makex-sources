from mbuild.encoder_motor import encoder_motor_class
from mbuild.smartservo import smartservo_class
from mbuild.dual_rgb_sensor import dual_rgb_sensor_class
from mbuild import power_expand_board
from mbuild import gamepad
import novapi
import time

# Important variables
auto_stage = 0 # Auto
shoot = 0 #
invert = 0 # Invert movements
feeddc = 1 # DC front on/off
lrmode = 0  # 0 = shoot, 1 = arm
turret_origin_angle = 0 # for reset servo angle
bp = 50 # brushless power
vl = 0.5 # Movement speed

# DC motors
feeddc_main = "DC1" # Main feed belt
feeddc_front = "DC2" # Front roller
feeddc_aux = "DC3" # No need!
unsighed_dc = "DC4" # Assign if new parts are added
unsigned_dc2 = "DC5" # Assign if new parts are added
handdc1 = "DC6" # hand updown 
handdc2 = "DC7" # hand updown
handdc_roll = "DC8"
 
# Indicators
dual_rgb_sensor_1 = dual_rgb_sensor_class("PORT2", "INDEX1")
dual_rgb_sensor_2 = dual_rgb_sensor_class("PORT2", "INDEX2")

# Arm
smartservo_arm = smartservo_class("M6", "INDEX1")

# Turret
smartservo_pitch =   smartservo_class("M5", "INDEX1")
smartservo_updown = smartservo_class("M5", "INDEX2")

# Bot motors
encoder_motor_M1 = encoder_motor_class("M1", "INDEX1")
encoder_motor_M2 = encoder_motor_class("M2", "INDEX1")
encoder_motor_M3 = encoder_motor_class("M3", "INDEX1")
encoder_motor_M4 = encoder_motor_class("M4", "INDEX1")