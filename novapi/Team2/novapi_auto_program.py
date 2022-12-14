from mbuild.encoder_motor import encoder_motor_class
from mbuild import power_expand_board
from mbuild.ranging_sensor import ranging_sensor_class
import novapi

EM1 = encoder_motor_class("M1", "INDEX1") # RIGHT MOTOR
EM2 = encoder_motor_class("M2", "INDEX1") # FEED BELT
EM3 = encoder_motor_class("M3", "INDEX1") # LEFT MOTOR

distance_sensor_1 = ranging_sensor_class("PORT3", "INDEX1")


ranging_value = 0
steps = 0
origin_angle = 0 
def movevl(v1,v2):
    EM3.set_power(v1)
    EM1.set_power(-v2)

def autoshoot():
    global ranging_value, steps, origin_angle
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
    while steps < 3: #ranging_value is 0:

        ranging_value = float(distance_sensor_1.get_distance())
        if ranging_value < 10:
            power_expand_board.set_power("BL1",50)
            power_expand_board.set_power("BL2",50)
            EM2.set_power(-100)
            time.sleep(2.5)
            movevl(-50,50)
            time.sleep(0.15)
            movevl(0,0)

            steps += 1
        else:
            EM2.set_power(-50)
            power_expand_board.set_power("BL1",0)
            power_expand_board.set_power("BL2",0)

    power_expand_board.set_power("BL1", 0)
    power_expand_board.set_power("BL2", 0)
    power_expand_board.stop("DC1")
    EM2.set_power(0)

autoshoot()