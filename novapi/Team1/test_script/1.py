import time

# RESOURCES
modes = ["cube", "test"]

class led_lights():
    def __init__ (self):
        pass
    def set_rgb_color(self,col):
        color = ["red", "green", "blue"]
        try:
            color.index(col)
            print(f"> Setting rgb color to {col}")
        except ValueError:
            print("> That color DOES NOT exist")

class encode_motor():
    def __init__ (self):
        pass
    def set_speed(speed):
        print(f"setting motor at {speed}%")

# BOT CORE
class auto():
    def __init__ (self):
        self.lights = led_lights() #simulate_lights

    def modes(self,prompt):
        self.lights.set_rgb_color("cyan")
        time.sleep(2)
        print("Set motor speed to 50,-50,50,-50 (fwd) for 1 sec")
        time.sleep(1)
        print("Set motor speed to -50,50,-50,50 (rlf) for 1 sec")
        time.sleep(1)

        print("> Auto code done <\n")

# FUNCTIONS
print("----------- NETto!_NS Bootloader") 
def ask():
    prompt = input(f"Choose scenarios to test\n{' , '.join(modes)}\n")
    return prompt

while True:
    prompt  = ask()
    print(f"Keywords prompted: {prompt}")
    auto_test = auto()
    auto_test.modes(prompt)
