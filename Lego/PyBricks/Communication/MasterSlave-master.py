# https://www.sato-susumu.com/entry/lego_robo_ms
from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor
from pybricks.parameters import Port
from pybricks.tools import wait

hub = PrimeHub(broadcast_channel=1, observe_channels=[2])
motors = [Motor(Port.B), Motor(Port.C), Motor(Port.D), Motor(Port.E), Motor(Port.F)]

while True:
    angles = [motor.angle() for motor in motors]

    hub.ble.broadcast(tuple(angles))
    wait(10)
