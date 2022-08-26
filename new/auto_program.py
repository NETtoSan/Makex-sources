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

default_speed = 50
default_runtime = "null"
second_msfactor = 1000

automatic_stage = 1
reaction_preferences = [0, 6]  # Quad RGB, Ultrasonic sensor
programs = ["How", "Auto start left", "Auto start left\nNo cube",
            "Auto start right", "Auto start right\nNo cube"]


class Auto_Program:
    def __init__(self, sides):
        pass

    def RunCode(sides, cube):
        pass

    def GrabBall(lea, side):
        pass

    def GrabCube(lea, side):
        pass

    def Shoot():
        pass


class Manual_Program:
    def ControlMode():
        pass

    def forward(speed=default_speed, run_time=default_runtime, accel_time=1, decel_time=1):
        if speed == 0:
            mbot2.EM_stop(all)

    def backward(speed=default_speed, run_time=default_runtime, accel_time=1, decel_time=1):
        pass

    def turn_left(speed=default_speed, run_time=default_runtime, accel_time=1, decel_time=1):
        pass

    def turn_right(speed=default_speed, run_time=default_runtime, accel_time=1, decel_time=1):
        pass

    def EM_set_speed(speed=default_speed, port="all"):
        pass

    def drive_speed(EM1_speed=default_speed, EM2_speed=default_speed, run_time=default_runtime, accel_time=1, decel_time=1):
        pass


mbot2.forward = Manual_Program.forward
mbot2.backward = Manual_Program.backward
mbot2.turn_left = Manual_Program.turn_left
mbot2.turn_right = Manual_Program.turn_right
mbot2.EM_set_speed = Manual_Program.EM_set_speed
mbot2.drive_speed = Manual_Program.drive_speed


class Start:
    def Boot():
        base_bat = cyberpi.get_battery()
        external_bat = cyberpi.get_extra_battery()
        cyberpi.console.clear()
        cyberpi.console.print("ST BUU\n------")
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
                while not not cyberpi.controller.is_press('up') or gamepad.is_key_pressed('up'):
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

                if auto_start == 1:
                    select_mode = 0
                else:
                    select_program = 1
                    cyberpi.console.clear()


class Math:
    def GetAngles(sides):
        pass


Start.Boot()

while True:
    Start.SelectMenu()
