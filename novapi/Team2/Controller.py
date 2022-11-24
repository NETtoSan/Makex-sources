# codes make you cry
import novapi
import math
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
manual_automatic_mode = 1
inverse = -1 # 1 to disable
inverse2 = 1

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
BallBeltHR ='N3'
BallBeltTG = 'N1'
BallBeltINV = 'N2'
AutoMode = '+'
RotateL = 'L1'
RotateR = 'R1'
ShootTG = 'L2'
ShootHD = 'R2'
#ArmUp = 'Left' 
#ArmDown = 'Right'
BPUp = 'Up'
BPDown =  ' Down'


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

    BTN1: Ball Belt Toggle
    BTN2: Ball Belt Hold ( CW )
    BTN3: Ball Belt Hold ( CCW )
    BTN4: Automatic Mode ( NOT SET )

    L1: Rotate Bot Left
    L2: Shooter (Toggle)
    R1: Rotate Bot Right
    R2: Shooter (Hold And Shoot)

    +: Automatic Mode
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
def FlowModule(Mode):
    global flow,inverse2

    if Mode == 0: # <Hold> Ball Belt
        while not (not gamepad.is_key_pressed(BallBeltH)):
            time.sleep(0.001)
            EM3.set_power(90)
            power_expand_board.set_power("DC3", 100)
            MoveModule()
            ShooterModule_N()
        EM3.set_power(0)
        power_expand_board.set_power("DC3", 0)

    if Mode == 1: # <Toggle> Ball Belt
        if flow == 0:
            flow = 1
        else:
            flow = 0
        '''
        if flow == 1:
            #time.sleep(0.001)
            EM3.set_power(inverse2*100)
            power_expand_board.set_power("DC3", inverse2*100)
        else:
            EM3.set_power(0)
            power_expand_board.set_power("DC3", 0)
        '''

    
    if Mode == 2: # <Hold,Reverse> Ball Belt
        while not (not gamepad.is_key_pressed(BallBeltHR)):
            time.sleep(0.001)
            EM3.set_power(-90)
            power_expand_board.set_power("DC3", -100)
            MoveModule()
            ShooterModule_N()

        EM3.set_power(0)
        power_expand_board.set_power("DC3", 0)

def Mover(W1=0, W2=0,angle=90):
    EM1.move(angle,W1)
    EM2.move(angle,W2)
    #EM1.set_power(W3)
    #EM1.set_power(W4)


def BotMover(dir,power):
    MoveElements = ['U','D','L','R']
    power = int(power)
    if dir == 'U':
        Mover(power, power)

    if dir == 'D':
        Mover(-1 * power, 1 * power)

    if dir == 'L':
        Mover(power)

    if dir == 'R':
        Mover(0, power)
    else:
        Mover(0, 0, 0, 0)
        hand_mover(0,0,0)
    Mover()

def hand_mover(v_center,v_left,v_right): # UNRELIABLE, FIX THIS LATER
    SERVO5.move(v_center,10)
    SERVO4.move(-1*v_left,10)
    SERVO6.move(v_right,10)
    limit = 1000
    if SERVO5.get_value("current") > limit:
        SERVO5.set_power(0)
    if SERVO4.get_value("current") > limit:
        SERVO4.set_power(0)
    if SERVO6.get_value("current") > limit:
        SERVO6.set_power(0)

def AutomaticMode2():
    EM1.move(360, 0)
    #EM2.move(360, 50)
    EM2.set_speed(-1 * mps_to_rpm(distance_and_time_to_speed(angle_to_distance(90,0.5),0.5))) #turn 90 cw degree+
    time.sleep(0.5)
    EM1.set_speed(mps_to_rpm(distance_and_time_to_speed(0.26,1))) #moves foward 26 cm
    EM2.set_speed(-1 * mps_to_rpm(distance_and_time_to_speed(0.26,1)))
    time.sleep(1)
    EM1.set_speed(0)
    EM2.set_speed(-1 * mps_to_rpm(distance_and_time_to_speed(angle_to_distance(90,0.5),0.5))) #turn -90 degree+
    time.sleep(0.5)
    #put the hand up
    power_expand_board.set_power("DC7", -1 * 10) # Flag
    hand_mover(0,100,100)
    time.sleep(1)
    hand_mover(0,0,0)
    time.sleep(4)
    power_expand_board.set__power("DC7",-2)
    EM1.set_speed(mps_to_rpm(distance_and_time_to_speed(1.80,5))) #moves foward 26 cm
    EM2.set_speed(-1 * mps_to_rpm(distance_and_time_to_speed(1.80,5)))
    time.sleep(5)
    EM1.set_speed(0) #moves foward 26 cm
    EM2.set_speed(0)
    EM2.set_speed(-1 * mps_to_rpm(distance_and_time_to_speed(angle_to_distance(90,0.5),0.5))) #turn 90 cw degree+
    time.sleep(0.5)

def AutomaticMode():
    """25: 15cm/sec
    50: 30cm/sec
    100: 60cm/sec
    Based on NETtoSan's calculations."""
    EM1.set_speed(0)
    EM2.set_speed(mps_to_rpm(distance_and_time_to_speed(angle_to_distance(17.39,0.5),0.5))) #turn 17.39 degree+
    #BotMover('R',mps_to_rpm(distance_and_time_to_speed(angle_to_distance(17.39),0.5)))
    time.sleep(0.5)
    EM1.set_speed(mps_to_rpm(distance_and_time_to_speed(0.87,1))) #moves foward 87 cm
    EM2.set_speed(mps_to_rpm(distance_and_time_to_speed(0.87,1)))
    #BotMover('U',)
    time.sleep(1)
    EM3.set_speed(90)
    power_expand_board.set_power("DC3", 100)
    time.sleep(5)
    EM3.set_power(-0)
    power_expand_board.set_power("DC3", -0)
    EM1.set_speed(mps_to_rpm(distance_and_time_to_speed(angle_to_distance(17.39,0.5),0.125)))
    EM2.set_speed(0)
    time.sleep(0.125)
    #EM1.set_speed(-1*mps_to_rpm(distance_and_time_to_speed(0.25,1)))
    #EM2.set_speed(-1*mps_to_rpm(distance_and_time_to_speed(0.25,1)))
    #time.sleep(1)
    EM1.set_speed(mps_to_rpm(distance_and_time_to_speed(angle_to_distance(17.39,0.5),0.125)))
    time.sleep(0.125)
    EM1.set_speed(-1*mps_to_rpm(distance_and_time_to_speed(0.10,1)))
    EM2.set_speed(-1*mps_to_rpm(distance_and_time_to_speed(0.10,1)))
    time.sleep(1)
    EM1.set_speed(0)
    EM2.set_speed(mps_to_rpm(distance_and_time_to_speed(angle_to_distance(17.39,0.5),0.5))) #turn 17.39 degree+
    #BotMover('R',mps_to_rpm(distance_and_time_to_speed(angle_to_distance(17.39),0.5)))
    time.sleep(0.5)
    EM3.set_power(90)
    power_expand_board.set_power("DC3", 100)
    power_expand_board.set_power("BL1", BP)
    power_expand_board.set_power("BL2", BP)
    
    '''
    #smaller triangle here
    #large triangle below
    for i in range(-10,45,5): # roughly a triangle (18 cycles) 
        mybppower = velocity_to_power(vel_from_angle_distance(i,3.96))
        power_expand_board.set_power("BL1", mybppower)
        power_expand_board.set_power("BL2", mybppower)
        time.sleep(1)
        EM1.set_speed(mps_to_rpm(distance_and_time_to_speed(angle_to_distance(17.39),0.5))) # CHANGE HERE!
        #BotMover() # Reset
    '''

def ShooterModule_N(Mode):
    global BP, brushless
    # Mode 0: Manual Hold
    # Mode 1: Toggle Shoot
    '''
    if Mode == 0:
        power_expand_board.set_power("BL1", BP)
        power_expand_board.set_power("BL2", BP)
        #power_expand_board.set_power("DC3", -50)
        while not not gamepad.is_key_pressed(ShootHD):
            pass

        power_expand_board.stop("BL1")
        power_expand_board.stop("BL2")
        #power_expand_board.stop("DC3")
    '''
    if Mode == 1:
        if brushless == 0:
            brushless = 1

        else:
            brushless = 0
            #power_expand_board.stop("DC3")

        while not not gamepad.is_key_pressed(ShootTG):
            pass

        while not not gamepad.is_key_pressed(ShootHD):
            pass

def MoveModule():
    EM1.set_power(0.8*(gamepad.get_joystick("Ly")+(gamepad.get_joystick("Lx")))*inverse/1.5)
    EM2.set_power(-0.8*(gamepad.get_joystick("Ly")-(gamepad.get_joystick("Lx")))*inverse/1.5)
    
    #rotating a hand 
    hand_mover(gamepad.get_joystick("Rx"),0,0)

    #griping the hand
    #hand_mover(0,gamepad.get_joystick("Ry"),(-1) *gamepad.get_joystick("Ry"))

    power_expand_board.set_power("DC2",gamepad.get_joystick("Ry")*-1)

    if gamepad.is_key_pressed('Left'):
        hand_mover(0,100*10,-100*10)
    if gamepad.is_key_pressed('Right'):
        hand_mover(0,-100*10,100*10)
    

def AutoController_Angle_N_Time_N_Distance_N_Motor_N_Inverse_B (Angle, Time, Distance, Motor, inverse):
    EM1.set_speed(0)
    EM2.set_speed(0)
    localdistance = Distance
    if Angle == 0 :
        EM2.set_speed(mps_to_rpm(distance_and_time_to_speed(Distance,Time)))
        EM1.set_speed(-1 * mps_to_rpm(distance_and_time_to_speed(Distance,Time)))
        time.sleep(float(Time))
        EM1.set_speed(0)
        EM2.set_speed(0)
    else :
        if not Angle == 0:
            localdistance = (Angle / 180) * (0.3 * 0.5)

        localspeed = localdistance / Time
        localrpm = (60 * localspeed) / (2 * (3.1452 * 0.029))
        if Motor == 1:
            EM1.set_speed(localrpm)

        if Motor == 2:
            if inverse:
                EM2.set_speed(localrpm * -1)

            else:
                EM2.set_speed(localrpm)

        time.sleep(float(Time))
        EM1.set_speed(0)
        EM2.set_speed(0)

def  Rotate_N_Time_N_ARV_S (Angle, Time, Dir):
    if Dir == 'Left':
        AutoController_Angle_N_Time_N_Distance_N_Motor_N_Inverse_B(Angle, Time, 0, 2, 50 == 50)

    if Dir == 'Right':
        AutoController_Angle_N_Time_N_Distance_N_Motor_N_Inverse_B(Angle, Time, 0, 1, 1 == 50)

def Walk_N_N_B (Distance, Time, Inverse):
    AutoController_Angle_N_Time_N_Distance_N_Motor_N_Inverse_B(0, Time, Distance, 1, Inverse)
    AutoController_Angle_N_Time_N_Distance_N_Motor_N_Inverse_B(0, Time, Distance, 2, Inverse)
    
def testAuto() :
    Rotate_N_Time_N_ARV_S(17.39, 0.5, 'Left')
    Rotate_N_Time_N_ARV_S(-17.39, 0.5, 'Left')
    time.wait(3)
    Walk_N_N_B(1, 1, None)
    Walk_N_N_B(1, 1, True)

# Tests
distance_sensor_1 = ranging_sensor_class("PORT3", "INDEX1")


ranging_value = 0
steps = 0
origin_angle = 0

def movevl(v1,v2):
    EM3.set_power(v1)
    EM1.set_power(-v2)

def autoshoot():
    global ranging_value, steps, origin_angle
    power_expand_board.set_power("DC1",-100)

    time.sleep(1)
    movevl(-50,50)
    time.sleep(0.25)     
    movevl(50,50)
    time.sleep(0.6)
    movevl(50,-50)
    time.sleep(0.35)
    movevl(50,50)
    time.sleep(0.7)
    movevl(0,0)
    
    # SHOOT BALL . WAIT BALL TO GET NEAR RANGING SENSOR
    while steps < 5: #ranging_value is 0:

        ranging_value = float(distance_sensor_1.get_distance())
        if ranging_value < 10:
            power_expand_board.set_power("BL1",100)
            power_expand_board.set_power("BL2",100)
            EM2.set_power(-100)
            time.sleep(2)
            movevl(-50,50)
            time.sleep(0.15)
            movevl(0,0)
        else:
            EM2.set_power(-50)
            power_expand_board.set_power("BL1",0)
            power_expand_board.set_power("BL2",0)

    #power_expand_board.set_power("BL1", 0)
    #power_expand_board.set_power("BL2", 0)
    #power_expand_board.stop("DC1")
    #EM2.set_power(0)



def autoshootdemo (): # LEFT

    time.sleep(0.001)
    Rotate_N_Time_N_ARV_S(17.39, 0.5, 'Left')
    Walk_N_N_B(0.87, 1, None)
    power_expand_board.set_power("DC3", 100)
    EM3.set_power(-100)
    time.sleep(2)
    power_expand_board.set_power("DC3", 0)
    EM3.set_power(0)
    Rotate_N_Time_N_ARV_S(-17.39, 0.5, 'Left')
    Walk_N_N_B(-0.1, 0.5, None)
    # start
    Rotate_N_Time_N_ARV_S(-5.19, 0.5, 'Left')
    EM3.set_power(-100)
    power_expand_board.set_power("BL1", velocity_to_power(vel_from_angle_distance(5.19,291.5)))
    power_expand_board.set_power("BL2", velocity_to_power(vel_from_angle_distance(5.19,291.5)))
    # start (STABLE)
    Rotate_N_Time_N_ARV_S(5.19, 0.5, 'Left')

    Walk_N_N_B(0.1, 0.5, None)
    power_expand_board.set_power("BL1", 0)
    power_expand_board.set_power("BL2", 0)
    power_expand_board.set_power("DC3", 100)
    EM3.set_power(-100)
    time.sleep(2)
    power_expand_board.set_power("DC3", 0)
    EM3.set_power(0)
    Walk_N_N_B(-0.1, 0.5, None)
    # start
    Rotate_N_Time_N_ARV_S(5.19, 0.5, 'Left')
    EM3.set_power(-100)
    power_expand_board.set_power("BL1", velocity_to_power(vel_from_angle_distance(5.19,291.5)))
    power_expand_board.set_power("BL2", velocity_to_power(vel_from_angle_distance(5.19,291.5)))
    # start (STABLE)
    Rotate_N_Time_N_ARV_S(-5.19, 0.5, 'Left')
    Walk_N_N_B(0.1, 0.5, None)
    power_expand_board.set_power("BL1", 0)
    power_expand_board.set_power("BL2", 0)
    power_expand_board.set_power("DC3", 100)
    EM3.set_power(-100)
    time.sleep(2)
    power_expand_board.set_power("DC3", 0)
    EM3.set_power(0)
    Walk_N_N_B(-0.1, 0.5, None)
    # start
    Rotate_N_Time_N_ARV_S(12.97, 0.5, 'Left')
    EM3.set_power(-100)
    power_expand_board.set_power("BL1", velocity_to_power(vel_from_angle_distance(12.97,291.5)))
    power_expand_board.set_power("BL2", velocity_to_power(vel_from_angle_distance(12.97,291.5)))
    # start (STABLE)
    Rotate_N_Time_N_ARV_S(-12.97, 0.5, 'Left')
    Walk_N_N_B(0.1, 0.5, None)
    power_expand_board.set_power("BL1", 0)
    power_expand_board.set_power("BL2", 0)
    power_expand_board.set_power("DC3", 100)
    EM3.set_power(-100)
    time.sleep(2)
    power_expand_board.set_power("DC3", 0)
    EM3.set_power(0)
    Walk_N_N_B(-0.1, 0.5, None)
    # start
    Rotate_N_Time_N_ARV_S(23.87, 0.5, 'Left')
    EM3.set_power(-100)
    power_expand_board.set_power("BL1", velocity_to_power(vel_from_angle_distance(23.87,291.5)))
    power_expand_board.set_power("BL2", velocity_to_power(vel_from_angle_distance(23.87,291.5)))
    # start (STABLE)
    Rotate_N_Time_N_ARV_S(-23.87, 0.5, 'Left')
    Walk_N_N_B(0.1, 0.5, None)
    power_expand_board.set_power("BL1", 0)
    power_expand_board.set_power("BL2", 0)
    power_expand_board.set_power("DC3", 100)
    EM3.set_power(-100)
    time.sleep(2)
    power_expand_board.set_power("DC3", 0)
    EM3.set_power(0)
    Walk_N_N_B(-0.1, 0.5, None)
    # start
    Rotate_N_Time_N_ARV_S(31.22, 0.5, 'Left')
    EM3.set_power(-100)
    power_expand_board.set_power("BL1", velocity_to_power(vel_from_angle_distance(31.22,291.5)))
    power_expand_board.set_power("BL2", velocity_to_power(vel_from_angle_distance(31.22,291.5)))
    # start (STABLE)
    Rotate_N_Time_N_ARV_S(-31.22, 0.5, 'Left')
    Walk_N_N_B(0.1, 0.5, None)
    power_expand_board.set_power("BL1", 0)
    power_expand_board.set_power("BL2", 0)
    power_expand_board.set_power("DC3", 100)
    EM3.set_power(-100)
    time.sleep(2)
    power_expand_board.set_power("DC3", 0)
    EM3.set_power(0)
    Walk_N_N_B(-0.1, 0.5, None)
    # start
    Rotate_N_Time_N_ARV_S(38.87, 0.5, 'Left')
    EM3.set_power(-100)
    power_expand_board.set_power("BL1", velocity_to_power(vel_from_angle_distance(38.87,291.5)))
    power_expand_board.set_power("BL2", velocity_to_power(vel_from_angle_distance(38.87,291.5)))
    # start (STABLE)
    Rotate_N_Time_N_ARV_S(-38.87, 0.5, 'Left')
    Walk_N_N_B(0.1, 0.5, None)




# ================= Main Program ===================== #

while True:

    time.sleep(0.001)
    MoveModule()
    power_expand_board.set_power("DC7", -1 * (gamepad.get_joystick("Rx") / 10)) # Flag
    if gamepad.is_key_pressed(RotateR): # Rotate Bot Right
        while not not gamepad.is_key_pressed(RotateR):
            EM1.set_power(45)
            EM2.set_power(45)

        EM1.set_power(0)
        EM2.set_power(0)
    '''
    if gamepad.is_key_pressed(ShootHD): # Toggle Shoot (High)
        BP = 40
        ShooterModule_N(1)
    '''
    if gamepad.is_key_pressed(RotateL): # Rotate Bot Left
        while not not gamepad.is_key_pressed(RotateL):
            time.sleep(0.001)
            EM1.set_power(-45)
            EM2.set_power(-45)

        EM1.set_power(0)
        EM2.set_power(0)

    if gamepad.is_key_pressed(ShootTG): # Toggle Shoot (Low)
        ShooterModule_N(1)
        

    if gamepad.is_key_pressed(BPUp): # Brushless power up
        if BP == 25:
            BP = 40
        while not not gamepad.is_key_pressed(BPUp):
            pass

    if gamepad.is_key_pressed(BPDown): # Brushless power down
        if BP == 40:
            BP = 25
        while not not gamepad.is_key_pressed(BPDown):
            pass
   
    if gamepad.is_key_pressed(BallBeltTG): # Ball Belt Clockwise <Toggle>
        time.sleep(0.001)
        FlowModule(1)
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
    
    if gamepad.is_key_pressed('N3'): # Rotate Bot Left
        while not not gamepad.is_key_pressed('N3'):
            time.sleep(0.001)
            EM3.set_power(inverse2*100)
        EM3.set_power(0)

    if flow == 1:
            power_expand_board.set_power("DC3", inverse2*100)
    else:
        power_expand_board.set_power("DC3", 0)

    if brushless == 1:
        power_expand_board.set_power("BL1", BP)
        power_expand_board.set_power("BL2", BP)
        #power_expand_board.set_power("DC3", -100)

    else:
        power_expand_board.stop("BL1")
        power_expand_board.stop("BL2")