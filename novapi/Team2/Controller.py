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
EM1 = encoder_motor_class("M1", "INDEX1")
EM2 = encoder_motor_class("M2", "INDEX1")
EM3 = encoder_motor_class("M3", "INDEX1")
EM4 = encoder_motor_class("M4", "INDEX1")

SERVO1 = smartservo_class("M1", "INDEX1")
SERVO2 = smartservo_class("M2", "INDEX1")
SERVO3 = smartservo_class("M3", "INDEX1")
SERVO4 = smartservo_class("M4", "INDEX2")
SERVO5 = smartservo_class("M6", "INDEX1")
SERVO6 = smartservo_class("M6", "INDEX2")

def MoveModule(Mode):
    global BP, SP
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
        EM1.set_power(maxspeedi * ((gamepad.get_joystick("Ly") - ((Fl + drift)))))
        EM2.set_power((-1 * maxspeedi) * ((gamepad.get_joystick("Ly") + ((Fr - drift)))))
        EM3.set_power(maxspeedi * ((gamepad.get_joystick("Ly") + ((Rl + drift)))))
        EM4.set_power((-1 * maxspeedi) * ((gamepad.get_joystick("Ly") - ((Rr - drift)))))

    if Mode == 90:
        EM1.set_power(maxspeedi * ((gamepad.get_joystick("Ly") + 0)))
        EM2.set_power((-1 * maxspeedi) * ((gamepad.get_joystick("Lx") + 0)))
        EM3.set_power(maxspeedi * ((gamepad.get_joystick("Lx") + 0)))
        EM4.set_power((-1 * maxspeedi) * ((gamepad.get_joystick("Ly") + 0)))

    if Mode == 180:
        EM1.set_power(maxspeedi * ((gamepad.get_joystick("Ly") - ((Rl - drift)))))
        EM2.set_power((-1 * maxspeedi) * ((gamepad.get_joystick("Ly") + ((Rr + drift)))))
        EM3.set_power(maxspeedi * ((gamepad.get_joystick("Ly") + ((Fl - drift)))))
        EM4.set_power((-1 * maxspeedi) * ((gamepad.get_joystick("Ly") - ((Fr + drift)))))

    # Safe servo angle
    # =============
    # if not exceed 180; move!
    # ! FIX THIS LATER !
    safetyangle = (gamepad.get_joystick("Ry") * 0.15 + SERVO6.get_value("angle"))
    SERVO6.move(gamepad.get_joystick("Ry") * 0.15, 30)

def FlowModule():
    global flow
    if flow == 0:
        flow = 1

    else:
        flow = 0

    if flow == 1:
        power_expand_board.set_power("DC1", -100)
        power_expand_board.set_power("DC2", 100)

    else:
        power_expand_board.stop("DC1")
        power_expand_board.stop("DC2")

    while not not gamepad.is_key_pressed("N4"):
        pass

def Mover(W1, W2, W3, W4):
    EM1.set_power(W1)
    EM1.set_power(W2)
    EM1.set_power(W3)
    EM1.set_power(W4)

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
        power_expand_board.set_power("DC3", -50)
        while not not gamepad.is_key_pressed("R2"):
            pass

        power_expand_board.stop("BL1")
        power_expand_board.stop("BL2")
        power_expand_board.stop("DC3")

    else:
        if brushless == 0:
            brushless = 1

        else:
            brushless = 0

        if brushless == 1:
            power_expand_board.set_power("BL1", BP)
            power_expand_board.set_power("BL2", BP)
            power_expand_board.set_power("DC3", -100)

        else:
            power_expand_board.stop("BL1")
            power_expand_board.stop("BL2")
            power_expand_board.stop("DC3")

        while not not gamepad.is_key_pressed("L2"):
            pass

while True:
    time.sleep(0.001)
    MoveModule(180)
    power_expand_board.set_power("DC7", -1 * (gamepad.get_joystick("Rx") / 10))
    if gamepad.is_key_pressed("N4"):
        FlowModule()

    if gamepad.is_key_pressed("R1"):
        while not (not gamepad.is_key_pressed("R1")):
            time.sleep(0.001)
            BotMover('R', 100)

        BotMover('N', 0)

    if gamepad.is_key_pressed("R2"):
        # Hold And Shoot
        ShooterModule_N(0)

    if gamepad.is_key_pressed("L1"):
        while not (not gamepad.is_key_pressed("L1")):
            time.sleep(0.001)
            BotMover('L', 100)

        BotMover('N', 0)

    if gamepad.is_key_pressed("L2"):
        # Toggle Shoot
        ShooterModule_N(1)

    if gamepad.is_key_pressed("Up"):
        SERVO5.move(30, 30)

    if gamepad.is_key_pressed("Down"):
        SERVO5.move(-30, 30)

    if gamepad.is_key_pressed("Left"):
        power_expand_board.set_power("DC8", -50)
        while not not gamepad.is_key_pressed("Left"):
            pass

    if gamepad.is_key_pressed("Right"):
        power_expand_board.set_power("DC8", 50)
        while not not gamepad.is_key_pressed("Right"):
            pass
        power_expand_board.stop("DC8")

    if gamepad.is_key_pressed("N1"):
        if automatic_mode == 1:
            automatic_mode = 0
            AutomaticMode()