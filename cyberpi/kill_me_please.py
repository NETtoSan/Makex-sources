import cyberpi
import time
import gamepad

automatic_stage = 1
programs = ["How did you get here????",
            "color sensor test", "full test", "ultrasonic test", "preferences", "test auto", "test servo"]
sensor_values = [1, 1]
# Declare on boot function
isCube = False


def start(prepmsg):
    #Clear screen
    cyberpi.console.clear()
    cyberpi.console.print("ST BUU\n--------")
    cyberpi.console.println(prepmsg)

    time.sleep(1)
    cyberpi.console.println("Done")


def select_menus():
    auto_start = 0  # Set automatic mission
    select_program = 1
    total_program = len(programs) - 1
    select_mode = 1

    cyberpi.console.clear()
    time.sleep(0.5)

    while select_mode == 1:

        if cyberpi.controller.is_press('up'):
            while not not cyberpi.controller.is_press('up'):
                pass
            select_program = select_program + 1
            if select_program > total_program:
                select_program = 1

        if cyberpi.controller.is_press('down'):
            while not not cyberpi.controller.is_press('down'):
                pass
            select_program = select_program - 1
            if select_program < 1:
                select_program = total_program

        cyberpi.display.show_label(
            "program:\n" + programs[select_program], 16, "center", index=0)

        #select mode = 0 goes back to manual mode, use this to stop a program or something.
        if cyberpi.controller.is_press('a'):
            while not not cyberpi.controller.is_press('a'):
                pass
            select_mode = 0

        if cyberpi.controller.is_press('b'):
            cyberpi.console.clear()
            while not not cyberpi.controller.is_press('b'):
                pass
            #Evaulate appropriate runtimes
            if select_program == 1:
                cyberpi.led.on(255, 255, 0, "all")
                test_mode(programs[select_program])
                time.sleep(1)
                cyberpi.led.on(0, 0, 0, "all")
            if select_program == 2:
                cyberpi.led.on(255, 0, 255, "all")
                test_joylr(programs[select_program])
                time.sleep(1)
                cyberpi.led.on(0, 0, 0, "all")
            if select_program == 3:
                cyberpi.led.on(255, 255, 255, "all")
                test_ultrasonic(programs[select_program])
                time.sleep(1)
                cyberpi.led.on(0, 0, 0, "all")
            if select_program == 4:
                cyberpi.led.on(0, 255, 255, "all")
                preferences(programs[select_program])
                time.sleep(1)
                cyberpi.led.on(0, 0, 0, "all")
            if select_program == 5:
                cyberpi.led.on(0, 255, 255, "all")
                test_auto(programs[select_program])
                time.sleep(1)
                cyberpi.led.on(0, 0, 0, "all")
            if select_program == 6:
                cyberpi.led.on(0, 255, 255, "all")
                test_servo(programs[select_program])
                time.sleep(1)
                cyberpi.led.on(0, 0, 0, "all")

            if select_program > len(programs) - 1:
                cyberpi.led.on(255, 0, 0, "all")
                cyberpi.display.show_label("program not set", 16, "center")
                time.sleep(1)
                cyberpi.led.on(0, 0, 0, "all")

            if auto_start == 1:
                select_mode = 0
            else:
                select_program = 1
                cyberpi.console.clear()
        #end if


def preferences(name):
    cyberpi.display.show_label(name, 16, 'center')
    time.sleep(1)
    preferences_list = ["offset track", "sensor line"]
    selected_settings = 0

    while not cyberpi.controller.is_press('a'):
        if cyberpi.controller.is_press('up'):
            while not not cyberpi.controller.is_press('up'):
                pass
            cyberpi.console.clear()
            selected_settings = selected_settings + 1
            if selected_settings > len(preferences_list) - 1:
                selected_settings = 0

        if cyberpi.controller.is_press('down'):
            while not not cyberpi.controller.is_press('down'):
                pass
            cyberpi.console.clear()
            selected_settings = selected_settings - 1
            if selected_settings < 1:
                selected_settings = len(preferences_list) - 1

        cyberpi.display.show_label(
            preferences_list[selected_settings], 16, 'center')

    cyberpi.console.clear()
    cyberpi.display.show_label('preferences saved', 16, 'center', index=0)
    time.sleep(2)

# Test gun loading mechanism


def test_servo(name):
    cyberpi.display.show_label(name, 16, 'center', index=0)
    time.sleep(1)

    #set caliper to load
    cyberpi.mbot2.servo_set(0, "S4")

    #lock shooting arm
    time.sleep(1)
    cyberpi.mbot2.motor_drive(-40, 0)

    time.sleep(0.25)

    #push the shooting arm servo back
    cyberpi.mbot2.motor_drive(0, 0)
    time.sleep(0.5)

    # return servo to original state
    cyberpi.mbot2.servo_set(170, "S4")
    while not cyberpi.controller.is_press('a'):
        if cyberpi.controller.is_press('b'):

            #release
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
        else:
            pass

    cyberpi.mbot2.servo_release("S4")
    cyberpi.console.clear()
    cyberpi.display.show_label('quit servo', 16, 'center')
    time.sleep(2)

# Full test


def test_joylr(name):
    cyberpi.display.show_label(name, 16, 'center', index=0)
    time.sleep(1)
    speed = 50
    isCube = True

    while not cyberpi.controller.is_press('a'):
        left_motor = (
            speed - (0.5 * cyberpi.quad_rgb_sensor.get_offset_track(1)))
        right_motor = -1 * \
            (speed + (0.5 * cyberpi.quad_rgb_sensor.get_offset_track(1)))

        offset = cyberpi.quad_rgb_sensor.get_offset_track(1)
        sta = cyberpi.quad_rgb_sensor.get_line_sta(1)
        gyro_x = cyberpi.get_gyro("x")
        gyro_y = cyberpi.get_gyro("y")
        gyro_r = cyberpi.get_yaw()
        usensor = cyberpi.ultrasonic2.get(1)

        label = str(offset) + " : " + str(usensor) + \
            "\n" + str(left_motor) + \
            "\n" + str(right_motor) + \
            "\n" + str(gyro_x) + " : " + str(gyro_y) + " : " + str(gyro_r)
        if offset < 1 and sta < 1:
            label = label + \
                "\nQRS Offline!"
        if usensor == 0:
            label = label + "\nU Offline!"

        elif usensor < 5.8:
            if isCube == True:
                isCube = False
                cyberpi.display.show_label(
                    'Cube grab function', 16, 'center', index=0)
                time.sleep(3)
            else:
                label = label + "\nSphere!"
        # Reports log to display
        cyberpi.console.println(label)
        cyberpi.console.clear()

    cyberpi.led.on(0, 0, 0, "all")
    cyberpi.display.show_label('quit full test', 16, 'center', index=0)
    time.sleep(2)


# !!!!! This will run on the actual stage <------------------ !!!!!
def test_auto(name):
    cyberpi.display.show_label(name, 16, 'center', index=0)
    time.sleep(1)
    speed = 50
    isCube = True
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
                grab_cube("lea")
            else:
                grab_arm("shoot")
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
    cyberpi.display.show_label('quit test auto', 16, 'center', index=0)
    time.sleep(2)

# Test line following program


def test_mode(name):
    cyberpi.display.show_label(name, 16, 'center', index=0)
    speed = 30

    time.sleep(1)
    while not cyberpi.controller.is_press('a'):

        # Swap + - to left and right motor
        left_motor = (
            speed - 0.5 * cyberpi.quad_rgb_sensor.get_offset_track(1))
        right_motor = -1 * \
            ((speed + 0.5 * cyberpi.quad_rgb_sensor.get_offset_track(1)))

        cyberpi.mbot2.drive_power(left_motor, right_motor)

    cyberpi.display.show_label('quit drive mode', 16, 'center', index=0)
    time.sleep(2)

# Test object grabbing hand


def test_ultrasonic(name):
    cyberpi.display.show_label(name, 16, 'center', index=0)
    time.sleep(1)

    #Set servo angles
    cyberpi.mbot2.servo_set(120, "S1")  # Left arm
    cyberpi.mbot2.servo_set(60, "S2")  # Right arm
    cyberpi.mbot2.servo_set(0, "S3")  # UD servo
    mode = "nothing"
    while not cyberpi.controller.is_press('a'):
        if cyberpi.controller.is_press('b'):
            while not not cyberpi.controller.is_press('b'):
                pass
            if mode == "nothing":
                mode = "shoot"
            else:
                mode = "nothing"
            # Print servo test mode. Whether to shoot or do nothing.

            cyberpi.console.print(mode)
            time.sleep(1)

        usensor = cyberpi.ultrasonic2.get(1)
        if usensor == 0:
            cyberpi.console.print(str(usensor)+"\nOffline!")

        elif usensor < 5.3:
            # Code goes here
            cyberpi.console.print(str(usensor)+"\ngrab object")

            grab_arm(mode)

        else:
            cyberpi.mbot2.servo_set(120, "S1")  # Left arm
            cyberpi.mbot2.servo_set(60, "S2")  # Right arm
            cyberpi.mbot2.servo_set(0, "S3")  # UD servo
            cyberpi.console.print(str(usensor)+"\nOnline")

        cyberpi.console.clear()

    # Release all servos as relative to their angles
    cyberpi.mbot2.servo_release("S1")
    cyberpi.mbot2.servo_release("S2")
    cyberpi.mbot2.servo_release("S3")

    cyberpi.display.show_label('quit ultrasnic mode', 16, 'center', index=0)
    time.sleep(2)

# Run the shooting program


def shoot():

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


# Get angles to predict from whether the bot starts from left to right.
def get_angles(lea, lex):
    # set every values to default as if relative position is on the right

    pass

# Cube program


def grab_cube(lea):

    #Grab cube
    cyberpi.mbot2.servo_set(60, "S1")
    cyberpi.mbot2.servo_set(120, "S2")

    time.sleep(1)

    #Lift cube
    cyberpi.mbot2.servo_set(90, "S3")  # UD servo

    # 90 CW
    cyberpi.mbot2.drive_speed(-50, -50)
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
    time.sleep(0.25)

    # U turn
    cyberpi.mbot2.drive_speed(-50, -50)
    time.sleep(2)

    # Return to line
    cyberpi.mbot2.drive_speed(50, -50)
    time.sleep(1.75)

    # 90 CW ; DLT CBC 03
    cyberpi.mbot2.drive_speed(-50, -50)
    time.sleep(1)

    colornum = cyberpi.quad_rgb_sensor.get_offset_track(1)

    # IF TIMED SEQUENCE DOES NOT WORK. LET THE SENSOR DO ITS JOB AND GOD HOPE THIS WILL WORK

    #while colornum > 10:
    #    cyberpi.mbot2.drive_speed(50, -50)
    #    colornum = cyberpi.quad_rgb_sensor.get_offset_track(1)
    #    cyberpi.display.show_label(str(colornum), 16, 'center', index=0)

# Sphere program


def grab_arm(lea):

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

        cyberpi.mbot2.drive_speed(50, 50)
        time.sleep(1)
        cyberpi.mbot2.drive_speed(0, 0)

        time.sleep(2)
        shoot()

        cyberpi.mbot2.drive_speed(-50, -50)
        time.sleep(1)
        cyberpi.mbot2.drive_speed(0, 0)

    else:
        pass


start("Preparing libraries.....")


while True:
    if automatic_stage == 1:
        select_menus()
        automatic_stage = 0
    else:
        automatic_stage = 1
        start("Rebooting....")
        cyberpi.restart()
