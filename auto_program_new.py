import cyberpi
import time
import gamepad
import mbot2
import event
import mbuild_modules.starter_shield as starter_shield

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


automatic_stage = 1
reaction_preferences = [0, 6]  # Quad RGB, Ultrasonic sensor
programs = ["How", "Auto start left", "Auto start left\nNo cube",
            "Auto start right", "Auto start right\nNo cube"]
# Manual MODE


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

# End manual stage


def start():
    batlevel = cyberpi.get_battery()
    ebatlevel = cyberpi.get_extra_battery()

    cyberpi.console.clear()
    cyberpi.console.print("ST BUU\n-------")

    if ebatlevel == 0:
        cyberpi.console.println("No external battery")
    if batlevel < 10:
        cyberpi.console.println("Battery low! Do not use on stage!")

    cyberpi.console.println("Preparing bot.....")
    time.sleep(1)


def select_menu():
    auto_start = 0
    select_program = 1
    total_program = len(programs) - 1
    select_mode = 1

    cyberpi.console.clear()
    time.sleep(0.5)

    while select_mode == 1:
        if cyberpi.controller.is_press('up') or gamepad.is_key_pressed('Up'):
            while not not cyberpi.controller.is_press('up'):
                pass
            select_program = select_program + 1
            if select_program > total_program:
                select_program = 1

        if cyberpi.controller.is_press('down') or gamepad.is_key_pressed('Down'):
            while not not cyberpi.controller.is_press('down'):
                pass
            select_program = select_program - 1
            if select_program < 1:
                select_program = total_program

        cyberpi.display.show_label(
            programs[select_program], 16, "center", index=0)

        if cyberpi.controller.is_press('a') or gamepad.is_key_pressed('N3'):
            while not not cyberpi.controller.is_press('a'):
                pass
            select_mode = 0
        if cyberpi.controller.is_press('b') or gamepad.is_key_pressed('N4'):
            cyberpi.console.clear()
            while not not cyberpi.controller.is_press('b') or not not gamepad.is_key_pressed('N4'):
                pass

            if select_program == 1:
                cyberpi.led.on(255, 0, 0, "all")
                auto_mode("left", True)
                time.sleep(1)
                cyberpi.led.on(0, 0, 0, "all")
            if select_program == 2:
                cyberpi.led.on(0, 255, 0, "all")
                auto_mode("left", False)
                time.sleep(1)
                cyberpi.led.on(0, 0, 0, "all")
            if select_program == 3:
                cyberpi.led.on(255, 0, 255, "all")
                auto_mode("right", True)
                time.sleep(1)
                cyberpi.led.on(0, 0, 0, "all")
            if select_program == 4:
                cyberpi.led.on(255, 255, 255, "all")
                auto_mode("right", False)
                time.sleep(1)
                cyberpi.led.on(0, 0, 0, "all")

            if auto_start == 1:
                select_mode = 0
            else:
                select_program = 1
                cyberpi.console.clear()


def get_inverse(sides):

    # Left and right have opposite starting angles. Best to invert everything so we can have the expected behavior
    pass


def Manual():
    global select_mission, TotalMission, RunningMission, motor_left, motor_right, TurningTheta, MODE, LCSPEED, arm_y
    while True:
        mbot2.drive_power(0.8 * ((gamepad.get_joystick('Ly') + gamepad.get_joystick('Lx'))
                                 ), -0.8 * ((gamepad.get_joystick('Ly') - gamepad.get_joystick('Lx'))))
        arm_y = gamepad.get_joystick('Ry')
        distance = cyberpi.ultrasonic2.get(1)
        if distance < 10:
            cyberpi.led.on(255, 0, 0, "all")
        else:
            cyberpi.led.on(255, 255, 255, "all")
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


def auto_mode(sides, cube):
    cyberpi.display.show_label("Auto mode", 16, 'center', index=0)
    time.sleep(1)
    speed = 50
    isCube = cube
    # Pretend that the bot starts in the area. And the sensor havent found the lines yet. Let it run at 50% both sides for 1 second
    # Presuming the next thing that's next to the bot is the lines
    cyberpi.mbot2.drive_speed(50, -50)
    time.sleep(1)

    # Set arm to STANDBY
    cyberpi.mbot2.drive_speed(0, 0)
    cyberpi.mbot2.servo_set(120, "S1")  # Left arm
    cyberpi.mbot2.servo_set(60, "S2")  # Right arm
    cyberpi.mbot2.servo_set(0, "S3")  # UD servo

    # Retracting shooting servo
    cyberpi.mbot2.servo_set(0, "S4")

    # Set shooting mechanics to STANDBY
    time.sleep(1)
    cyberpi.mbot2.motor_drive(-40, 0)
    time.sleep(0.25)
    cyberpi.mbot2.motor_drive(0, 0)
    time.sleep(0.5)

    # Return shooting servo to DONE state
    cyberpi.mbot2.servo_set(170, "S4")
    while not cyberpi.controller.is_press('a'):
        if gamepad.is_key_pressed('R2'):
            cyberpi.console.clear()
            cyberpi.display.show_label('Manual mode', 16, 'center', index=0)
            cyberpi.led.on(255, 255, 0, "all")
            Manual()

        left_motor = (
            speed - (0.5 * cyberpi.quad_rgb_sensor.get_offset_track(1)))
        right_motor = -1 * \
            (speed + (0.5 * cyberpi.quad_rgb_sensor.get_offset_track(1)))

        usensor = cyberpi.ultrasonic2.get(1)

        # Make an identification logic for usensor. Whether it's a cube or a sphere. Look at full test program for references
        if usensor < 6 and usensor != 0:

            cyberpi.mbot2.drive_speed(30, -30)  # slow mbot2 motion
            time.sleep(0.3)
            cyberpi.mbot2.drive_speed(0, 0)  # stop mbot2

            if isCube == True:
                isCube = False
                grab_cube("lea", sides)
            else:
                grab_sphere("shoot", sides)
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


def shoot(side):
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


def grab_sphere(lea, side):
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
        #count CW
        orientation = cyberpi.get_yaw()

        # If start from the right spot. Rotate CW to point bot to the oponent's goal
        target = orientation - 90

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
        shoot(side)
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


def grab_cube(lea, side):
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

    colornum = cyberpi.quad_rgb_sensor.get_offset_track(1)


start()

while True:
    if automatic_stage == 1:
        select_menu()
        automatic_stage = 0
    else:
        automatic_stage = 1
        start()
        cyberpi.restart()
