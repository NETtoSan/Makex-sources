import cyberpi, time, gamepad, mbot2, event, mbuild_modules.starter_shield as starter_shield

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

    def RunCode(sides,cube):
        pass


class Manual_Program:
    def ControlMode():
        pass
    def forward(speed= default_speed, run_time= default_runtime, accel_time=1, decel_time=1):
        if speed = 0:
            mbot2.EM_stop(all)
    def backward(speed=default_speed, run_time=default_runtime, accel_time=1, decel_time=1):

    def turn_left(speed=default_speed, run_time=default_runtime, accel_time=1, decel_time=1):

    def turn_right(speed=default_speed, run_time=default_runtime, accel_time=1, decel_time=1):

    def EM_set_speed(speed=default_speed, port="all"):

    def drive_speed(EM1_speed=default_speed, EM2_speed=default_speed, run_time=default_runtime, accel_time=1, decel_time=1):

mbot2.forward = Manual_Program.forward
mbot2.backward = Manual_Program.backward
mbot2.turn_left = Manual_Program.turn_left
mbot2.turn_right = Manual_Program.turn_right
mbot2.EM_set_speed = Manual_Program.EM_set_speed
mbot2.drive_speed = Manual_Program.drive_speed


class Start:
    def Boot():
        pass

    def SelectMenu():
        pass


class Math:
    def GetAngles(sides):
        pass


Start.Boot()

while true:
    Start.SelectMenu()
