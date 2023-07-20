import time, keyboard, math

# acel
ax = 100
ay = 100

# heading; 
default_heading = 90
cur_bot = 45 # Current bot heading from 0
heading = ((default_heading - cur_bot) * math.pi) / 180

start_time = time.time()
last_time = time.time()

# traveled distance
x = 0
y = 0


while True:
    time.sleep(0.01)
    time_now = time.time()

    if keyboard.is_pressed("q"):
        heading -= 1
    if keyboard.is_pressed("e"):
        heading += 1

    delta_time = float(f'{(time_now - last_time):.2f}')
    time_elapsed = float(f'{(time_now - start_time):.2f}')
    vx = ax * delta_time
    vy = ay * delta_time


    vx_world = ((vx * math.cos(heading)) - (vy * math.sin(heading)))
    vy_world = ((vx * math.sin(heading)) + (vy * math.cos(heading)))

    x += float(f'{(vx_world * delta_time):.3f}')
    y += float(f'{(vy_world * delta_time):.3f}')

    last_time = time_now
    print(f"[{delta_time}] | vx: {vx} vy:{vy} heading:{cur_bot} | xw: {vx_world:.1f} yw: {vy_world:.1f} | total_x: {x:.3f} total_y: {y:.3f}")