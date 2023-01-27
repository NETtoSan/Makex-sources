# codes make you happy
import novapi
import time
from mbuild.smart_camera import smart_camera_class
from mbuild.encoder_motor import encoder_motor_class
from mbuild.ranging_sensor import ranging_sensor_class

# new class
smart_camera_1 = smart_camera_class("PORT2", "INDEX1")
encoder_motor_M1 = encoder_motor_class("M1", "INDEX1")
encoder_motor_M2 = encoder_motor_class("M2", "INDEX1")
encoder_motor_M3 = encoder_motor_class("M3", "INDEX1")
encoder_motor_M4 = encoder_motor_class("M4", "INDEX1")

ranging_sensor_1 = ranging_sensor_class("PORT1", "INDEX1")

smart_camera_1.set_mode("color")

def drive(v1,v2,v3,v4):
    encoder_motor_M1.set_power(v1)
    encoder_motor_M2.set_power(v2)
    encoder_motor_M3.set_power(v3)
    encoder_motor_M4.set_power(v4)

def drive_middle():
    ranging_sensor = float(ranging_sensor_1.get_distance())
    while ranging_sensor > 10:
        drive(50, -50, 50, -50)
        ranging_sensor = float(ranging_sensor_1.get_distance())
        
    drive(0, 0, 0, 0)

while True:
    time.sleep(0.001)
    if smart_camera_1.detect_sign(1):
        smart_camera_1.close_light()

        if smart_camera_1.detect_sign_location(1, "middle"):
            drive_middle()

        elif smart_camera_1.detect_sign_location(1, "right"):
            drive(50, 50, -50, -50)

        elif smart_camera_1.detect_sign_location(1, "left"):
            drive(-50, -50, 50, 50)
        else:
            drive(0, 0, 0, 0)
    else:
        smart_camera_1.open_light()
        drive(0, 0, 0, 0)