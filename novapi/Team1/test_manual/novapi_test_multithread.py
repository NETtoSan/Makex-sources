import novapi
import machine
import _thread
import time
import os

# important function
print("""
  _   _ ______ _______ _        ___  _   _  _____ 
 | \ | |  ____|__   __| |      | \ \| \ | |/ ____|
 |  \| | |__     | |  | |_ ___ | || |  \| | (___  
 | . ` |  __|    | |  | __/ _ \| || | . ` |\___ \ 
 | |\  | |____   | |  | || (_) |_|| | |\  |____) |
 |_| \_|______|  |_|   \__\___/(_)| |_| \_|_____/ 
                                 /_/              
                                                  """)
print("--- NETto!_NS Runtime ---\n[W] For testing purposes!\n---------")
print("machine:\n{}".format(dir(machine)))
print("---\nnovapi:\n{}".format(dir(novapi)))
print("---\nthreading:\n{}".format(dir(_thread)))


# Programs to run in bg
def start_1(var1, var2):
    y = 0
    while y < 50:
        print("hello mill {}".format(y))
        print("{} {}".format(var1, var2))
        time.sleep(0.1)
        y += 1

def start_2(var1, var2):
    z = 0
    while z < 50:
        print("hello everyone".format(z))
        print("{} {}".format(var1, var2))
        time.sleep(0.1)
        z += 1

# Test class
class robot:

    def logic_control(time_set):
        global logic
        # Switches param ON/OFF on time set
        time_elapsed = 0
        logic = True; print("[i] Set logic to TRUE")

        while time_elapsed < time_set:
            time_elapsed += 1
            print("[i] -- Elapsed time: {} --".format(time_elapsed))
            time.sleep(1)

        logic = False

    def use_arm():
        global logic
        while logic == True:
            print("[O] Arm running!")
            time.sleep(0.5)
        print("[R] Arm stopped ---")
    
    def use_wheel():
        global logic
        while logic == True:
            print("[O] Wheel running!")
            time.sleep(0.5)
        print("[R] Wheel stopped ---")

# Declare variables to use in multithreading
var1 = 1
var2 = 2
logic = False   # Control both use_arm and use_wheel process

# Runtime
def start_thread():
    # Spawn another function in the background
    _thread.start_new_thread(start_1, var1, [var1, var2])
    _thread.start_new_thread(start_2, var1, [var1, var2])
    x = 0
    while x < 50:
        print("Single thread! {}".format(x))
        x += 1
        time.sleep(0.1)
def start_thread_robot():
    param = True
    _thread.start_new_thread(robot.logic_control, 0, [10])
    _thread.start_new_thread(robot.use_arm, 0, [])
    _thread.start_new_thread(robot.use_wheel, 0, [])

# Single thread operation
print("\n------ Start thread ------")
start = 0
if start == 1:
    start_thread()
if start == 2:
    start_thread_robot()
else:
    print("Start thread not enabled!")