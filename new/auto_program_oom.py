import cyberpi
import time
import gamepad
import mbot2
import event
import mbuild_modules.starter_shield as starter_shield

from cyberpi import *
# Optimize code tonight. Source: ../auto_program_new.py

select_mission = 0
TotalMission = 0
RunningMision = 0
motor_left = 0
motor_right = 0
TurningTheta = 0
MODE = 0
LCSPEED = 0
arm_y = 0
arm_l = 0
arm_r = 0

default_speed = 50
default_runtime = "null"
second_msfactor = 1000

automatic_stage = 1
reaction_preferences = [0, 6]  # Quad RGB, Ultrasonic sensor
programs = ["How", "Auto start left", "Auto start left\nNo cube",
            "Auto start right", "Auto start right\nNo cube", "Manual program (Debugging!)"]


class Auto_Program:
    def __init__(self, sides):
        pass

    def RunCode(sides, cube):
        cyberpi.display.show_label("Auto mode", 16, "center", index=0)
        time.sleep(1)
        speed = 50
        isCube = cube

        # Run straight to the white lines for 1 second
        cyberpi.mbot2.drive_speed(50, -50)
        time.sleep(1)

        # Standby arm
        cyberpi.mbot2.drive_speed(0, 0)
        cyberpi.mbot2.servo_set(120, "S1")
        cyberpi.mbot2.servo_set(60, "S2")
        cyberpi.mbot2.servo_set(0, "S3")

        # Load shooting mechanism
        cyberpi.mbot2.servo_set(0, "S4")
        time.sleep(1)
        cyberpi.mbot2.motor_drive(-30, 0)
        time.sleep(0.25)
        cyberpi.mbot2.motor_drive(0, 0)
        time.sleep(0.5)

        cyberpi.mbot2.servo_set(170, "S4")
        while not cyberpi.controller.is_press("a"):
            if gamepad.is_key_pressed("R2"):
                while not not gamepad.is_key_pressed("R2"):
                    cyberpi.console.clear()
                    cyberpi.display.show_label(
                        "Manual mode", 16, "center", index=0)
                    cyberpi.led.on(255, 255, 0, "all")
                    Manual_Program.ControlMode()
            left_motor = (speed - (0.5 * quad_rgb_sensor.get_offset_track(1)))
            right_motor = -1 * \
                (speed + (0.5 * quad_rgb_sensor.get_offset_track(1)))
            distance = ultrasonic2.get(1)

            # Make an identification logic for distance. Whether it's a cube or a ball. Look at full test program for references
            if distance < 6 and distance != 0:

                cyberpi.mbot2.drive_speed(30, -30)  # slow mbot2 motion
                time.sleep(0.3)
                cyberpi.mbot2.drive_speed(0, 0)  # stop mbot2

                if isCube == True:
                    isCube = False
                    Auto_Program.GrabCube("lea", sides)
                else:
                    Auto_Program.GrabBall("shoot", sides)
            else:
                cyberpi.mbot2.servo_set(120, "S1")  # Left arm
                cyberpi.mbot2.servo_set(60, "S2")  # Right arm
                cyberpi.mbot2.servo_set(0, "S3")  # UD servo
            # Drives motor

            cyberpi.mbot2.drive_speed(left_motor, right_motor)

        cyberpi.mbot2.servo_release("S1")
        cyberpi.mbot2.servo_release("S2")
        cyberpi.mbot2.servo_release("S3")

        cyberpi.led.on(0, 0, 0, "all")
        cyberpi.display.show_label('Quit auto mode', 16, 'center', index=0)
        time.sleep(2)

    def GrabBall(lea, side):
        time.sleep(0.5)
        cyberpi.mbot2.servo_set(60, "S1")  # Left arm
        cyberpi.mbot2.servo_set(120, "S2")  # Right arm

        time.sleep(1)

        #Lift arms up to 0
        cyberpi.mbot2.servo_set(180, "S3")  # UD servo

        #Release arms and release arms back to 135
        time.sleep(0.7)
        cyberpi.mbot2.servo_set(110, "S1")
        cyberpi.mbot2.servo_set(70, "S2")
        time.sleep(1)

        if lea == "shoot":
            if side == "right":
                cyberpi.mbot2.drive_speed(50, 50)
            elif side == "left":
                cyberpi.mbot2.drive_speed(-50, -50)
            time.sleep(1)
            cyberpi.mbot2.drive_speed(0, 0)
            cyberpi.mbot2.drive_speed(-50, 50)
            time.sleep(1.5)
            cyberpi.mbot2.drive_speed(0, 0)

            time.sleep(2)
            Auto_Program.Shoot(side)

            time.sleep(0.5)
            cyberpi.mbot2.drive_speed(50, -50)
            time.sleep(1.5)
            if side == "right":
                cyberpi.mbot2.drive_speed(-50, -50)
            elif side == "left":
                cyberpi.mbot2.drive_speed(50, 50)
            time.sleep(1)
            cyberpi.mbot2.drive_speed(0, 0)

        else:
            pass

    def GrabCube(lea, side):
        #Grab cube
        cyberpi.mbot2.servo_set(60, "S1")
        cyberpi.mbot2.servo_set(120, "S2")

        time.sleep(1)

        #Lift cube
        cyberpi.mbot2.servo_set(90, "S3")  # UD servo

        # 90 CW
        if side == "right":
            cyberpi.mbot2.drive_speed(-50, -50)
        elif side == "left":
            cyberpi.mbot2.drive_speed(50, 50)
        time.sleep(1)

        # Move
        cyberpi.mbot2.drive_speed(50, -50)

        # CHECK HOW MANY SECONDS TO REACH THE LEAKAGE DEVICE AREA! THIS IS A TIMED SEQUENCE
        time.sleep(2)
        cyberpi.mbot2.drive_speed(0, 0)

        # Release cube
        cyberpi.mbot2.servo_set(0, "S3")
        time.sleep(1)
        cyberpi.mbot2.servo_set(110, "S1")
        cyberpi.mbot2.servo_set(70, "S2")

        # BW for a bit
        time.sleep(0.5)
        cyberpi.mbot2.drive_speed(-50, 50)
        time.sleep(0.5)

        # U turn
        cyberpi.mbot2.drive_speed(-50, -50)
        time.sleep(2)

        # Return to line
        cyberpi.mbot2.drive_speed(50, -50)
        time.sleep(1.5)

        # 90 CW ; DLT CBC 03
        if side == "right":
            cyberpi.mbot2.drive_speed(-50, -50)
        elif side == "left":
            cyberpi.mbot2.drive_speed(50, 50)
        time.sleep(1)

    def Shoot(side):
        #release.
        cyberpi.mbot2.motor_drive(50, 0)
        time.sleep(0.5)

        #reset speed
        cyberpi.mbot2.motor_drive(0, 0)
        #set caliper to load
        cyberpi.mbot2.servo_set(0, "S4")

        #lock caliper
        time.sleep(1)
        cyberpi.mbot2.motor_drive(-40, 0)
        time.sleep(0.25)
        cyberpi.mbot2.motor_drive(0, 0)
        time.sleep(0.5)

        # return servo to original state
        cyberpi.mbot2.servo_set(170, "S4")

        time.sleep(1)


class Manual_Program:
    def __init__(self):
        pass

    def ControlMode():
        mbot2.servo_set(120, "S1")
        mbot2.servo_set(60, "S2")

        global select_mission, TotalMission, RunningMission, motor_left, motor_right, TurningTheta, MODE, LCSPEED, arm_y, arm_l, arm_r
        arm_l = 120
        arm_r = 60
        while True:
            mbot2.drive_power(0.8 * ((gamepad.get_joystick('Ly') + gamepad.get_joystick('Lx'))
                                     ), -0.8 * ((gamepad.get_joystick('Ly') - gamepad.get_joystick('Lx'))))
            arm_y = gamepad.get_joystick('Ry')
            distance = cyberpi.ultrasonic2.get(1)
            # Set servo ARM
            if not gamepad.is_key_pressed('N2'):
                mbot2.servo_set(arm_l, "S1")
                mbot2.servo_set(arm_r, "S2")
                mbot2.servo_set(arm_y, "S3")

            cyberpi.mbot2.motor_drive(0, 0)
            if distance < 10:
                cyberpi.led.on(255, 0, 0, "all")
            else:
                cyberpi.led.on(255, 255, 255, "all")
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
                arm_l = arm_l + 2
                arm_r = arm_r - 2

                # Prevents numbers from being negative

                if arm_l > 180:
                    arm_l = 180
                if arm_r < 0:
                    arm_r = 0

            if gamepad.is_key_pressed('N4'):
                arm_l = arm_l - 2
                arm_r = arm_r + 2

                # Prevents numbers from being negative

                if arm_l < 0:
                    arm_l = 0
                if arm_r > 180:
                    arm_r = 180

            if gamepad.is_key_pressed('N2'):
                mbot2.servo_set(180, "S3")
                time.sleep(0.4)

                mbot2.servo_set(120, "S1")
                mbot2.servo_set(50, "S2")

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
                time.sleep(0.25)
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


mbot2.forward = Manual_Program.forward
mbot2.backward = Manual_Program.backward
mbot2.turn_left = Manual_Program.turn_left
mbot2.turn_right = Manual_Program.turn_right
mbot2.EM_set_speed = Manual_Program.EM_set_speed
mbot2.drive_speed = Manual_Program.drive_speed


class Start:
    def __init__(self):
        pass

    def Boot():
        base_bat = cyberpi.get_battery()
        external_bat = cyberpi.get_extra_battery()
        cyberpi.console.clear()
        cyberpi.console.print("OOM PY\n------")
        if external_bat == 0:
            cyberpi.console.println("No external battery!")
        if base_bat < 10:
            cyberpi.console.println("Base battery low! Do not use on stage")

        cyberpi.console.print("Preparing bot...")
        time.sleep(1)

    def SelectMenu():
        auto_start = 0
        select_program = 1
        total_program = len(programs) - 1
        select_mode = 1

        cyberpi.console.clear()
        time.sleep(0.5)

        while select_mode == 1:
            if cyberpi.controller.is_press('up') or gamepad.is_key_pressed('Up'):
                while not not cyberpi.controller.is_press('up') or gamepad.is_key_pressed('Up'):
                    pass
                select_program = select_program + 1
                if select_program > total_program:
                    select_program = 1
            if cyberpi.controller.is_press('down') or gamepad.is_key_pressed('Down'):
                while not not cyberpi.controller.is_press('down') or gamepad.is_key_pressed('Down'):
                    pass
                select_program = select_program - 1
                if select_program < 1:
                    select_program = total_program

            cyberpi.display.show_label(
                programs[select_program], 16, "center", index=0)

            if cyberpi.controller.is_press('a') or gamepad.is_key_pressed('N4'):
                while not not cyberpi.controller.is_press('a') or not not gamepad.is_key_pressed('N4'):
                    pass
                select_mode = 0
            if cyberpi.controller.is_press('b') or gamepad.is_key_pressed('N3'):
                cyberpi.console.clear()
                while not not cyberpi.controller.is_press('b') or not not gamepad.is_key_pressed('N3'):
                    pass

                if select_program == 1:
                    cyberpi.led.on(255, 0, 0, "all")
                    Auto_Program.RunCode("left", True)
                    time.sleep(1)
                    cyberpi.led.on(0, 0, 0, "all")
                if select_program == 2:
                    cyberpi.led.on(0, 255, 0, "all")
                    Auto_Program.RunCode("left", False)
                    time.sleep(1)
                    cyberpi.led.on(0, 0, 0, "all")
                if select_program == 3:
                    cyberpi.led.on(255, 0, 255, "all")
                    Auto_Program.RunCode("right", True)
                    time.sleep(1)
                    cyberpi.led.on(0, 0, 0, "all")
                if select_program == 4:
                    cyberpi.led.on(255, 255, 255, "all")
                    Auto_Program.RunCode("right", False)
                    time.sleep(1)
                    cyberpi.led.on(0, 0, 0, "all")
                if select_program == 5:
                    cyberpi.led.on(255, 0, 255, "all")
                    Manual_Program.ControlMode()
                    time.sleep(1)
                    cyberpi.led.on(0, 0, 0, "all")

                if auto_start == 1:
                    select_mode = 0
                else:
                    select_program = 1
                    cyberpi.console.clear()


class Math:
    def __init__(self):
        pass

    def GetAngles(sides):
        pass


Start.Boot()

while True:
    Start.SelectMenu()
