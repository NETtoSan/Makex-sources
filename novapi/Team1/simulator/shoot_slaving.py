'''
shoot slaving
<-- L:0 R:100     | L:100 R: 100 |     L:100 R:0 -->

camera slaved
            [pin]
              |      what we know: [1] cam target angle
              |                    [2] target distance
[cam]       [gun]                  [3] distance from cam to gun

: distance from pin to gun
[1] distance pingun = sqrt(camgun^2 + campin^2 - 2 * camgun * campin * cos(campinangle))
[2] angle to aim = 2 *   ( finish the equations for me pls )
'''
# This is a pseudocode. Adapt this to your robot config manually.

# change this to your motherboard config
cam     = 0       # The camera
mot_l   = 0       # The motors
mot_r   = 0 

# Seeker setup
prepare = False   # Spooling up the camera only requires once!
caged = False     # Caged   = The camera stays in fixed position
                  # Uncaged = The camera has its own gimbal system to track objects
servo_x = 0       # The servos are for the camera gimbal setup
servo_y = 0

cam_res_x = 0
cam_res_y = 0

tgt_x = 0         # The target orientation
tgt_y = 0

gun_l   = 0       # Values for controlling each propelling motor
gun_r   = 0

# Readying up the camera apon boot
def spool_cam():
    if caged == False:
        if prepare == False:
            # Center the cam gimbal
            servo_x.move_to(0); servo_y.move_to(0)
            
            # If the camera have the gyroscope. enter the servos until the camera is centered
            if cam.gyro != None:
                while cam.gyro.pitch != 0 and cam.gyro.yaw != 0:
                    pitch_error = servo_y.angle - cam.gyro.pitch
                    yaw_error = servo_x.angle - cam.gyro_yaw
                    servo_y.move(pitch_error); servo_x.move(yaw_error)

            prepare = True  # Tells the system that the camera has spooled up

# Track the target
def track_target():
    # Put this in a while loop or a separate thread!

    # Saves coord to the variable
    sig_x = cam.sig_x()    # Refer this to your camera config
    sig_y = cam.sig_y()    # The function should be similar

    if sig_x == 0 or sig_y == 0:
        servo_x.move_to(0); servo_y.move_to(0)
    else:
        # Center out the camera's resolution
        center_x = cam_res_x / 2
        center_y = cam_res_y / 2

        # Track objects
        if sig_x != center_x or sig_y != center_y:
            # Calculate the error
            tgt_err_x = center_x - sig_x
            tgt_err_y = center_y - sig_y


            # If the camera doesnt utilize gimbals for tracking objects
            if caged == True:
                tgt_x = tgt_err_x; tgt_y = tgt_err_y
            else:
                servo_y.move(tgt_err_y); servo_x.move(tgt_err_x)
                tgt_x = servo_x.angle; tgt_y = servo_y.angle

            # use the tgt_x and tgt_y to control your gun if you're using it to assist aiming the targets