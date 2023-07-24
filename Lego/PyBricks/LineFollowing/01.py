# https://github.com/orgs/pybricks/discussions/149#discussioncomment-212436
# with Laurens Valk tips
# for Proportional control and COUNTERCLOCKWISE option

from pybricks.hubs import PrimeHub
from pybricks.parameters import Port, Color, Direction, Button
from pybricks.pupdevices import Motor, ColorDistanceSensor
from pybricks.tools import wait

hub = PrimeHub()
mL = Motor(Port.E, Direction.COUNTERCLOCKWISE)
mR = Motor(Port.F)
s = ColorDistanceSensor(Port.A)

SPEED = 95
TIME = 1
THRESHOLD = 55
KP = 2.5

# wait for LEFT button to be pressed
while True:
    if hub.buttons.pressed() == [Button.LEFT] :
        break
    wait(10)

while True:
    wait(TIME)
    v = s.reflection()
    print(v)
    steering = (v - THRESHOLD) * KP
    mR.dc(SPEED + steering)
    mL.dc(SPEED - steering)
