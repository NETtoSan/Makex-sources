import cyberpi

# Reduce modes needed to run the program. Must rely on color sensors to detect whether there is a cube or not.
modes = ["Auto program left", "Auto program right", "Preferences"]


# Ports needed to run this project. Refer to SERVOS -> DRIVEMOTOR -> DCMOTOR
# SERVOS consists of ARMS, ARM-ROTATE, ARM-UPDOWN, GUN-MECHANISM
# DRIVEMOTOR consists of MOTOR-LEFT, MOTOR-RIGHT
# DCMOTOR consits of MOTOR-SHOOT, not set
ports = ["S1", "S2", "S3", "S4", "EM1", "EM2", "M1", "M2"]


class Start:
    def __init__(self):
        pass


class Auto:
    def __init__(self):
        self.cube = False
        self.sides = "Left"  # Default sides to left

    def FollowLine(r, s):
        pass

    def grabCube(s):
        pass

    def grabBall(s):
        pass


class Math:
    def __init__(self):
        self.seconds = 3  # Default operation to 3 seconds
        self.speed = 50  # Set default speed to 50%

    def calcspeed(s):
        return 0


class Manual:
    def __init__(self):
        pass

    def shoot():
        pass

    def reload(s):
        pass


# Preferences program, Use to edit or set component's ports
class Preferences:
    def __init__(self):
        pass

    def on_screen(p):
        pass
    def get_values(v):
        pass
