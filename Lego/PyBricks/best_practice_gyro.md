https://github.com/pybricks/support/issues/989#issuecomment-1474781023

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
