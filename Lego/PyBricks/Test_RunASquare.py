# ('primehub', '3.2.2', 'v3.2.2 on 2023-01-06')

from pybricks.hubs import InventorHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch

hub = InventorHub()

#left_motor = Motor(Port.B, Direction.COUNTERCLOCKWISE)
#right_motor = Motor(Port.A,Direction.CLOCKWISE)

left_motor = Motor(Port.B, Direction.CLOCKWISE)
right_motor = Motor(Port.A,Direction.COUNTERCLOCKWISE)

drive_base = DriveBase(left_motor, 
    right_motor, 
    wheel_diameter = 56,
    axle_track= 80)

turn_angle = -90
length = 355.5
width = 355.5

for i in range(1):
    drive_base.straight(length/2.0)
    print(f"{drive_base.distance()} {drive_base.angle()}")
    
    drive_base.turn(turn_angle)
    drive_base.straight(width)
    print(f"{drive_base.distance()} {drive_base.angle()}")

    drive_base.turn(turn_angle)
    drive_base.straight(length)
    print(f"{drive_base.distance()} {drive_base.angle()}")

    drive_base.turn(turn_angle)
    drive_base.straight(width)
    print(f"{drive_base.distance()} {drive_base.angle()}")

    drive_base.turn(turn_angle)
    drive_base.straight(length/2.0)
    print(f"{drive_base.distance()} {drive_base.angle()}")
