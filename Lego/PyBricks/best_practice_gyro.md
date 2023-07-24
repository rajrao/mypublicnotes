**Best Practice 1: Use Stop** (https://github.com/pybricks/support/issues/989#issuecomment-1474781023)

```python
hub.imu.reset_heading(0)

do_mission_one()

drive_base.stop()   # <--- This will stop the robot from trying to keep up with the last commanded gyro angle

# prep robot for next mission

# put it back down / position it / wait for button

hub.imu.reset_heading(0)

do_mission_two()

drive_base.stop()

# prep robot for next mission

# put it back down / position it / wait for button

# and so on
```


**Best Practice 2: How to wait for button**

```python
# wait for any button to be pressed
while not any(hub.buttons.pressed()):
    wait(10)
```






**Tips**

**Menu**
Now available as an inbuilt option: https://github.com/pybricks/pybricks-api/issues/144. But here is how you can code a menu: https://github.com/pybricks/support/issues/861#issue-1499778720
