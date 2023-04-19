import time
import os, sys
import random
from datetime import date
# RESOURCES
modes = ["auto", "manual"]
commands = ["restart", "settings", "about", "exit (CTRL+C)"]
logs = []
cube_done = False

def logutil(s):
    global logs
    t = time.localtime(time.time())
    ctime = f"[{t.tm_hour}:{t.tm_min}:{t.tm_sec}]"
    print(f"{ctime} {s}")
    logs.append(f"{ctime} {s}")
def isneg(v):
    return False if v > 0 else False if v == 0 else True
def stat(ts):
        global logs
        t = time.localtime(time.time())
        nowtime = f"{t.tm_hour}{t.tm_min}{t.tm_sec}"
        logutil("\n--------------------")
        logutil("> Auto code done <")
        logutil("[!] The cube is not on our alliance side") if cube_done is False else logutil("[I] The cube is on our alliance side")
        logutil(f"Time elapsed {t} seconds. {'time out!' if ts > 30 else 'Auto completed in time limit'}")
        logutil(f"[I] Log file has been saved at ./logs/{date.today()}/{nowtime}.txt")
        logutil("--------------------")

        with open(f'./logs/{date.today()}/{nowtime}.txt','w') as tfile:
            tfile.write('\n'.join(logs))
def ask(which):
    prompt = input(f"Available scenarios: [{' , '.join(modes)}]\nAvailable commands:  [{' , '.join(commands)}]\n> " if which == "main" else f"Available settings: [{' , '.join(settings_config)}]\n> ")
    return prompt
def about():
    print("\n\n\nMakeX robot simulator Version 0.3")
    print("By NETto and Lupow132 (2023)")
    print("This software or python source code is intended for demonstration purposes\nand does not interfere with MakeBlock co.ltd")
    print("This software is intended to use for simulating MakeX challenge robotics competiton\nand such equipment is simulated through generating random numbers")
    print("\nGenerated given random numbers and you need to do whatever it takes to make cube x,y is 0. Basically an auto cube program")
    print("\n\nThis software is intended to use inside iRobot ST-BUU. But if you are from the outside schools. Feel free\n")
def boot():
    print("\n----------- NETto!_NS Scenario simulator -----------") 
    print("> god help me")
    print("[I] By NETto & LuPow132\nVersion 0.3\n")

class led_lights():
    def __init__ (self):
        pass
    def set_rgb_color(self,col):
        global logs
        color = ["red", "green", "blue"]
        try:
            color.index(col)
            logutil(f"[I] Setting rgb color to {col}")
        except ValueError:
            logutil("[!] That color DOES NOT exist")
class encode_motor():
    def __init__ (self):
        pass
    def set_speed(self, speed):
        logutil(f"setting motor at {speed}%")
class ranging_sensor():
    def __init__ (self):
        pass
    def get_distance(self):
        return random.randint(20,200)
class smart_camera():
    def __init__ (self):
        pass
    
    def detect_sign(self, s):
        return True
    def get_sign_x(self, s):
        return random.randint(-100,100)
    def get_sign_y(self ,s):
        return random.randint(-100,100)
    def detect_sign_location(s, side):
        if side == "middle" or side == "up" or side == "down" or side == "left" or side == "right":
            pass
        else:
            print("[!] Not a valid camera region")
class bot():
    def __init__ (self):
        pass
    def move(v1, v2, v3, v4, sec):
        global logs
        movement = "Invalid"
        if isneg(v1) is False and isneg(v2) is True and isneg(v3) is False and isneg(v4) is True:
            movement = "fwd"
        if isneg(v1) is True and isneg(v2) is False and isneg(v3) is True and isneg(v4) is False:
            movement = "bwd"
        if isneg(v1) is True and isneg(v2) is True and isneg(v3) is False and isneg(v4) is False:
            movement = "slf"
        if isneg(v1) is False and isneg(v2) is False and isneg(v3) is True and isneg(v4) is True:
            movement = "srt"
        if isneg(v1) is True and isneg(v2) is True and isneg(v3) is True and isneg(v4) is True:
            movement = "rlf"
        if isneg(v1) is False and isneg(v2) is False and isneg(v3) is False and isneg(v4) is False:
            movement = "rrt"
        logutil(f"[I] Set motor speed for {v1} {v2} {v3} {v4} {movement} for {sec} sec")
        time.sleep(sec)

# SETTINGS
def settings():
    prompt_exit = 0
    prompt_selector = { "now": 0, "max": len(settings_config) -1 }
    while prompt_exit == 0:
        prompt = ask("settings")
        print(f"Keywords prompted: {prompt}\n")
        if prompt == "exit" or prompt == "quit":
            prompt_exit = 1
        else:
            a = settings_config.get(prompt)
            if a is None:
                print("That DOES NOT exist!")


# BOT CORE
smartcam = smart_camera()
rangesensor = ranging_sensor()
class auto():
    def __init__ (self):
        self.lights = led_lights() #simulate_lights

    def self_correct_cube(cube_location):
        if cube_location[0] > 0:
            while cube_location[0] > 0: # right
                bot.move(-50, 50, -50, 50, 0.01)
                cube_location[0] = cube_location[0] - 1
        if cube_location[0] < 0:
            while cube_location[0] < 0: # left
                bot.move(50, -50, 50, -50, 0.01)
                cube_location[0] = cube_location[0] + 1

    def modes(self,prompt):
        global cube_done, logs
        # Log time init, starting time
        start_time = int(time.localtime(time.time()).tm_sec)

        logutil("MakeX Challenge energy innovator auto cube program\n")
        logutil("> SENSORS: RANDOM NUMBERS\n> JSON FILE: ./intents.json\n> CAMERA: True\n> RANGING_SENSORS: True")
        self.lights.set_rgb_color("blue")
        time.sleep(2)
        bot.move(50, -50, 50, -50, 1)     # Move forward
        bot.move(50, 50, 50, 50, 1)       # Slide right
        bot.move(50, -50, 50, -50, 1)     # Move forward
        
        cube_exist = smartcam.detect_sign("S1")
        if cube_exist is True:
            cube_location = [
                int(smartcam.get_sign_x("S1")),
                int(smartcam.get_sign_y("S1"))
            ]

            logutil(f"{cube_exist} [cube_x:{int(cube_location[0])} cube_y:{int(cube_location[1])}]")
            logutil("[!] AUTO CORRECTING CUBE LOCATION")            
            time.sleep(1)
            # Move the bot so it aligned to the cube
            if cube_location[0] != 0:
                auto.self_correct_cube(cube_location)
            
            cube_range = rangesensor.get_distance()
            cube_was_range = cube_range
            check_counts = 0
            
            logutil("[!] SLIDING TO CUBE")
            time.sleep(1)
            # Slide to cube
            while cube_range > 10:
                bot.move(50, 50, -50, -50, 0.01)
                check_counts += 1

                if check_counts == 10:
                    # Simulate bot error while sliding
                    cube_location[0] = random.randint(0, 20)
                    if cube_location[0] != 0:
                        logutil("[---] AUTO CORRECTING CUBE LOCATION")
                        auto.self_correct_cube(cube_location)
                        logutil("[---] AUTO CORRECTING CUBE DONE")
                    check_counts = 0
                cube_range -= 1
        
        logutil("[-!-] CUBE AT POSITION")
        logutil(f"{cube_exist} [cube_x:{int(cube_location[0])} cube_y:{int(cube_location[1])} cube_range_was:{cube_was_range} cube_range_now:{cube_range}]")


        #power_expand_board.set_power(dc_hand,100)
        logutil("Grabbing cube")
        time.sleep(2)
        bot.move(50, 50, -50, -50, 2)
        #power_expand_board.set_power(dc_hand,100)
        logutil("Releasing cube")
        time.sleep(2)

        cube_range = rangesensor.get_distance() # This sensor int is randomly generated
        if cube_range != 10:
            cube_done = True 
        else:
            cube_done = False
        
        end_time = int(time.localtime(time.time()).tm_sec) - start_time
        stat(end_time)

# FUNCTIONS
boot()
while True:
    time.sleep(1)
    prompt  = ask("main")
    print(f"Keywords prompted: {prompt}")
    auto_test = auto()
    if prompt == "auto":
        auto_test.modes(prompt)

    elif prompt == "restart":
        print("Restarting simulator......")
        os.system("python novapi/Team1/simulator/cube.py")
        time.sleep(0.2)
    elif prompt == "about":
        about()
    elif prompt == "exit":
        quit()
    elif prompt == "settings":
        settings()
    else:
        print("[!] Not a valid scenario\n")