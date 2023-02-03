# codes make you happy
import novapi
import time
from mbuild.smart_camera import smart_camera_class
from mbuild.encoder_motor import encoder_motor_class
from mbuild.ranging_sensor import ranging_sensor_class
from mbuild.dual_rgb_sensor import dual_rgb_sensor_class
# new class
smart_camera_1 = smart_camera_class("PORT2", "INDEX1")
encoder_motor_M1 = encoder_motor_class("M1", "INDEX1")
encoder_motor_M2 = encoder_motor_class("M2", "INDEX1")
encoder_motor_M3 = encoder_motor_class("M3", "INDEX1")
encoder_motor_M4 = encoder_motor_class("M4", "INDEX1")

ranging_sensor_1 = ranging_sensor_class("PORT1", "INDEX1")
smart_camera_1.set_mode("color")

auto_spec = {
    "wall_distance": 30,         # Distance between bot and the wall in auto code
    "cube_distance": 5,          # Distance between bot and the cube in auto mode
    "cube_light_intensity": 10,  # Measure distance from the cube when ranging sensor is not available
    "angle_offset": 0,           # Tolerable angle for janky mecanum 
    
    "status_led": ["PORT3","INDEX1"],   # Initiate auto led
    "cube_found": ["STILL", "blue"],     # Status when the cube is found
    "cube_ready": ["STILL", "green"],    # Status when the cube is ready to be grabbed
    "cube_done":  ["FLASH", "green"],    # Status when the cube is on our side
    "cube_gone":  ["FLASH", "red"]       # Status when the cube suddenly disappeared
}
status_led = dual_rgb_sensor_class(auto_spec["status_led"][0], auto_spec["status_led"][1])

def drive(v1,v2,v3,v4):
    encoder_motor_M1.set_power(v1)
    encoder_motor_M2.set_power(v2)
    encoder_motor_M3.set_power(v3)
    encoder_motor_M4.set_power(v4)

def led_status(data):
    if data[0] is "FLASH":
        status_led.set_led_color(data[1])
    elif data[0] is "STILL":
        status_led.set_led_color(data[1])

def drive_middle():
    ranging_sensor = float(ranging_sensor_1.get_distance())
    while ranging_sensor > 10:
        drive(50, -50, 50, -50)
        ranging_sensor = float(ranging_sensor_1.get_distance())
        
    drive(0, 0, 0, 0)


drive(50,-50,50,-50)
time.sleep(1)

while True:
    time.sleep(0.001)
    if smart_camera_1.detect_sign(1):
        smart_camera_1.close_light()

        if smart_camera_1.detect_sign_location(1, "middle"):
            drive_middle()
        if smart_camera_1.detect_sign_location(1, "up"):
            drive_middle()
        if smart_camera_1.detect_sign_location(1, "down"):
            drive_middle()

        elif smart_camera_1.detect_sign_location(1, "right"):
            origin_angle = float(novapi.get_yaw())    #FINISH THIS AT THE LAB!
            current_angle = float(novapi.get_yaw())

            if current_angle is not origin_angle:
                pass

            drive(50, 50, -50, -50)

        elif smart_camera_1.detect_sign_location(1, "left"):
            origin_angle = float(novapi.get_yaw())    #FINISH THIS AT THE LAB!
            current_angle = float(novapi.get_yaw())

            if current_angle is not origin_angle:
                pass

            drive(-50, -50, 50, 50)
        else:
            drive(0, 0, 0, 0)
    else:
        smart_camera_1.open_light()
        led_status(auto_spec["cube_gone"])
        drive(0, 0, 0, 0)