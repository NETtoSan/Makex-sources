# codes make you cry
import novapi
from mbuild import gamepad
from mbuild.encoder_motor import encoder_motor_class
from mbuild import power_expand_board
from mbuild.smartservo import smartservo_class

# initialize variables
BP = 65
SP = 50
brushless = 0
flow = 0
maxspeedi = 0.25
safetyangle = 0
automatic_mode = 1

# new class
EM1 = encoder_motor_class("M1", "INDEX1") # FRONT LEFT WHEEL
EM2 = encoder_motor_class("M2", "INDEX1") # FRONT RIGHT WHEEL
EM3 = encoder_motor_class("M3", "INDEX1") # BALL BELT
#EM4 = encoder_motor_class("M4", "INDEX1") # HAND
#SERVO1 = smartservo_class("M1", "INDEX1") # WRIST
#SERVO2 = smartservo_class("M2", "INDEX1")
#SERVO3 = smartservo_class("M3", "INDEX1")
#SERVO4 = smartservo_class("M4", "INDEX2")
#SERVO5 = smartservo_class("M6", "INDEX1")
#SERVO6 = smartservo_class("M6", "INDEX2")
S1 = smartservo_class("M4","INDEX1") # wrist
S2 = smartservo_class("M5","INDEX1") # hand left
S3 = smartservo_class("M6","INDEX1") # hand right

# map BASIC controls
BallBeltTG =  'N2'
BallBeltH = 'N3'
BallBeltHR ='N1'

"""Blueprint right here!
    +=== CONTROLS ===+
    Left Joystick ( Analog ): Robot's movement 6 AXIS
    Right Joystick ( Analog ) RX: Rotating hand                                              //Flag movement/Drift CTL - ไม่ใช้แล้ว
    Right Joystick ( Analog ) RY: Hand Squeeze
    Left Joystick (Click): -
    Right Joystick (Click): -
    DPAD LEFT: Arm Up
    DPAD RIGHT: Arm Down
    DPAD UP: Hand Up
    DPAD DOWN: Hand Down
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
    M4: Hand's wrist - 17/7/2022
    M5: - hand's left servo looking from the robot - 17/11/2022
    M6: - hand's right servo looking form the robot  - 17/11/2022
    NovaPi Extension Board
    DC1: -
    DC2: Arm Belt
    DC3: Shooter Belt
    DC8: Hand // I think no need to use this any more since the hand will be controled using 3 servos. - 17/11/2022
    BL1: Shooter
    BL2: Shooter
    """

# The MoveModule2 function is the quick replacement for MoveModule. - 17/11/2022
def MoveModule2() :
    EM1.set_power(0.8*(gamepad.get_joystick("Ly")+gamepad.get_joystick("Lx")))
    EM2.set_power(-0.8*(gamepad.get_joystick("Ly")-gamepad.get_joystick("Lx")))

# Techinac
def MoveModule(Mode=180):
    global BP, SP
    # Used NEToSan's control scheme.
    Fl = 0
    Fr = 0
    Rl = 0
    Rr = 0
    drift = gamepad.get_joystick("Rx")
    if not gamepad.get_joystick("Lx") == 0:
        if gamepad.get_joystick("Lx") < 0:
            Fl = (gamepad.get_joystick("Lx") + 10)

        if gamepad.get_joystick("Lx") > 0:
            Fl = (gamepad.get_joystick("Lx") - 10)

        Fr = (gamepad.get_joystick("Lx") + Fr)
        Rl = (gamepad.get_joystick("Lx") + Rl)
        Rr = (gamepad.get_joystick("Lx") + Rr)
    if Mode == 45:
        # Wheels angled 45 degrees
        EM1.set_power(maxspeedi * ((gamepad.get_joystick("Ly") - ((Fl + drift)))))
        EM2.set_power((-1 * maxspeedi) * ((gamepad.get_joystick("Ly") + ((Fr - drift)))))
        #EM3.set_power(maxspeedi * ((gamepad.get_joystick("Ly") + ((Rl + drift)))))
        #EM4.set_power((-1 * maxspeedi) * ((gamepad.get_joystick("Ly") - ((Rr - drift)))))

    if Mode == 90:
        # Wheels angled 90 degrees
        EM1.set_power(maxspeedi * ((gamepad.get_joystick("Ly") + 0)))
        EM2.set_power((-1 * maxspeedi) * ((gamepad.get_joystick("Lx") + 0)))
        #EM3.set_power(maxspeedi * ((gamepad.get_joystick("Lx") + 0)))
        #EM4.set_power((-1 * maxspeedi) * ((gamepad.get_joystick("Ly") + 0)))

    if Mode == 180:
        # Wheels angled 180 degrees ( Normal: Default )
        EM1.set_power(maxspeedi * ((gamepad.get_joystick("Ly") - ((Rl - drift)))))
        EM2.set_power((-1 * maxspeedi) * ((gamepad.get_joystick("Ly") + ((Rr + drift)))))
        #EM3.set_power(maxspeedi * ((gamepad.get_joystick("Ly") + ((Fl - drift)))))
        #EM4.set_power((-1 * maxspeedi) * ((gamepad.get_joystick("Ly") - ((Fr + drift)))))
    #EM4.set_power(gamepad.get_joystick("Ry")) - 19/11/2022

def FlowModule(Mode):
    global flow
    if Mode == 0: # <Hold> Ball Belt
        while not (not gamepad.is_key_pressed(BallBeltH)):
            time.sleep(0.001)
            EM3.set_power(90)

        EM3.set_power(0)

    if Mode == 1: # <Toggle> Ball Belt
        if flow == 0:
            flow = 1

        else:
            flow = 0

        while not (flow == 0):
            time.sleep(0.001)
            EM3.set_power(70)
            if gamepad.is_key_pressed(BallBeltTG):
                EM3.set_power(0)
                flow = 0

    if Mode == 2: # <Hold,Reverse> Ball Belt
        while not (not gamepad.is_key_pressed(BallBeltHR)):
            time.sleep(0.001)
            EM3.set_power(-90)

        EM3.set_power(0)

def hand_mover(v_center,v_left,v_right) :
    S1.move(90, v_center)
    S2.move(90,v_left)
    S3.move(90,v_right)

def Mover(W1, W2, W3, W4):
    EM1.set_power(W1)
    EM2.set_power(W2)
    #EM1.set_power(W3)
    #EM1.set_power(W4)

def BotMover(Direction, Amount):
    if Direction == 'U' or Direction == 'D' or Direction == 'L' or Direction == 'R':
        if Direction == 'U':
            Mover(Amount, -1 * Amount, Amount, -1 * Amount)

        if Direction == 'D':
            Mover(-1 * Amount, Amount, -1 * Amount, Amount)

        if Direction == 'L':
            Mover(-1 * Amount, -1 * Amount, -1 * Amount, -1 * Amount)

        if Direction == 'R':
            Mover(Amount, Amount, Amount, Amount)

    else:
        Mover(0, 0, 0, 0)

def AutomaticMode():
    """25: 15cm/sec
    50: 30cm/sec
    100: 60cm/sec
    Based on NETtoSan's calculations."""
    BotMover('U', 50)
    time.sleep(1.5)
    FlowModule()
    BotMover('U', 25)
    time.sleep(1.75)
    BotMover('U', 0)
    time.sleep(4)
    FlowModule()
    BotMover('D', 50)
    time.sleep(1.75)
    # Chnage Left/Right here
    BotMover('L', 100)
    time.sleep(2)
    BotMover('U', 50)
    time.sleep(4)
    # Chnage Left/Right here
    BotMover('R', 100)
    time.sleep(0.7)
    ShooterModule_N(1)
    BP = 35
    # Change Legt/Right here
    BotMover('R', 100)
    time.sleep(3)
    FlowModule()
    ShooterModule_N(1)
    BotMover('L', 0)
    # Reset

def ShooterModule_N(Mode):
    global brushless
    # Mode 0: Manual Hold
    # Mode 1: Toggle Shoot
    if Mode == 0:
        power_expand_board.set_power("BL1", BP)
        power_expand_board.set_power("BL2", BP)
        #power_expand_board.set_power("DC3", -50)
        while not not gamepad.is_key_pressed("R2"):
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

        while not not gamepad.is_key_pressed("L2"):
            pass

while True:
    time.sleep(0.001)
    MoveModule2()
    power_expand_board.set_power("DC7", -1 * (gamepad.get_joystick("Rx") / 10))
    if gamepad.is_key_pressed(BallBeltH): # Ball Belt Clockwise <Hold>
        FlowModule(0)

    if gamepad.is_key_pressed("R1"): # Rotate Bot Right
        while not (not gamepad.is_key_pressed("R1")):
            time.sleep(0.001)
            BotMover('R', 100)

        BotMover('N', 0)

    if gamepad.is_key_pressed("R2"): # Hold And Shoot
        ShooterModule_N(0)

    if gamepad.is_key_pressed("L1"): # Rotate Bot Left
        while not (not gamepad.is_key_pressed("L1")):
            time.sleep(0.001)
            BotMover('L', 100)

        BotMover('N', 0)

    if gamepad.is_key_pressed("L2"): # Toggle Shoot
        ShooterModule_N(1)

    if gamepad.is_key_pressed("Up"): # Hand Up
        SERVO5.move(30, 30)

    if gamepad.is_key_pressed("Down"): # Hand Down
        SERVO5.move(-30, 30)

    if gamepad.is_key_pressed("Left"): # Arm Up
        power_expand_board.set_power("DC2", -50)
        while not not gamepad.is_key_pressed("Left"):
            pass
        power_expand_board.stop("DC2")

    if gamepad.is_key_pressed("Right"): # Arm Down
        power_expand_board.set_power("DC2", 50)  
        while not not gamepad.is_key_pressed("Right"):
            pass

        power_expand_board.stop("DC2")

    if gamepad.is_key_pressed(BallBeltHR): # Ball Belt Counter Clockwise <Hold>
        FlowModule(2)

    if gamepad.is_key_pressed(BallBeltTG): # Ball Belt Clockwise <Toggle>
        FlowModule(1)
        pass
    
    #rotating a hand 
    hand_mover(gamepad.get_joystick("Rx"),0,0)

    #griping the hand
    hand_mover(0,gamepad.get_joystick("Ry"),(-1) *gamepad.get_joystick("Ry"))