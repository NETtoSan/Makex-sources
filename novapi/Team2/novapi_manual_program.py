from mbuild.encoder_motor import encoder_motor_class
from mbuild import power_expand_board

EM1 = encoder_motor_class("M1", "INDEX1") # RIGHT MOTOR
EM2 = encoder_motor_class("M2", "INDEX1") # FEED BELT
EM3 = encoder_motor_class("M3", "INDEX1") # LEFT MOTOR





def movevl(v1,v2):
    EM3.set_power(v1)
    EM1.set_power(-v2)

def autoshoot():
    power_expand_board.set_power("DC1", -100)
    EM2.set_power(-100)
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
    time.sleep(5)

    power_expand_board.stop("DC1")
    EM2.set_power(0)

autoshoot()