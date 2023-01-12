# codes make you happy

from mbuild.encoder_motor import encoder_motor_class
from mbuild.smartservo import smartservo_class
from mbuild.dual_rgb_sensor import dual_rgb_sensor_class
from mbuild.smart_camera import smart_camera_class
from mbuild import power_expand_board
from mbuild import gamepad
import novapi
import time

# new class
dual_rgb_sensor_1 = dual_rgb_sensor_class("PORT3", "INDEX1")
novacam = smart_camera_class("PORT4", "INDEX1")

encoder_motor_M1 = encoder_motor_class("M1", "INDEX1")
encoder_motor_M2 = encoder_motor_class("M2", "INDEX1")
encoder_motor_M3 = encoder_motor_class("M3", "INDEX1")
encoder_motor_M4 = encoder_motor_class("M4", "INDEX1")

novacam.set_mode("color")

vl = 0.5
light = True

class ManualCode:

    def Move(v1,v2,v3,v4):
        encoder_motor_M1.move(v1)
        encoder_motor_M2.move(v2)
        encoder_motor_M3.move(v3)
        encoder_motor_M4.move(v4)

    def JoystickMovement():
        global vl
        Lx = gamepad.get_joystick("Rx")  # literally Lx variable
        Fl = 0   # Front left
        Fr = 0   # Front right
        Rl = 0   # Rear left
        Rr = 0   # Rear right   
        Fl = Lx
        Fr = Lx
        Rl = Lx
        Rr = Lx
        EFl = vl * (gamepad.get_joystick("Ly") - Rl
                    - gamepad.get_joystick("Lx"))
        EFr = -vl * (gamepad.get_joystick("Ly") + Rr
                     + gamepad.get_joystick("Lx"))
        ERl = vl * (gamepad.get_joystick("Ly")
                    + Fl - gamepad.get_joystick("Lx"))
        ERr = -vl * (gamepad.get_joystick("Ly") - Fr
                     + gamepad.get_joystick("Lx"))
        encoder_motor_M1.set_power(EFl)
        encoder_motor_M2.set_power(EFr)
        encoder_motor_M3.set_power(ERl)
        encoder_motor_M4.set_power(ERr)
            
    def ButtonControls():
        global light
        if gamepad.is_key_pressed("L1"):
            power_expand_board.set_power("DC8", 100)
        else:
            power_expand_board.stop("DC8")
            
        if gamepad.is_key_pressed("N3"):
            if light is True:
                novacam.open_light()
                light = False
            elif light is False:
                novacam.close_light()
                light = True
            while not not gamepad.is_key_pressed("N3"):
                pass
            
        if gamepad.is_key_pressed("R1"):
            pass
        else:
            pass

class AutoCode:
    def __init__(self):
        pass
    def Movement(direction):
        if direction is "left":
            ManualCode.Move(-50,50,50,-50)
        if direction is "right":
            ManualCode.Move(50,-50,-50,50)
        if direction is "rotateleft":
            ManualCode.Move(50,50,50,50)
        if direction is "rotateright":
            ManualCode.Move(-50,-50,-50,-50)
        if direction is "forward":
            ManualCode.Move(50,-50,50,-50)
        if direction is "backward":
            ManualCode.Move(-50,50,-50,50)


while True:
    time.sleep(0.001)
    #ManualCode.Movement()
    ManualCode.ButtonControls()

    #SmartCameraCode
    if novacam.detect_sign(1):
        dual_rgb_sensor_1.set_led_color("red")
    else:
        dual_rgb_sensor_1.set_led_color("blue")

    if(novacam.detect_sign(1)):

        # Align bot angle to default ( arena angle )
        roll = novapi.get_roll()
        default_angle = 0
        while(roll is not default_angle):
            if(roll < default_angle):
                AutoCode.Movement("rotateleft")
                roll = novapi.get_roll()
            elif(roll > default_angle):
                AutoCode.Movement("rotateright")
                roll = novapi.get_roll()

        # Move the bot bot always perpendicular to arena's angle
        center = novacam.detect_sign_location(1, "middle")
        while(center is not True):
            stat  = novacam.detect_sign_location(1, "left")
            if(stat is True):
                AutoCode.Movement("left")
                center = novacam.detect_sign_location(1, "middle")
            else:
                stat = novacam.detect_sign_location(1, 'right')
                if(stat is True):
                    AutoCode.Movement("left")
                    center = novacam.detect_sign_location(1, "middle")
       
        # Obtain distance between bot and objects
        # Code goes here blablablablalbalbal
