

# These are for demonstration purposes!

class system:
    def loadlogo():
        print("""
         _   _ ______ _______ _        ___  _   _  _____ 
        | \ | |  ____|__   __| |      | \ \| \ | |/ ____|
        |  \| | |__     | |  | |_ ___ | || |  \| | (___  
        | . ` |  __|    | |  | __/ _ \| || | . ` |\___ \ 
        | |\  | |____   | |  | || (_) |_|| | |\  |____) |
        |_| \_|______|  |_|   \__\___/(_)| |_| \_|_____/ 
                                         /_/              
                                                        """)
        print("--- NETto!_NS Runtime ---\n[i] This runtime is compiled for NovaPi V1_3\n[W] For testing purposes!\n----------------")

    def loadme():
        print("NETto!_NS Bootloader\nLoading attributes"); time.sleep(1)
        print("----------------")
        x = 0
        while x <= 100:
            print("[i] Preparing [{}%]".format(x))
            x += 2
            time.sleep(0.1)
        print("----------------")

    def loadConfig(path):
        cfile = system.getfiles(path)
        if(cfile.startswith("[W]")):
            return cfile
        else:
            return eval(cfile)

    def getfiles(path):
        try:
            with open(path) as user_file:
                file_contents = user_file.read()
                print("[i] Successfully loaded {}!".format(path))
                return file_contents
        except:
            return "[W] Could not read {}!".format(path)

    def uiinput():
        global challenge_robot
        isshell = True
        print("----------------")
        print("[I] You are now on shell mode\n    To run the challenge bot, simply run the command run.")
        while isshell == True:
            arg = input("> ").split()
            cmd = arg[0]

            if(cmd == "help"):
                # Change this to ui_help.txt then upload!
                print(" Available commands")
                print(" Parameters: [] required, <> optional")
                print("----------------------------------------------")
                print("| commands                         | description")
                print("----------------------------------------------")
                print("| acq [on/off]                     | Set a Ranging sensor to aquire mode")
                print("| dir [path]                       | List NovaPi's directory")
                print("| exit                             | Exit NETto!_NS runtime (For flashing!)")
                print("| flash                            | Also exit the program allowing the novapi to flash (The indicator will start blinking)")
                print("| load_mbuild                      | Load a file from internal EEPROM chip")
                print("| mbuild [set|read] [port] [kind]  | Set an mbuild port to a configuration of choice")
                print("| odometry [on/off]                | Track X, Y movement of a robot")
                print("| read [file_name]                 | Read a file from internal EEPROM chip")
                print("| reboot                           | Reboot a system")
                print("| run <auto/manual>                | Run the MakeX Challenge program [On field!]")
                print("| setarm [port_no]                 | Set a DC motor for operating an arm")
                print("| setgun [servo/dc] [port]         | Program a motor in which to control a gun angle")
                print("| setsensor [sensor] [port]        | Set mbuild sensor")
                print("| settarget [sign] [color]         | Set a color signature")
                print("| setwheel [mode]                  | Set a wheel to desired mode")
                print("| testtarget [sign]                | Test a signature, Needs ACQ mode to be turn on!")
                print("----------------------------------------------")

            elif(cmd == "run"):
                print("[i] Running MakeX Challenge program!")
                print("----------------")
                try:
                    exec(open(CHALLENGE_DEFAULT_RUNTIME_FILE).read()) # Run a separate file
                except:
                    print("[W] Something went wrong running challenge_default!")

            elif(cmd == "dir"):
                if len(arg) > 1 and len(arg) < 3:
                    print("[i] Listing {}".format(arg[-1]))
                    try:
                        file_contents = os.listdir(arg[-1])
                        for file in file_contents:
                            print(" > {}".format(file))
                    except:
                        print("[W] Could not read {}!".format(arg[-1]))
                elif len(arg) > 1:
                    print("[W] > dir, Only 1 argument is required\n    e.g: dir ./obj.json")
                else:
                    print("[i] > dir, Missing file path!\n    e.g: dir ./obj.json")        


            elif(cmd == "acq"):
                mbuild_ports_4 = "ranging_sensor" # dummy code. use mbuild_ports[] and for loop to find ranging sensor

                if (mbuild_ports_4 == "ranging_sensor"):
                    print(" ACQ (Aquisition mode)")
                    # Change all these .format() with actual values
                    print("----------------------------")
                    print("| settings           | value")
                    print("| mbuld port         | {}".format("4"))
                    print("| scan attribute     | {}".format("rect"))
                    print("| scan azimuth       | {}, {}".format(-5, 5))
                    print("| scan altitute      | {}, {}".format(5, 5))
                    print("| scan interval      | {}".format("100"))
                    print("| scan range         | {}".format("100"))
                    print("----------------------------")
                    continue
                else:
                    print("[W] ACQ (Aquisition) mode requires 1 ranging sensor!\n Aquisition mode requires ranging sensor to track singular object")

            elif(cmd == "mbuild"):
                if len(arg) == 1:
                    # Actual mbuild configurator API soon!
                    print(" mbuild configurator")
                    print(" To view or setup mbuild ports. Run: mbuild [set|read] [port] [kind]")
                    print(" mbuild config path: ./flash/hawkeye_sensors.json")
                    print("----------------------------------------------")
                    print("| mbuild port | device        | stat     | chained")
                    print("| [mbuild 1]  | !DEAD         | [DEAD]   | [0]")
                    print("| [mbuild 2]  | !DEAD         | [DEAD]   | [0]")
                    print("| [mbuild 3]  | !DEAD         | [DEAD]   | [0]")
                    print("| [mbuild 4]  | RANGING_SENS  | [NORM]   | [1]")
                    print("| [mbuild 5]  | BLUETOOTH     | [NORM]   | [1]")
                    print("----------------------------------------------")

            elif(cmd == "load_mbuild"):
                print("[i] Loading {}".format("./sensors.json"))
                file_contents = system.loadConfig("./sensors.json")
                is_valid = True
                for i in file_contents:
                    if(i == "identifier" and file_contents[i] == "NETto!_NS" or is_valid == True):
                        is_valid = True
                        print("{}: {}".format(i, file_contents[i]))
                    else:
                        print("[W] Idenfier must be set to NETto!_NS !")
                
                # I = Index, D = Details!
                for i in range(len(file_contents["sensors"])):
                    print("----------------------------")
                    for d in file_contents["sensors"][i]:
                        print("{}: {}".format(d, file_contents["sensors"][i][d]))
                print("----------------------------")

            elif(cmd == "read"):
                if len(arg) > 1 and len(arg) < 3:
                    print("[i] Loading {}".format(arg[-1]))
                    file_contents = system.getfiles(arg[-1])
                    print(file_contents)
                elif len(arg) > 1:
                    print("[W] > read, Only 1 argument is required\n    e.g: read ./obj.json")
                else:
                    print("[i] > read, Missing file path!\n    e.g: read ./obj.json")

            elif(cmd == "reboot"):
                machine.reset()

            elif(cmd == "exit"):
                isshell = False

            elif(cmd == "flash"):
                print("[i] The NovaPi will stop and will enter flash mode")
                while True:
                    continue
            else:
                print("[W] That is not a valid command!")

        print("Program exit (Novapi will start flashing)")

import _thread
#import novapi
#import machine
import time
import os


# Init class
CHALLENGE_DEFAULT_MBUILD_CONFIGURATOR = {
    "name": "default_port",
    "type": "ranging_sensor",
    "indict": dict,
    "port": 1,
    "index": 1
}
# Init variables
CHALLENGE_DEFAULT_RUNTIME_FILE = './challenge_default.py'
CHALLENGE_DEFAULT_MBUILD_FILE = "./sensors.json"


#system.loadme()
system.loadlogo()
_thread.start_new_thread(system.uiinput, 0, [])
