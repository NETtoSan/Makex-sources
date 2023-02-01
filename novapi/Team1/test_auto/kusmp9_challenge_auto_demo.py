import novapi , time

cube_distance = ranging_sensor_1.get_value()

# BOT ---------> CUBE : 1cm
while cube_distance > 3:
    move(-50,50,50,-50)
    cube_distance = ranging_sensor_1.get_value()

move(0,0,0,0)
grab_cube()