import mbuild_modules.starter_shield as starter_shield
import time
import event
import cyberpi
import gamepad
import mbot2

select_mission = 0
TotalMission = 0
RunningMission = 0
motor_left = 0
motor_right = 0
TurningTheta = 0
MODE = 0
LCSPEED = 0
arm_y = 0

default_speed = 50
default_runtime = "null"
second_msfactor = 1000


def forward(speed=default_speed, run_time=default_runtime, accel_time=1, decel_time=1):
    if speed == 0:
        mbot2.EM_stop("all")
    else:
        if run_time == 0:
            run_time = 0.001
        if run_time == default_runtime:
            run_time = 0
        if not isinstance(run_time, (int, float)):
            return
        run_time = int(run_time * second_msfactor)
        starter_shield.car_spd_mode_forward(
            speed, run_time, accel_time, decel_time)


def backward(speed=default_speed, run_time=default_runtime, accel_time=1, decel_time=1):
    if speed == 0:
        mbot2.EM_stop("all")
    else:
        if run_time == 0:
            run_time = 0.001
        if run_time == default_runtime:
            run_time = 0
        if not isinstance(run_time, (int, float)):
            return
        run_time = int(run_time * second_msfactor)
        starter_shield.car_spd_mode_backward(
            speed, run_time, accel_time, decel_time)


def turn_left(speed=default_speed, run_time=default_runtime, accel_time=1, decel_time=1):
    if speed == 0:
        mbot2.EM_stop("all")
    else:
        if run_time == 0:
            run_time = 0.001
        if run_time == default_runtime:
            run_time = 0
        if not isinstance(run_time, (int, float)):
            return
        run_time = int(run_time * second_msfactor)
        starter_shield.car_spd_mode_turn_left(
            speed, run_time, accel_time, decel_time)


def turn_right(speed=default_speed, run_time=default_runtime, accel_time=1, decel_time=1):
    if speed == 0:
        mbot2.EM_stop("all")
    else:
        if run_time == 0:
            run_time = 0.001
        if run_time == default_runtime:
            run_time = 0
        if not isinstance(run_time, (int, float)):
            return
        run_time = int(run_time * second_msfactor)
        starter_shield.car_spd_mode_turn_right(
            speed, run_time, accel_time, decel_time)


def EM_set_speed(speed=default_speed, port="all"):
    if port not in [0, 1, 2, "all", "ALL", "em1", "em2", "EM1", "EM2"]:
        return
    if speed == 0:
        mbot2.EM_stop(port)
    else:
        if port == "all" or port == "ALL":
            port = 0
        if port == "em1" or port == "EM1":
            port = 1
        if port == "em2" or port == "EM2":
            port = 2
        starter_shield.encoder_motor_set_speed(port, speed)


def drive_speed(EM1_speed=default_speed, EM2_speed=default_speed, run_time=default_runtime, accel_time=1, decel_time=1):
    if run_time == 0:
        run_time = 0.001
    if run_time == default_runtime:
        run_time = 0
    if not isinstance(run_time, (int, float)):
        return
    run_time = int(run_time * second_msfactor)
    EM2_speed = -EM2_speed
    if EM1_speed != 0 and EM2_speed != 0:
        starter_shield.car_spd_mode_apiece(
            EM1_speed, EM2_speed, run_time, accel_time, decel_time)
    else:
        if EM1_speed == 0 and EM2_speed == 0:
            mbot2.EM_stop("all")
        elif EM1_speed == 0 and EM2_speed != 0:
            starter_shield.car_spd_mode_apiece(
                EM1_speed, EM2_speed, run_time, accel_time, decel_time)
            mbot2.EM_stop("em1")
        elif EM1_speed != 0 and EM2_speed == 0:
            starter_shield.car_spd_mode_apiece(
                EM1_speed, EM2_speed, run_time, accel_time, decel_time)
            mbot2.EM_stop("em2")


mbot2.forward = forward
mbot2.backward = backward
mbot2.turn_left = turn_left
mbot2.turn_right = turn_right
mbot2.EM_set_speed = EM_set_speed
mbot2.drive_speed = drive_speed


@event.start
def on_start():
    global select_mission, TotalMission, RunningMission, motor_left, motor_right, TurningTheta, MODE, LCSPEED, arm_y
    cyberpi.led.show('red orange yellow green cyan')
    cyberpi.display.rotate_to(-90)
    cyberpi.display.show_label('ST-BUU', 32, "center", index=0)
    time.sleep(1)
    cyberpi.display.show_label(
        str(cyberpi.get_battery()) + str('%'), 32, "center", index=0)
    cyberpi.led.on(0, 255, 0, "all")
    time.sleep(1)
    cyberpi.led.on(0, 0, 0, "all")
    cyberpi.console.clear()
    Manual()


def LoadMe():
    global select_mission, TotalMission, RunningMission, motor_left, motor_right, TurningTheta, MODE, LCSPEED, arm_y
    select_mission = 0
    TotalMission = 5
    cyberpi.display.show_label('ready to start', 32, "center", index=0)


def Manual():
    global select_mission, TotalMission, RunningMission, motor_left, motor_right, TurningTheta, MODE, LCSPEED, arm_y
    while True:
        mbot2.drive_power(0.8 * ((gamepad.get_joystick('Ly') + gamepad.get_joystick('Lx'))
                                 ), -0.8 * ((gamepad.get_joystick('Ly') - gamepad.get_joystick('Lx'))))
        arm_y = gamepad.get_joystick('Ry')
        mbot2.servo_set(arm_y, "S3")
        if gamepad.is_key_pressed('Up'):
            mbot2.forward(20)
            while not not gamepad.is_key_pressed('Up'):
                pass

        if gamepad.is_key_pressed('Down'):
            mbot2.backward(20)
            while not not gamepad.is_key_pressed('Down'):
                pass

        if gamepad.is_key_pressed('Left'):
            mbot2.turn_left(20)
            while not not gamepad.is_key_pressed('Left'):
                pass

        if gamepad.is_key_pressed('Right'):
            mbot2.turn_right(20)
            while not not gamepad.is_key_pressed('Right'):
                pass

        if gamepad.is_key_pressed('N1'):
            pass

        if gamepad.is_key_pressed('N4'):
            pass

        if gamepad.is_key_pressed('N2'):
            mbot2.servo_set(180, "S3")
            time.sleep(0.4)
            mbot2.servo_set(50, "S2")
            mbot2.servo_set(120, "S1")

        if gamepad.is_key_pressed('N3'):
            mbot2.servo_set(arm_y + 15, "S3")
            time.sleep(1)
            mbot2.drive_power(50, -50)
            mbot2.servo_set(110, "S2")
            mbot2.servo_set(60, "S1")

        if gamepad.is_key_pressed('R1'):
            mbot2.motor_set(30, "M1")
            time.sleep(1)
            mbot2.motor_set(0, "M1")
            time.sleep(0.2)
            mbot2.servo_set(0, "S4")
            time.sleep(0.5)
            mbot2.motor_set(-30, "M1")
            time.sleep(0.5)
            mbot2.motor_set(0, "M1")
            time.sleep(0.25)
            mbot2.servo_set(180, "S4")

        if gamepad.is_key_pressed('L1'):
            mbot2.servo_set(110, "S2")
            mbot2.servo_set(60, "S1")

        if gamepad.is_key_pressed('L2'):
            mbot2.servo_set(80, "S3")

        if gamepad.is_key_pressed('R2'):
            mbot2.servo_set(100, "S3")
