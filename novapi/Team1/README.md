# 2022 Makex Challenge
This MakeX competition is another competition we have joined after winning the local XMaker's Explorer kind of thing. **However**, with the lack of parts, fundings, virtually everything, we have to come up with different methods of trying out new ideas.
____
## What the bot must do
**[1] The easiest yet them all is to propel the yellow balls in the stage with high accuracy. And to have high gun elevation/ depression.**\
**[2] Another one is to have relatively big and efficient arm in which to grab the cubes at the middle row easily.**\
**[3] It's also nice to add some sensors, specially the one that can measure range and a camera to help players aim the opponent's target**

## The ideas
The ideas we've tried for this 2022's MakeX Challenge is.... I'd say **A lot** for a short amount of time.

**> This is what we've come up to try out so far <\
[1] Holonomic X Drive\
[2] Rubber wheel brushless motor technique\
[3] Temporary ball stowage\
[4] Fully automatic automatic program\
[5] Accelerometer dependant and odometry for automatic program**
> [1] The Holonomic X Drive is an improvisation we have to face with very limiting resources. We do not have mecanum wheels. And have to use these 4 omniwheels to work with a code that's designed for mecanum wheels.\
[2] The rubber wheel brushless motor technique is also another improvisation we came up with to counteract with lack of parts. Which also introduced a Flywheel into a competition. We can propel the balls efficiently with just 10% of the motor's power.\
[5] Yeah we got tired to time each movement's in seconds. Luckily not with floating numbers for the sake of accuracy. So we just let the bot complete its mission on its own

____

# The code
This folder consists of\
**[1] An actual code we used in the competition `./test_manual`\
[2] A simulator when we dont have a bot on hand. `./simulator`\
[3] A code where we test each sensors and the bot's efficiency in completing each tasks. Especially the ones that it has to move in x,y coordinates `./test_auto`**
>*!!! The code that contains the movement in x,y coordinates is not in `./test_auto` because we do not have the robot anymore. If you wanted to see its currently unfinished code please head to `./simulator/pure_persuit.py`*
____

# The Novapi connections
- **Encoder motor**\
**These wheel configs are used both for omniwheels and mecanum wheels**\
EM1: Front left wheel\
EM2: Front right wheel\
EM3: Rear left wheel\
EM4: Rear right wheel\
**DC ports are used to power the motors and other peripherals**\
DC1: Unknown\
DC2: Unknown\
DC3: Unknown\
DC4: Unknown\
DC5: Unknown\
DC6: Unknown\
DC7: Unknown\
DC8: Unknown\
**MBuild ports are used to connect its smarts**\
I forgot how many mbuilds ive used.

**! Please head to `./test_manual/hawkeye_main_program.py` and find out for yourself !**
____
**More information coming soon i'm trying to remember what i've done to this repository**