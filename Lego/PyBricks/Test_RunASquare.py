from pybricks.hubs import InventorHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch

hub = InventorHub()

left_motor = Motor(Port.B, Direction.CLOCKWISE)
right_motor = Motor(Port.A,Direction.COUNTERCLOCKWISE)

drive_base = DriveBase(left_motor, 
    right_motor, 
    wheel_diameter = 56,
    axle_track= 80)

for i in range(1):
    drive_base.straight(177.5)
    drive_base.turn(-90)
    drive_base.straight(355.5)
    drive_base.turn(-90)
    drive_base.straight(355.5)
    drive_base.turn(-90)
    drive_base.straight(355.5)
    drive_base.turn(-90)
    drive_base.straight(177.5)
