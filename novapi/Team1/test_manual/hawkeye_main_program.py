################################################
 #         A HOLONOMIC MECANUM SOLUTIONS        # 
 # - (C) 2023, NETtoSan                         #
 # - Thai Nichi Institute of Technology         #
 # This is to provide a solutions in which to   #
 # drive mecanum wheel with holonomic aspects   #
 # This is made suitable for odometry purposes  #
 ################################################
 
 # PS:1 This code is for MakeX Challenge 2023


from mbuild.encoder_motor import encoder_motor_class
from mbuild.smart_camera import smart_camera_class
from mbuild import gamepad
import math
import novapi
from mbuild.ranging_sensor import ranging_sensor_class
from mbuild import power_expand_board
from mbuild.smartservo import smartservo_class
from mbuild.dual_rgb_sensor import dual_rgb_sensor_class
from mbuild.ultrasonic_sensor import ultrasonic_sensor_class
import mbuild

encode_fl = encoder_motor_class("M1", "INDEX1")
encode_fr = encoder_motor_class("M2", "INDEX1")
encode_rl = encoder_motor_class("M3", "INDEX1")
encode_rr = encoder_motor_class("M4", "INDEX1")

# Test functions #
smart_cam = smart_camera_class("PORT5", "INDEX1")
smart_cam.set_mode("color")
rot_spd = 0
track = False

kp = 0
ki = 0
kd = 0
ks = 0
novapi_travelled_x = 0
novapi_travelled_y = 0
def backgroundProcess():
    tws.lock_target(1)
    updatePosition()

# Test functions #

# Built functions to conpensate missing python functions
def isneg(v):
    return False if v > 0 else False if v == 0 else True

def constrain(v, mn, mx):
    if v < mn : return mn
    if v > mx : return mx
    return v
    
# Class
class tws:
    def lock_target(signature):
        global rot_spd
        if smart_cam.detect_sign(signature):
            rot_spd = ( smart_cam.get_sign_x(signature) - 160 ) * -0.5
        else:
            rot_spd = 0 
    
    def find_target(signature):
        pass

    def find_target_x(signature):
        pass

class motors:
    def drive(v1, v2, v3, v4):
        encode_fl.set_power(v1)
        encode_fr.set_power(v2)
        encode_rl.set_power(v3)
        encode_rr.set_power(v4)

    def throttle_curve(v, s, e):
        return s * (v ** e)
        
    # Find relative path
    def pure_persuit(x, y, rot, auto:bool):
        starting_angle = 90  # novapi.get_rot("Y")
        dX = (-1 * x * 0.3)
        dY = (y * 0.3)
        rX = rot

        target_angle =  starting_angle - math.degrees(math.atan2(dY , dX))
        power = constrain(motors.throttle_curve(math.sqrt((dX * dX) + (dY * dY)), 0.005, 2) * 10, -100, 100)
        
        # Automatic stage
        if auto == True:
            dX = (-1 * x * 0.3) - novapi_travelled_x
            dY = (y * 0.3) - novapi_travelled_y
            rX = 0

            target_angle =  starting_angle - math.degrees(math.atan2(dY , dX))
            power = constrain(motors.throttle_curve(math.sqrt((dX * dX) + (dY * dY)), 0.005, 2) * 10, -100, 100)

            if novapi_travelled_x < x:
                while novapi_travelled_x < x:
                    novapi_travelled_x += novapi.get_acceleration("x")
                    motors.holonomic(power, [target_angle, dX, dY], rx)
            elif novapi_travelled_x > x:
                while novapi_travelled_x > x:
                    novapi_travelled_x += novapi.get_acceleration("x")
                    motors.holonomic(power, [target_angle, dX, dY], rx)

            motors.drive(0,0,0,0)
        else:
            motors.holonomic(power, [target_angle, dX, dY], rX)

    # Calculate each motor power to travel
    def holonomic(power, packet, rot_speed): # Use this for auto code!

        #power = power/10
        packet[0] = (packet[0] + 180) % 360 - 180
        angle_rad = math.radians(- packet[0])

        vx = round(power * math.cos(angle_rad))
        vy = round(power * math.sin(angle_rad))

        EFl =   constrain((vx - vy) - rot_speed, -100, 100)
        EFr = - constrain((vx + vy) + rot_speed, -100, 100)
        ERl =   constrain((vx + vy) - rot_speed, -100, 100)
        ERr = - constrain((vx - vy) + rot_speed, -100, 100)

        motors.drive(EFl, EFr, ERl, ERr)

# Functions
def updatePosition():
    global novapi_travelled_x, novapi_travelled_y
    novapi_travelled_x += novapi.get_acceleration("x")
    novapi_travelled_y += novapi.get_acceleration("y")

def auto():
    pass

def manual():
    global rot_spd, track
    backgroundProcess()

    x = gamepad.get_joystick("Lx")
    y = gamepad.get_joystick("Ly")
    rot = motors.throttle_curve(gamepad.get_joystick("Rx"), 0.0001, 3)

    if gamepad.is_key_pressed("≡"):
        if track == False:
            track = True
        else:
            track = False
        while not not gamepad.is_key_pressed("≡"):
            pass

    if track == True:
        rot = rot_spd
    else:
        pass

    motors.pure_persuit(x, y, rot, False)

class en_motor:
    def __init__(self, port):
        self.port = port #กำหนด port ของ encode motor
    def hold(self, hold_default_speed, hold_speed, hold_key): #( ความเร็วเริ่มต้นของมอเตอร์, ความเร็วมอเตอร์เป็นตัวเลข ,  ปุ่มที่ใช้กดค้าง ) เช่น (0, 100, "N1")
        encoder_motor = encoder_motor_class(self.port, "INDEX1")
        if gamepad.is_key_pressed(hold_key): #กดค้าง
            encoder_motor.set_power(hold_speed)
        else:
            encoder_motor.set_power(hold_default_speed)
            pass
    def double_hold(self, double_hold_default_speed, double_speed, double_hold_key_1, double_hold_key_2): #( ความเร็วเริ่มต้นของมอเตอร์, ความเร็วมอเตอร์2ทิศเป็น list, ปุ่มที่ใช้กดค้างทิศที่1, ปุ่มที่ใช้กดค้างทิศที่2 ) เช่น (0, [-100, 100], "N1", "N2")
        encoder_motor = encoder_motor_class(self.port, "INDEX1")
        if gamepad.is_key_pressed(double_hold_key_1):
            encoder_motor.set_power(double_speed[0])
        elif gamepad.is_key_pressed(double_hold_key_2):
            encoder_motor.set_power(double_speed[1])
        else:
            encoder_motor.set_power(double_hold_default_speed)
#ส่วนของ dc motor
class dc_motor:
    #ใส่ port ของ dc motor
    #เช่น "DC1"
    def __init__(self, port):
        self.port = port #กำหนด port ของ dc motor
    #กดเปิดปิด
    mode_for_toggle = 0 #ตัวระบุตำแหน่งของสมาชิกใน list
    def toggle(self, toggle_speed, toggle_key): #รับค่า ( ความเร็วมอเตอร์เป็น list สมาชิก 2ตัว,  ปุ่มที่ใช้กดเปิดปิด ) เช่น ([0, -100], "N1")
        if gamepad.is_key_pressed(toggle_key): #กดเปิดปิดโดย สลับค่าตำแหน่งใน list
            if self.mode_for_toggle == 0:
                self.mode_for_toggle = 1
            else:
                self.mode_for_toggle = 0
            while gamepad.is_key_pressed(toggle_key):
                pass
        else:
            pass
        power_expand_board.set_power(self.port, toggle_speed[self.mode_for_toggle]) #run มอเตอร์
    #กดเปิดปิดเปลี่ยนทิศ
    mode_for_double_toggle = {
        "switch": 0,
        "speed": 0
    }
    def double_toggle(self, double_toggle_speed, toggle_key_1, toggle_key_2):
        if gamepad.is_key_pressed(toggle_key_1):
            if self.mode_for_double_toggle["switch"] == 0:
                self.mode_for_double_toggle["switch"] = 1
            else:
                self.mode_for_double_toggle["switch"] = 0
            while gamepad.is_key_pressed(toggle_key_1):
                pass
        else:
            pass
        if gamepad.is_key_pressed(toggle_key_2):
            if self.mode_for_double_toggle["speed"] == 0:
                self.mode_for_double_toggle["speed"] = 1
            else:
                self.mode_for_double_toggle["speed"] = 0
            while gamepad.is_key_pressed(toggle_key_2):
                pass
        else:
            pass
        if self.mode_for_double_toggle["switch"] == 1:
            power_expand_board.set_power(self.port, double_toggle_speed[self.mode_for_double_toggle["speed"]])
        else:
            self.mode_for_double_toggle["speed"] = 0
            power_expand_board.set_power(self.port, 0)
    #กดค้างเปิดปิด
    def hold(self, hold_default_speed, hold_speed, hold_key): #( ความเร็วเริ่มต้นของมอเตอร์, ความเร็วมอเตอร์เป็นตัวเลข ,  ปุ่มที่ใช้กดค้าง ) เช่น (0, 100, "N1")
        if gamepad.is_key_pressed(hold_key): #กดค้าง
            power_expand_board.set_power(self.port, hold_speed) #run ตอเมอเตอร์ 
        else:
            power_expand_board.set_power(self.port, hold_default_speed) #ค่า default ของมอเตอร์
            pass
    #กดค้างเปลี่ยนทิศ
    def double_hold(self, double_hold_default_speed, double_speed, double_hold_key_1, double_hold_key_2): #( ความเร็วเริ่มต้นของมอเตอร์, ความเร็วมอเตอร์2ทิศเป็น list, ปุ่มที่ใช้กดค้างทิศที่1, ปุ่มที่ใช้กดค้างทิศที่2 ) เช่น (0, [-100, 100], "N1", "N2")
        if gamepad.is_key_pressed(double_hold_key_1): #กดค้างหมุนทิศที่1
            power_expand_board.set_power(self.port, double_speed[0])
        elif gamepad.is_key_pressed(double_hold_key_2): #กดค้างหมุนทิศที่ 2
            power_expand_board.set_power(self.port, double_speed[1])
        else:
            power_expand_board.set_power(self.port, double_hold_default_speed) #ค่า default ของมอเตอร์

def bl():
    if gamepad.is_key_pressed("Up"):
        power_expand_board.set_power("BL1", 40)
        power_expand_board.set_power("BL2", 40)
    elif gamepad.is_key_pressed("Down"):
        power_expand_board.set_power("BL1", 18.5)
        power_expand_board.set_power("BL2", 18.5)
    elif gamepad.is_key_pressed("Right"):
        power_expand_board.set_power("BL1", 0)
        power_expand_board.set_power("BL2", 0)
    else:
        pass

def aim():
    encoder_motor_M1 = encoder_motor_class("M1", "INDEX1")
    encoder_motor_M2 = encoder_motor_class("M2", "INDEX1")
    encoder_motor_M3 = encoder_motor_class("M3", "INDEX1")
    encoder_motor_M4 = encoder_motor_class("M4", "INDEX1")
    if gamepad.is_key_pressed("R1"):
        encoder_motor_M1.set_speed(40)
        encoder_motor_M2.set_speed(40)
        encoder_motor_M3.set_speed(40)
        encoder_motor_M4.set_speed(40)
    elif gamepad.is_key_pressed("L1"):
        encoder_motor_M1.set_speed(-40)
        encoder_motor_M2.set_speed(-40)
        encoder_motor_M3.set_speed(-40)
        encoder_motor_M4.set_speed(-40) 
    else:
        pass

smartservo_1 = smartservo_class("M6", "INDEX1")
def arm():
    power_expand_board.set_power("DC2", gamepad.get_joystick("Ry"))
    if gamepad.is_key_pressed("Right"):
        smartservo_1.move(10, 100)
    elif gamepad.is_key_pressed("Left"):
        smartservo_1.move(-10, 100)
    else:
        pass

def shooting():
    manual()
    en_1.double_hold(0, [100, -100], "N2", "N3")
    dc_1.toggle([0, 60], "N4")
    bl()
    aim()

def grip():
    manual()
    aim()
    arm()

en_1 = en_motor("M5")
dc_1 = dc_motor("DC1")
mode = 0
while True:
    if gamepad.is_key_pressed("+"):
        if mode == 0:
            mode = 1
        elif mode == 1:
            mode = 0
        else:
            pass
        while gamepad.is_key_pressed("+"):
            pass
    else:
        pass
    if mode == 0:
        shooting()
    elif mode == 1:
        grip()
    else:
        pass