import time
import random

# ------ PID -------- #
kp = 1.5 #11
ki = 1 #4.2
kd = 0 #92
# ------ PID -------- #

integral = 0
error = 0
derivative = 0
prev_error = 0
result = 0
ks = -0.6
start = 0

now_angle = 0 # novapi.get_angle(any_novapi_orientation)
target_angle = random.randint(-180,180) # Use this on odometry target ./simulator/pure_persuit.py
curve = 0.01 # Adjust power to devices for each distance


# ------ STATS -------- #
stats = []
# ------ STATS -------- #

def constrain(v,mn,mx):
    if v < mn : return mn
    if v > mx : return mx
    return v

def power(s, t):
    global integral, prev_error
    

    # This is where PID is
    # DO NOT mess with it unless actual testings aren't working

    error = t - s
    integral = integral + (error * 0.25)
    derivative = error - prev_error
    prev_error = error
    start = (s - t)
    tpower = (error * kp) + (integral*ki) + (derivative*kd)  + (start*ks)

    # Limit values between -100 and 100
    tpower = constrain(tpower, -100, 100)
    return int(tpower)


print(f"START----------\ntarget: {target_angle} && start: {now_angle}\nrot_speed: 0\n----------\n")
while target_angle != now_angle:
    motor_power = power(now_angle, target_angle)
    now_angle += round(target_angle + motor_power)
    stats.append(now_angle)
    print(f"target: {target_angle} && now: {now_angle}\nrot_speed: {motor_power}\n--")
    time.sleep(0.5)