from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor
from pybricks.parameters import Port, Stop
from pybricks.tools import wait

hub = PrimeHub(broadcast_channel=2, observe_channels=[1])
motors = [Motor(Port.B), Motor(Port.C), Motor(Port.D), Motor(Port.E), Motor(Port.F)]
last_angles = [999, 999, 999, 999, 999]

while True:
    data = hub.ble.observe(1)

    if data is not None:
        for i in range(len(motors)):
            if abs(data[i] - last_angles[i]) >= 1:
                motors[i].run_target(500, data[i], then=Stop.HOLD, wait=False)
                last_angles[i] = data[i] 

    wait(10)
