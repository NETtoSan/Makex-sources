import time

origin = 0

def dest(target):
    global origin
    error = target - origin
    print(f"Target: {target} | Origin: {origin} | Error: {error}")
    time.sleep(1)
    origin = target



dest(0)
dest(90)
dest(180)
dest(0)