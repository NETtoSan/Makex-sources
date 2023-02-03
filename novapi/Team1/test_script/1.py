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
        except ValueError:
            print("> That color DOES NOT exist")

class auto(object):
    def __init__ (self):
        self.lights = led_lights() #simulate_lights

    def modes(self,prompt):
        self.lights.set_rgb_color("cyan")
def ask():
    print("\n----------- NETto!_NS Bootloader")
    prompt = input(f"Choose scenarios to test\n{' , '.join(modes)}\n")
    return prompt

while True:
    prompt  = ask()
    print(f"Keywords prompted: {prompt}")
    auto_test = auto()
    auto_test.modes(prompt)
