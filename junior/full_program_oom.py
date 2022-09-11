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
        pass


class Manual:
    def __init__(self):
        pass


# Preferences program, Use to edit or set component's ports
class Preferences:
    def __init__(self):
        pass
