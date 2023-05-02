https://docs.pybricks.com/en/latest/robotics.html#driving-straight-and-turning-in-place

**Measuring and validating the robot dimensions**

As a first estimate, you can measure the wheel_diameter and the axle_track with a ruler. Because it is hard to see where the wheels effectively touch the ground, you can estimate the axle_track as the distance between the midpoint of the wheels.

If you don’t have a ruler, you can use a LEGO beam to measure. The center-to-center distance of the holes is 8 mm. For some tyres, the diameter is printed on the side. For example, 62.4 x 20 means that the diameter is 62.4mm and that the width is 20 mm.

In practice, most wheels compress slightly under the weight of your robot. To verify, make your robot drive 1000 mm using my_robot.straight(1000) and measure how far it really traveled. 

**Compensate as follows:**

If your robot drives not far enough, decrease the wheel_diameter value slightly.

If your robot drives too far, increase the wheel_diameter value slightly.

Motor shafts and axles bend slightly under the load of the robot, causing the ground contact point of the wheels to be closer to the midpoint of your robot. 
To verify, make your robot turn 360 degrees using my_robot.turn(360) and check that it is back in the same place:

If your robot turns not far enough, increase the axle_track value slightly.

If your robot turns too far, decrease the axle_track value slightly.

When making these adjustments, always adjust the wheel_diameter first, as done above. Be sure to test both turning and driving straight after you are done.


```python
from pybricks.pupdevices import Motor
from pybricks.parameters import Port, Direction
from pybricks.robotics import GyroDriveBase

# Initialize both motors. In this example, the motor on the
# left must turn counterclockwise to make the robot go forward.
left_motor = Motor(Port.A, Direction.COUNTERCLOCKWISE)
right_motor = Motor(Port.B)

# Initialize the drive base. In this example, the wheel diameter is 56mm.
# The distance between the two wheel-ground contact points is 112mm.
drive_base = GyroDriveBase(left_motor, right_motor, wheel_diameter=56, axle_track=112)

# Drive forward by 500mm (half a meter).
drive_base.straight(500)

# Turn around clockwise by 180 degrees.
drive_base.turn(180)

# Drive forward again to get back to the start.
drive_base.straight(500)

# Turn around counterclockwise.
drive_base.turn(-180, then=Stop.COAST)
```

[GyroDriveBase](https://docs.pybricks.com/en/latest/robotics.html#pybricks.robotics.GyroDriveBase)
This class works just like the DriveBase, but it uses the hub’s built-in gyroscope to drive straight and turn more accurately.

If your hub is not mounted flat in your robot, make sure to specify the top_side and front_side parameters when you initialize the PrimeHub(), InventorHub(), EssentialHub(), or TechnicHub(). This way your robot knows which rotation to measure when turning.

The gyro in each hub is a bit different, which can cause it to be a few degrees off for big turns, or many small turns in the same direction. For example, you may need to use turn(357) or turn(362) on your robot to make a full turn.

By default, this class tries to maintain the robot’s position after a move completes. This means the wheels will spin if you pick the robot up, in an effort to maintain its heading angle. To avoid this, you can choose then=Stop.COAST in your last straight, turn, or curve command.
