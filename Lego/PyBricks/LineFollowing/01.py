# The original code came from https://github.com/orgs/pybricks/discussions/149#discussioncomment-212436
# with Laurens Valk tips for Proportional control and COUNTERCLOCKWISE option
# it was modified by my kid to work with Spike Prime/Robot Inventor with some notes added by her and me.

from pybricks.hubs import InventorHub
from pybricks.pupdevices import Motor, ColorSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch

hub = InventorHub()
# change the Directions for the motors below to make sure the robot moves
# in the correct direction

motor_left = Motor(Port.A, Direction.COUNTERCLOCKWISE)
motor_right = Motor(Port.D,Direction.CLOCKWISE)

motor_attach_left = Motor(Port.C, Direction.CLOCKWISE,gears=[20,12])
motor_attach_right = Motor(Port.B, Direction.CLOCKWISE,gears=[20,12])
sensor = ColorSensor(Port.F)

# line following is done by following the edge of the black line (where it meets the white border)
# place the robot sensor on top of edge of the black and white area before you start the robot
# threshold represents the reflection value at this border/threshold
THRESHOLD = 55

# You need to tweak these settings for your robot and the amount of light in your area
# Higher KP (constant of proportion values) will make the robot turn more while looking for the threshold
# Faster speeds can cause the robot to loose the threshold easier.
# you are trying to find the highest speed with the lowest KP that allows your robot to track the line
SPEED = 46
KP = 0.25 # constant of proportion

#30, 0.25 - 46, 0.25 work

while True:
    wait(1)
    refl = sensor.reflection()
    error = (refl - THRESHOLD) * KP
    print(f"reflection: {refl} error: {error}")
    motor_right.dc(SPEED + error)
    motor_left.dc(SPEED - error)


# The algorithm used here is a PD algorithm (as opposed to PID).
# proportional–integral–derivative. Its just a fancy way to say, the 
# robot will try and move proportionally (KP*error) to how far it thinks its away from the threshold (the error)
# as there is no accumulation of the error, there is no I in this implementation.
# for more information: https://blog.aggregatedintelligence.com/2022/06/error-correction-using-pid-proportional.html
