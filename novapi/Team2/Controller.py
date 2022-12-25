import novapi
import math
import random
from mbuild import gamepad
from mbuild.encoder_motor import encoder_motor_class
from mbuild import power_expand_board
from mbuild.smartservo import smartservo_class
from mbuild.ranging_sensor import ranging_sensor_class

# initialize mechanic variables
BP = 40
SP = 50
flow = 0
maxspeedi = 0.25
brushless = 0
manual_automatic_mode = 1
inverse = 1 # 1 to disable
inverse2 = 1
fliparm = 0

# new class
RightWheel = encoder_motor_class("M1", "INDEX1") # FRONT RIGHT WHEEL
FeedBelt = encoder_motor_class("M2", "INDEX1") # FRONT LEFT WHEEL
LeftWheel = encoder_motor_class("M3", "INDEX1") # BALL BELT
EM4 = encoder_motor_class("M4", "INDEX1")
SERVO1 = smartservo_class("M1", "INDEX1") # WRIST
SERVO2 = smartservo_class("M2", "INDEX1") # HAND LEFT
SERVO3 = smartservo_class("M3", "INDEX1") # HAND RIGHT
SERVO4 = smartservo_class("M4", "INDEX1") 
SERVO5 = smartservo_class("M5", "INDEX1")
SERVO6 = smartservo_class("M6", "INDEX1")
distance_sensor_1 = ranging_sensor_class("PORT3", "INDEX1")

# map BASIC controls
BallBeltTG = 'N1'
BallBeltINV = 'N2'
AutoMode = '+'
RotateL = 'L1'
RotateR = 'R1'
ShootTG = 'L2'
#ArmUp = 'Left' 
#ArmDown = 'Right'
BPUp = 'Up'
BPDown =  'Down'

"""Blueprint right here!
    +=== CONTROLS ===+
    Left Joystick ( Analog ): Robot's movement 6 AXIS
    Right Joystick ( Analog ) RX: Rotate Wrist/Flag
    Right Joystick ( Analog ) RY: Move Arm
    Left Joystick (Click): -
    Right Joystick (Click): -

    DPAD LEFT: Grip +
    DPAD RIGHT: Grip -
    DPAD UP: + Brushless Power  // Ice's power manager
    DPAD DOWN: - Brushless Power // Ice's power manager

    BTN1:  Ball Belt Toggle
    BTN2: Invert all belt directions
    BTN3: - 
    BTN4: -

    L1: Rotate Bot Left
    L2: Shooter (Toggle)
    R1: Rotate Bot Right
    R2: -

    +: Automatic Mode
    =========== CONNECTIONS =============
    NovaPI Mainboard
    M1: Wheel (Fl)
    M2: Wheel (Fr)
    M3: Belt
    M4: Wrist
    M5: Left Hand
    M6: Right Hand

    SERVO1: -
    SERVO2: -
    SERVO3: -
    SERVO4: Left Hand
    SERVO5: Wrist
    SERVO6: Right Hand
    NovaPi Extension Board
    DC1: -
    DC2: Arm Belt
    DC3: Front Belt
    DC7: Flag
    DC8: -
    BL1: Shooter
    BL2: Shooter
    """

# ================== The Math ======================= # 
# Full credits goes to @Knilios

def vel_from_angle_distance(number1, number2): # arg1: angle (degrees) arg2: distance (meters) 
    #global x, y, velocity, _E0_B9_81, c, a, xf, yf, theta2, x_, mps, velocity_back
    x_ = number2 * (1 / math.cos(number1 / 180.0 * math.pi))
    x = x_
    return math.sqrt((4.9 * (x * x)) / ((math.cos(4 / 180.0 * math.pi) * math.cos(4 / 180.0 * math.pi)) * ((math.tan(4 / 180.0 * math.pi) * x + 0.05))))
    

def power_to_velocity(power): #Returns m/s from Brushless power precentage
    return 0.2284 * power

def velocity_to_power(velocity): #Returns Brushless power percentage from velocity
    return velocity / 0.2284

def rpm_to_mps(rpm): #Reurns m/s from RPM and Wheel Radius
    #global mps
    return (2 * (3.1452 * (0.029 * rpm))) / 60

def mps_to_rpm(mps):
    return 60*mps/(2 * (3.1452 * 0.029))

def angle_to_distance(angle,blength) : #for the wheels
    return ( angle / 180 ) * math.pi * blength

def distance_and_time_to_speed(x,t) : 
    return x / t
#y = 0.19

# ================= The Mechanics ===================== #
def FlowListener(Mode):
    global flow,inverse2
    if Mode == 1: # <Toggle> Ball Belt
        if flow == 0:
            flow = 1
        else:
            flow = 0

def hand_mover(v_center,v_left,v_right): # UNRELIABLE, FIX THIS LATER
    SERVO5.move(v_center,20)
    SERVO4.move(-1*v_left,20)
    SERVO6.move(v_right,20)
    limit = 1000
    
    if SERVO4.get_value("current") > limit:
        SERVO4.set_power(0)
    if SERVO6.get_value("current") > limit:
        SERVO6.set_power(0)

def ShooterListener(Mode):
    global BP, brushless
    # Mode 0: Manual Hold
    # Mode 1: Toggle Shoot
    if Mode == 1:
        if brushless == 0:
            brushless = 1

        else:
            brushless = 0
            #power_expand_board.stop("DC3")

        while not not gamepad.is_key_pressed(ShootTG):
            pass

def MoveModule():
    sensitivity = 1.5
    #if inverse == -1 :
    #    RightWheel.set_power(0.8*(gamepad.get_joystick("Ly")-(gamepad.get_joystick("Lx")))/sensitivity)
    #    LeftWheel.set_power(-0.8*(gamepad.get_joystick("Ly")+(gamepad.get_joystick("Lx")))/sensitivity)
    #else :
    #    LeftWheel.set_power(0.8*(gamepad.get_joystick("Ly")-(gamepad.get_joystick("Lx")))/sensitivity)
    #    RightWheel.set_power(-0.8*(gamepad.get_joystick("Ly")+(gamepad.get_joystick("Lx")))/sensitivity)

    if inverse == -1 :
        RightWheel.set_power(0.8*(gamepad.get_joystick("Ly"))/sensitivity)
        LeftWheel.set_power(-0.8*(gamepad.get_joystick("Ly"))/sensitivity)
    else :
        LeftWheel.set_power(0.8*(gamepad.get_joystick("Ly"))/sensitivity)
        RightWheel.set_power(-0.8*(gamepad.get_joystick("Ly"))/sensitivity)
    
    #rotating a hand
    if gamepad.get_joystick("Rx") == 100:
        hand_mover(gamepad.get_joystick("Rx")/25,0,0)
        time.sleep(0.001)
        

    # Move hand up/down
    invalue = gamepad.get_joystick("Ry")*-1
    if invalue is 0:
        invalue = -10
    else:
        gamepad.get_joystick("Ry")*-1
    power_expand_board.set_power("DC2",invalue)

    # Hand gripper
    if gamepad.is_key_pressed('Left'):
        hand_mover(0,100,-100)
    elif gamepad.is_key_pressed('Right'):
        hand_mover(0,-100,100)
    else:
        hand_mover(0,0,0)


ranging_value = 0
steps = 0
origin_angle = 0 
def movevl(v1,v2):
    LeftWheel.set_power(v1)
    RightWheel.set_power(-v2)

def autocube():
    
    pass

def autoshoot():
    ison = True
    steps = 0
    power_expand_board.set_power("DC1",-70)

    # Move to ball zone
    time.sleep(1)
    movevl(-50,50)
    time.sleep(0.25)     
    movevl(50,50)
    time.sleep(0.6)
    movevl(50,-50)
    time.sleep(0.35)

    # Collect ball
    movevl(50,50)  # get ball
    time.sleep(0.7)
    movevl(-50,-50) # go back
    time.sleep(0.5)
    movevl(0,0)
    
    # SHOOT BALL . WAIT BALL TO GET NEAR RANGING SENSOR
    while ison:
        ranging_value = float(distance_sensor_1.get_distance())
        FeedBelt.set_power(-100)
        if ranging_value < 10:
            power_expand_board.set_power("BL1",50)
            power_expand_board.set_power("BL2",50)
            FeedBelt.set_power(-100)
            time.sleep(2.5) # CHANGE HERE
            movevl(-50,50) 
            time.sleep(0.5) # CHANGE HERE
            movevl(50,-50)
            time.sleep(0.5)
            movevl(0,0)
            ison = False
        steps += 1
        time.sleep(0.5)
        if steps == 20 :
            movevl(5,5) 
            time.sleep(0.5)
            movevl(0,0)
        elif steps >= 40:
            ison = False
            break
    '''
    while steps < 3: #ranging_value is 0:
        
        ranging_value = float(distance_sensor_1.get_distance())
        if ranging_value < 10:
            power_expand_board.set_power("BL1",50)
            power_expand_board.set_power("BL2",50)
            FeedBelt.set_power(-100)
            time.sleep(2.5)
            movevl(-50,50)
            time.sleep(0.15)
            movevl(0,0)

            steps += 1
        else:
            FeedBelt.set_power(-50)
            power_expand_board.set_power("BL1",0)
            power_expand_board.set_power("BL2",0)
    '''
    power_expand_board.set_power("BL1", 0)
    power_expand_board.set_power("BL2", 0)
    power_expand_board.stop("DC1")
    FeedBelt.set_power(0)
# ================= Main Program ===================== #

while True:
    time.sleep(0.001)
    MoveModule()
    power_expand_board.set_power("DC7", -1 * (gamepad.get_joystick("Rx") / 10)) # Flag
    if gamepad.is_key_pressed(RotateR): # Rotate Bot Right
        while not not gamepad.is_key_pressed(RotateR):
            LeftWheel.set_power(45)
            RightWheel.set_power(45)

        LeftWheel.set_power(0)
        RightWheel.set_power(0)

    if gamepad.is_key_pressed(RotateL): # Rotate Bot Left
        while not not gamepad.is_key_pressed(RotateL):
            time.sleep(0.001)
            LeftWheel.set_power(-45)
            RightWheel.set_power(-45)

        LeftWheel.set_power(0)
        RightWheel.set_power(0)

    if gamepad.is_key_pressed(ShootTG): # Toggle Shoot
        ShooterListener(1)
        
    if gamepad.is_key_pressed(BPUp): # Brushless power up
        if BP != 30:
            BP = 30
        while not not gamepad.is_key_pressed(BPUp):
            pass

    if gamepad.is_key_pressed(BPDown): # Brushless power down
        if BP != 15:
            BP = 15
        while not not gamepad.is_key_pressed(BPDown):
            pass
   
    if gamepad.is_key_pressed(BallBeltTG): # Ball Belt Clockwise <Toggle>
        time.sleep(0.001)
        FlowListener(1)
        while not not gamepad.is_key_pressed(BallBeltTG):
            pass

    if gamepad.is_key_pressed(BallBeltINV):
        time.sleep(0.001)
        inverse2 = inverse2* -1
        while not not gamepad.is_key_pressed(BallBeltINV):
            pass

    if gamepad.is_key_pressed(AutoMode): # AUTOMATIC
        if manual_automatic_mode == 1:
            manual_automatic_mode = 0
            autoshoot()
    if gamepad.is_key_pressed('N3'): # Rotate ball belt manually <Hold>
        while not not gamepad.is_key_pressed('N3'):
            time.sleep(0.001)
            FeedBelt.set_power(inverse2*100)
        FeedBelt.set_power(0)

    if gamepad.is_key_pressed('R2'): # Rotate ball belt manually <Hold>
        inverse = inverse*-1
        while not not gamepad.is_key_pressed('R2'):
            pass
        
    if gamepad.is_key_pressed("N4"):
        if fliparm == 0:
            SERVO5.move_to(-180,50)
            fliparm = 1
        else:
            SERVO5.move_to(180,50)
            fliparm = 0

        while not not gamepad.is_key_pressed("N4"):
            pass

    #Check values
    if flow == 1:
            power_expand_board.set_power("DC1", inverse2*100)
    else:
        power_expand_board.set_power("DC1", 0)

    if brushless == 1:
        power_expand_board.set_power("BL1", BP)
        power_expand_board.set_power("BL2", BP)

    else:
        power_expand_board.stop("BL1")
        power_expand_board.stop("BL2")
