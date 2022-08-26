import cyberpi
import time
import gamepad
import mbuild  # <- This mbuild is NOT from makecode. It goes to github repository for chemistry molecular construction

from cyberpi import *


#Initialize necessary variables
automatic_stage = 1
msg = "ST BUU"
cyberpi.console.clear()


#Function that will start when the device boots


def on_start():

    #Reset motor speed apon device reflash
    cyberpi.mbot2.drive_speed(0, 0)

    #Initialize
    cyberpi.audio.set_vol(10)
    cyberpi.display.rotate_to(90)
    cyberpi.display.show_label(msg, 16, 'center')

    #cyberpi.led.on(255, 0, 255, "all")
    cyberpi.led.play(name="rainbow")

    cyberpi.console.clear()
    #cyberpi.display.show_label(f"{cyberpi.get_battery()}%", "center", index=0)
    cyberpi.led.on(0, 255, 0, "all")

    time.sleep(1)

    cyberpi.led.on(0, 0, 0, "all")
    cyberpi.console.clear()


def line_follower(speed):

    motor_left = (
        speed - (0.5 * cyberpi.quad_rgb_sensor.get_offset_track(1)))
    motor_right = -1 * \
        (speed + (0.5 * cyberpi.quad_rgb_sensor.get_offset_track(1)))
    cyberpi.mbot2.drive_speed(motor_left, motor_right)


def line_follower_timer(speed, seconds):
    cyberpi.timer.reset()
    while not cyberpi.timer.get() > seconds:
        line_follower(speed)
    cyberpi.mbot2.drive_speed(0, 0)
    time.sleep(0.5)


def stop_moving():
    cyberpi.mbot2.drive_speed(0, 0)
    time.sleep(0.5)

#Evaluate this dfunction and see if the motor runs as expected


def m01():
    cyberpi.display.show_label('m01', 32, 'center')
    line_follower_timer(50, 5)


def m02():
    cyberpi.display.show_label('m02', 32, 'center')
    cyberpi.mbot2.drive_speed(50, -50)
    time.sleep(5)
    cyberpi.mbot2.EM_stop(port="all")


def m03():
    cyberpi.display.show_label('m03', 32, 'center')
    while not cyberpi.quad_rgb_sensor.get_line_sta(1) == 15:
        cyberpi.mbot2.drive_speed(50, -50)
    cyberpi.mbot2.EM_stop(port="all")


def test_mode():
    cyberpi.display.show_label('sensor test mode', 32, 'center', index=0)

    time.sleep(1)
    while not cyberpi.controller.is_press('a'):
        output = str(cyberpi.quad_rgb_sensor.get_offset_track(1)) + \
            "\n" + str(cyberpi.quad_rgb_sensor.get_line_sta(1))
        cyberpi.display.show_label(
            output, 16, 'center', index=0)
        cyberpi.console.clear()

    cyberpi.display.show_label('Quit test mode', 16, 'center', index=0)
    time.sleep(2)


#Automatic program


def auto_program():
    auto_start = 0  # Set automatic mission
    select_program = 1
    total_program = 5
    select_mode = 1

    cyberpi.display.show_label('Ready to start', 32, 'center', index=0)
    time.sleep(2)

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

        cyberpi.display.show_label(select_program, 32, "center", index=0)

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
                m01()
                time.sleep(1)
                cyberpi.led.on(0, 0, 0, "all")

            elif select_program == 2:
                cyberpi.led.on(255, 50, 0, "all")
                m02()
                time.sleep(1)
                cyberpi.led.on(0, 0, 0, "all")

            elif select_program == 3:
                cyberpi.led.on(255, 0, 50, "all")
                m03()
                time.sleep(1)
                cyberpi.led.on(0, 0, 0, "all")

            elif select_program == 4:
                cyberpi.led.on(0, 255, 255, "all")
                test_mode()
                time.sleep(1)
                cyberpi.led.on(0, 0, 0, "all")

            elif select_program == 5:
                cyberpi.display.show_label('program not set', 32, 'center')
                cyberpi.led.on(0, 0, 255, "all")
                time.sleep(1)
                cyberpi.led.on(0, 0, 0, "all")

            if auto_start == 1:
                select_mode = 0
            else:
                select_program = 1
                cyberpi.console.clear()
        # end if


# Manual program


def manual_program():
    start_manual = 1

    # Put all motor to 0. To debug things
    motor_left = 0
    motor_right = 0

    cyberpi.display.show_label("Manual mode", 32, "center", index=0)
    while start_manual == 1:
        motor_left = 0
        motor_right = 0

        cyberpi.mbot2.drive_speed(motor_left, motor_right)

        if cyberpi.controller.is_press('a'):
            while not not cyberpi.controller.is_press('a'):
                pass
            start_manual = 0

    #end while
    cyberpi.mbot2.EM_stop(port="all")
    cyberpi.led.on(0, 0, 0, "all")
    cyberpi.display.show_label("Quit manual mode", 32, "center", index=0)
    cyberpi.led.on(255, 0, 0, "all")
    time.sleep(1)
    cyberpi.led.on(0, 0, 0, "all")


on_start()

while True:
    if automatic_stage == 1:
        auto_program()
        automatic_stage = 0
    else:
        manual_program()
        automatic_stage = 1
