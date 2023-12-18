from pybricks.pupdevices import Motor
from pybricks.parameters import Direction, Port
from pybricks.robotics import DriveBase
from pybricks.tools import multitask, run_task
from pybricks.hubs import InventorHub
from pybricks.tools import wait, StopWatch, hub_menu
from pybricks.parameters import Button

import menu

# Set up all devices.
hub = InventorHub()
motor_left = Motor(Port.C, Direction.COUNTERCLOCKWISE)
motor_right = Motor(Port.D,Direction.CLOCKWISE)
motor_attach_left = Motor(Port.A)
motor_attach_right = Motor(Port.B)
drivebase = DriveBase(left_motor = motor_left, right_motor=motor_right,
wheel_diameter = 55.6, axle_track = 83.8)

async def slot1(hub, drivebase, motor_attach_left, motor_attach_right):
    await multitask(motor_attach_left.run_angle(500, -360)
    , motor_attach_right.run_angle(500, -360))
    
    await multitask(motor_attach_left.run_angle(500, 360),
    motor_attach_right.run_angle(500, 360))


async def slot2(hub, drivebase, motor_attach_left, motor_attach_right):
    await multitask(motor_attach_left.run_angle(500, 360)
    , motor_attach_right.run_angle(500, 360))
    
    await multitask(motor_attach_left.run_angle(500, -360),
    motor_attach_right.run_angle(500, -360))

menu_options = ("1", "2")
cur_menu_index = 0

while True:
    try:
        selected, cur_menu_index =  do_menu(hub,menu_options,cur_menu_index) # hub_menu("1","2")
        if selected == "1":
            run_task(slot1(hub, drivebase, motor_attach_left, motor_attach_right))
        elif selected == "2":
            run_task(slot2(hub, drivebase, motor_attach_left, motor_attach_right))
        else:
            break
    except SystemExit:
        '''if center button is pressed while code is running, it will
        raise a SystemExit exception. We dont want the entire code to stop. 
        Instead we capture the exception, stop the drivebase and motors
        and allow the menu to be represented
        '''
        drivebase.stop()
        motor_left.stop()
        motor_right.stop()
        hub.speaker.beep(frequency=1, duration = 50)
        while hub.buttons.pressed():
            wait(100) # wait for button to be released
