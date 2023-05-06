#from https://docs.pybricks.com/en/latest/robotics.html?highlight=Drivebase

from pybricks.pupdevices import Motor
from pybricks.parameters import Port, Direction
from pybricks.robotics import DriveBase

# Initialize both motors. In this example, the motor on the
# left must turn counterclockwise to make the robot go forward.
left_motor = Motor(Port.A, Direction.COUNTERCLOCKWISE)
right_motor = Motor(Port.B)

# Initialize the drive base. In this example, the wheel diameter is 56mm.
# The distance between the two wheel-ground contact points is 112mm.
drive_base = DriveBase(left_motor, right_motor, wheel_diameter=56, axle_track=112)

# Drive forward by 500mm (half a meter).
drive_base.straight(500)

# Turn around clockwise (180 degrees)
drive_base.turn(180)

# Drive forward again to drive back.
drive_base.straight(500)

# Turn around counterclockwise.
drive_base.turn(-180)

#drive with a speed of 300
drive_base.drive(300,0)
wait(1500)
drive_base.drive(300,150)
wait(1500)


#using settings
drive_base.settings(
    straight_speed=500,
    straight_acceleration=1000,
    turn_rate=500,
    turn_acceleration=2000
)

