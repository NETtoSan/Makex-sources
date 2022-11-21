# codes make you cry
import novapi
import math
import time
from mbuild import gamepad
from mbuild.encoder_motor import encoder_motor_class
from mbuild import power_expand_board
from mbuild.smartservo import smartservo_class

# initialize mechanic variables
BP = 40
SP = 50
flow = 0
maxspeedi = 0.25
brushless = 0
automatic_mode = 1
inverse = -1 # 1 to disable

# initialize math variables
x = 0
y = 0.19
velocity = 0
_E0_B9_81 = 0
c = 0
a = 0
xf = 0
yf = 0
theta2 = 0
x_ = 0
mps = 0
velocity_back = 0

# new class
EM1 = encoder_motor_class("M1", "INDEX1") # FRONT LEFT WHEEL
EM2 = encoder_motor_class("M2", "INDEX1") # FRONT RIGHT WHEEL
EM3 = encoder_motor_class("M3", "INDEX1") # BALL BELT
EM4 = encoder_motor_class("M4", "INDEX1")
SERVO1 = smartservo_class("M1", "INDEX1") # WRIST
SERVO2 = smartservo_class("M2", "INDEX1") # HAND LEFT
SERVO3 = smartservo_class("M3", "INDEX1") # HAND RIGHT
SERVO4 = smartservo_class("M4", "INDEX1") 
SERVO5 = smartservo_class("M5", "INDEX1")
SERVO6 = smartservo_class("M6", "INDEX1")

# map BASIC controls
BallBeltHR ='N1'
BallBeltTG = 'N2'
BallBeltH = 'N3'
AutoMode = 'N4'
RotateL = 'L1'
RotateR = 'R1'
ShootTG = 'L2'
ShootHD = 'R2'
ArmUp = 'Left'
ArmDown = 'Right'
BPUp = 'Up'
BPDown =  ' Down'


"""Blueprint right here!
    +=== CONTROLS ===+
    Left Joystick ( Analog ): Robot's movement 6 AXIS
    Right Joystick ( Analog ) RX: Rotate Wrist/Flag
    Right Joystick ( Analog ) RY: Hand Squeeze
    Left Joystick (Click): -
    Right Joystick (Click): -

    DPAD LEFT: Arm Up
    DPAD RIGHT: Arm Down
    DPAD UP: + Brushless Power  // Ice's power manager
    DPAD DOWN: - Brushless Power // Ice's power manager

    BTN1: Ball Belt Hold ( CCW )
    BTN2: Ball Belt Toggle
    BTN3:  Ball Belt Hold ( CW )
    BTN4: Automatic Mode ( NOT SET )

    L1: Rotate Bot Left
    L2: Shooter (Toggle)
    R1: Rotate Bot Right
    R2: Shooter (Hold And Shoot)

    =========== CONNECTIONS =============
    NovaPI Mainboard
    M1: Wheel (Fl)
    M2: Wheel (Fr)
    M3: Belt
    M4: Wrist
    M5: Left Hand
    M6: Right Hand

    SERVO1: Wrist
    SERVO2: Left Hand
    SERVO3: Right Hand
    SERVO4:
    SERVO5:
    SERVO6:
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
    velocity = math.sqrt((4.9 * (x * x)) / ((math.cos(4 / 180.0 * math.pi) * math.cos(4 / 180.0 * math.pi)) * ((math.tan(4 / 180.0 * math.pi) * x + y))))
    return velocity

def power_to_velocity(power): #Returns m/s from Brushless power precentage
    return 0.2284 * power

def velocity_to_power(velocity): #Returns Brushless power percentage from velocity
    return velocity / 0.2284

def rpm_to_mps(radius, rpm): #Reurns m/s from RPM and Wheel Radius
    #global mps
    mps = (2 * (3.1452 * (radius * rpm))) / 60
    return mps

#y = 0.19

# ================= The Mechanics ===================== #
def FlowModule(Mode):
    global flow
    if Mode == 0: # <Hold> Ball Belt
        while not (not gamepad.is_key_pressed(BallBeltH)):
            time.sleep(0.001)
            EM3.set_power(90)
            power_expand_board.set_power("DC3", 100)
        EM3.set_power(0)
        power_expand_board.set_power("DC3", 0)

    if Mode == 1: # <Toggle> Ball Belt
        if flow == 0:
            flow = 1

        else:
            flow = 0

        while not (flow == 0):
            time.sleep(0.001)
            EM3.set_power(70)
            power_expand_board.set_power("DC3", 100)
            if gamepad.is_key_pressed(BallBeltTG):
                EM3.set_power(0)
                power_expand_board.set_power("DC3", 0)
                flow = 0

    if Mode == 2: # <Hold,Reverse> Ball Belt
        while not (not gamepad.is_key_pressed(BallBeltHR)):
            time.sleep(0.001)
            EM3.set_power(-90)
            power_expand_board.set_power("DC3", -100)

        EM3.set_power(0)
        power_expand_board.set_power("DC3", 0)

def Mover(W1, W2, W3, W4):
    EM1.set_power(W1)
    EM2.set_power(W2)
    #EM1.set_power(W3)
    #EM1.set_power(W4)

def hand_mover(v_center,v_left,v_right): # UNRELIABLE, FIX THIS LATER
    SERVO5.move(v_center,90)
    SERVO4.move(-1*v_left,90)
    SERVO6.move(v_right,90)


def BotMover(Direction, Amount,Amount2,Amount3):
    Mover(0, 0, 0, 0)
    if Direction == 'U' or Direction == 'D' or Direction == 'L' or Direction == 'R':
        if Direction == 'U':
            Mover(Amount, Amount)

        if Direction == 'D':
            Mover(-1 * Amount, -1* Amount)

        if Direction == 'L':
            Mover(Amount, 0)

        if Direction == 'R':
            Mover(0, Amount)

        if Direction == 'HAND' or Direction == 'HND': # RESET SERVO HERE
            hand_mover(Amount,Amount2,Amount3)
    else:
        Mover(0, 0, 0, 0)
        hand_mover(0,0,0)

def AutomaticMode():
    """25: 15cm/sec
    50: 30cm/sec
    100: 60cm/sec
    Based on NETtoSan's calculations."""
    BotMover('U',50)
    time.sleep(1)
    BotMover('R',50)
    EM3.set_power(90)
    power_expand_board.set_power("DC3", 100)
    time.sleep(5)
    #smaller triangle here
    #large triangle below
    for i in range(0,90,5): # roughly a triangle (18 cycles) 
        mybppower = velocity_to_power(vel_from_angle_distance(i,3.96/math.cos(i)))
        power_expand_board.set_power("BL1", mybppower)
        power_expand_board.set_power("BL2", mybppower)
        time.sleep(1)
        BotMover('R',i/2) # CHANGE HERE!
        BotMover() # Reset
    

def ShooterModule_N(Mode):
    global BP, brushless
    # Mode 0: Manual Hold
    # Mode 1: Toggle Shoot
    if Mode == 0:
        power_expand_board.set_power("BL1", BP)
        power_expand_board.set_power("BL2", BP)
        #power_expand_board.set_power("DC3", -50)
        while not not gamepad.is_key_pressed(ShootHD):
            pass

        power_expand_board.stop("BL1")
        power_expand_board.stop("BL2")
        #power_expand_board.stop("DC3")

    else:
        if brushless == 0:
            brushless = 1

        else:
            brushless = 0

        if brushless == 1:
            power_expand_board.set_power("BL1", BP)
            power_expand_board.set_power("BL2", BP)
            #power_expand_board.set_power("DC3", -100)

        else:
            power_expand_board.stop("BL1")
            power_expand_board.stop("BL2")
            #power_expand_board.stop("DC3")

        while not not gamepad.is_key_pressed(ShootTG):
            pass

def MoveModule():
    EM1.set_power(0.8*(gamepad.get_joystick("Ly")+gamepad.get_joystick("Lx"))*inverse)
    EM2.set_power(-0.8*(gamepad.get_joystick("Ly")-gamepad.get_joystick("Lx"))*inverse)
    
    #rotating a hand 
    hand_mover(gamepad.get_joystick("Rx"),0,0)

    #griping the hand
    hand_mover(0,gamepad.get_joystick("Ry"),(-1) *gamepad.get_joystick("Ry"))


# ================= Main Program ===================== #

while True:
    time.sleep(0.001)
    MoveModule()
    power_expand_board.set_power("DC7", -1 * (gamepad.get_joystick("Rx") / 10)) # Flag
    if gamepad.is_key_pressed(BallBeltH): # Ball Belt Clockwise <Hold>
        FlowModule(0)

    if gamepad.is_key_pressed(RotateR): # Rotate Bot Right
        while not (not gamepad.is_key_pressed(RotateR)):
            time.sleep(0.001)
            BotMover('R', 100)

        BotMover('N', 0)

    if gamepad.is_key_pressed(ShootHD): # Hold And Shoot
        ShooterModule_N(0)

    if gamepad.is_key_pressed(RotateL): # Rotate Bot Left
        while not (not gamepad.is_key_pressed(RotateL)):
            time.sleep(0.001)
            BotMover('L', 100)

        BotMover('N', 0)

    if gamepad.is_key_pressed(ShootTG): # Toggle Shoot
        ShooterModule_N(1)

    if gamepad.is_key_pressed(BPUp): # Brushless power up
        BP += 10

    if gamepad.is_key_pressed(BPDown): # Brushless power down
        BP -= 10

    if gamepad.is_key_pressed(ArmUp): # Arm Up
        power_expand_board.set_power("DC2", -100)
        while not not gamepad.is_key_pressed(ArmUp):
            pass
        power_expand_board.stop("DC2")

    if gamepad.is_key_pressed(ArmDown): # Arm Down
        power_expand_board.set_power("DC2", 50)  
        while not not gamepad.is_key_pressed(ArmDown):
            pass

        power_expand_board.stop("DC2")

    if gamepad.is_key_pressed(BallBeltHR): # Ball Belt Counter Clockwise <Hold>
        FlowModule(2)
        
    if gamepad.is_key_pressed(BallBeltTG): # Ball Belt Clockwise <Toggle>
        FlowModule(1)
        pass

    if gamepad.is_key_pressed(AutoMode): # AUTOMATIC
        if manual_automatic_mode == 1:
            manual_automatic_mode = 0
            AutomaticMode()