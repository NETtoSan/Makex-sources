# codes make you happy
from mbuild.encoder_motor import encoder_motor_class
from mbuild.smartservo import smartservo_class
from mbuild.dual_rgb_sensor import dual_rgb_sensor_class
from mbuild import power_expand_board
from mbuild import gamepad
import novapi
import time

# new class
encoder_motor_M1 = encoder_motor_class("M1", "INDEX1")
encoder_motor_M2 = encoder_motor_class("M2", "INDEX1")
#power_expand_board.set_power("BL1", 10)
#power_expand_board.set_power("BL2", 10)

while True:

    if gamepad.is_key_pressed("N3"):
        power_expand_board.set_power("BL1", 10)
        power_expand_board.set_power("BL2", 10)
        while not not gamepad.is_key_pressed("N2"):
            pass
    if gamepad.is_key_pressed("N2"):
        power_expand_board.set_power("BL1", 0)
        power_expand_board.set_power("BL2", 0)
        while not not gamepad.is_key_pressed("N3"):
            pass


    deltaR = 13 # ระยะห่ายของล้อทั้ง ๒ ข้าง
    maxX = 100 # ค่ามากที่สุดเมือ่ลากคันบังคับไปทางขวา
    maxY = 100 # ค่ามากที่สุดเมือ่ลากคันบังคับขึ้นข้างบน
    LX = gamepad.get_joystick("Lx")
    LY = gamepad.get_joystick("Ly")
    speed = math.math.sqrt(LX * LX + LY * LY)/math.sqrt(maxX*maxX + maxY*maxY)
    powerR = 0
    powerL = 0
    r = LY/LX * direction(LY)
    VlVr = (r + deltaR/2)/(r - deltaR/2)

    if abs(VlVr) > 1 :
        powerL = VlVr * 100 * speed * direction(LY)
        powerR = 100 * speed * direction
    else :
        powerR = VlVr * 100 * speed * direction(LY)
        powerL = 100 * speed * direction


    def direction(value) : # หาทิศทางของค่านั้น ๆ (ก็คือหาว่าเป็นบวกหรือลบหรือ ๐)
        if value > 0 :
            return -1
        elif value == 0 :
            return 0
        else :
            return 1

    encoder_motor_M1.set_power(powerL)
    encoder_moter_M2.set_power(powerR)