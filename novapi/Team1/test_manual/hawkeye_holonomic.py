

 ################################################
 #         A HOLONOMIC MECANUM SOLUTIONS        # 
 # - (C) 2023, NETtoSan                         #
 # - Thai Nichi Institute of Technology         #
 # This is to provide a solution in which to    #
 # drive mecanum wheel with holonomic aspects   #
 # This is made suitable for odometry purposes  #
 ################################################
 
 # PS:1 This code DOES NOT provide full challenge bot capabilities
 #      This only supplements necessary function to drive all 4 mecanum wheels
 #      If you need full functionality, please use ./hawkeye_main_program.py
 # PS:2 Rapid holonomic code change may occur. View latest holonomic simulation code via
 #      ../simulator/{pid_test or pure_persuit}.py


from mbuild.encoder_motor import encoder_motor_class
from mbuild.smart_camera import smart_camera_class
from mbuild import gamepad
import math
import novapi

encode_fl = encoder_motor_class("M1", "INDEX1")
encode_fr = encoder_motor_class("M2", "INDEX1")
encode_rl = encoder_motor_class("M3", "INDEX1")
encode_rr = encoder_motor_class("M4", "INDEX1")

# Test functions #
smart_cam = smart_camera_class("PORT5", "INDEX1")
smart_cam.set_mode("color")
rot_spd = 0
track = True

# --- PID --- #
kp = 0
ki = 0
kd = 0
ks = 0
# --- PID --- #

novapi_travelled_x = 0 # Needs to be updated every time. Missing equation!
novapi_travelled_y = 0 # Needs to be updated every time. Missing equation!
# Test functions #

# Built functions to conpensate missing python functions
def isneg(v):
    return False if v > 0 else False if v == 0 else True

def constrain(v, mn, mx):
    if v < mn : return mn
    if v > mx : return mx
    return v

# Background tasks
def updatePosition():
    global novapi_travelled_x, novapi_travelled_y
    novapi_travelled_x += novapi.get_acceleration("x")
    novapi_travelled_y += novapi.get_acceleration("y")

# Class
class track_while_scan:
    def lock_target(signature:int):
        global rot_spd
        if smart_cam.detect_sign(signature):
            rot_spd = ( smart_cam.get_sign_x(signature) - 160 ) * -0.5
        else:
            rot_spd = 0
        
        return rot_spd
    
    # Camera degree thing. Could be useful to lock target with servo
    def get_object_deg(pixel:int):
        v = pixel / track_while_scan.get_cam_ppd(pixel, 65)
        return v 
    def get_cam_ppd(pixel:int, fov_deg:int):
        #ppd = pixel-per-degree
        return pixel / fov_deg
    # Camera degree thing

    # An extra target lock using servos. While using camera to scan for objects
    def find_target(signature:int):
        pass

    def find_target_x(signature:int):
        pass

class motors:
    # Drive all the motors in one go
    def drive(v1:int, v2:int, v3:int, v4:int):
        encode_fl.set_power(v1)
        encode_fr.set_power(v2)
        encode_rl.set_power(v3)
        encode_rr.set_power(v4)
        
    # Calculate motor power using y = x theorem
    def throttle_curve(v:int, s:float, e:int):
        # Using formula y = s * (x-h)^e, but s = a, e = N; N = 2 parabola; N = 3 polynomial
        return s * (v ** e)
    
    # Find relative path
    def pure_persuit(x:int, y:int, rot:int, auto:bool):
        starting_angle = 90  # novapi.get_rot("Y")
        dX = (-1 * x * 0.3)
        dY = (y * 0.3)
        rX = rot

        target_angle =  starting_angle - math.degrees(math.atan2(dY , dX))
        power = constrain(motors.throttle_curve(math.sqrt((dX * dX) + (dY * dY)), 0.005, 2) * 10, -100, 100)
        

        # Automatic stage
        if auto == True:
            motors.holonomic_auto([x,y], starting_angle)
            motors.drive(0,0,0,0)
        else:
            motors.holonomic(power, [target_angle, dX, dY], rX)

    # Necessary for auto code
    def holonomic_auto(coords:list, starting_angle):
        x = coords[0]; y = coords[1]
        dX = (-1 * x * 0.3) - novapi_travelled_x
        dY = (y * 0.3) - novapi_travelled_y
        rX = 0

        ein_auto = True
        target_angle =  starting_angle - math.degrees(math.atan2(dY , dX))
        power = constrain(motors.throttle_curve(math.sqrt((dX * dX) + (dY * dY)), 0.005, 2) * 10, -100, 100)

        if ein_auto == True:
            pass
        else:
            motors.holonomic(0, [0, 0, 0], 0)

    # Calculate each motor power to travel
    def holonomic(power:float, packet:list, rot_speed:int): # Use this for auto code!

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

# Necessary for robot's functionality
class challenge_default:
    def __init__ (self):
        self_mode = "default"
    
    # Background task init
    def backgroundProcess():
        track_while_scan.lock_target(1)
        updatePosition()

    def rot_styles(style, buttons):
        # True -> Button preferences; False -> gamepad.get_joystick("Rx")
        # buttons: 0 = "left side", 1 = "right side"
        v = 0
        if style == True:
            if gamepad.is_key_pressed(buttons[0]):
                v = -100
            if gamepad.is_key_pressed(buttons[1]):
                v = 100

        else:
            v = gamepad.get_joystick("Rx")
        return v
    
    def auto(coords_list:list):

        for coordinate in coords_list:
            motors.pure_persuit(coordinate[0], coordinate[1], 0, True)

    def manual(rot_btns:bool):
        # rot_btns = Use 

        global rot_spd, track
        challenge_default.backgroundProcess()

        x = gamepad.get_joystick("Lx")
        y = gamepad.get_joystick("Ly")
        rot = motors.throttle_curve(challenge_default.rot_styles(rot_btns, ["L1", "R1"]), 0.0001, 3)

        if gamepad.is_key_pressed("N1"):
            if track == False:
                track = True
            else:
                track = False
            while gamepad.is_key_pressed("N1"):
                pass

        if track == True:
            rot = rot_spd

        motors.pure_persuit(x, y, rot, False)
    
    def challenge_runtime():
        use_buttons_for_rot = True
        while True:
            challenge_default.manual(use_buttons_for_rot)

challenge_default.challenge_runtime()