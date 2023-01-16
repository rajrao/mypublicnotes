**Template**
```python
from mindstorms import MSHub, Motor, MotorPair, ColorSensor, DistanceSensor, App
from mindstorms.control import wait_for_seconds, wait_until, Timer
from mindstorms.operator import greater_than, greater_than_or_equal_to, less_than, less_than_or_equal_to, equal_to, not_equal_to
import math

# Create your objects here.
hub = MSHub()

# Write your program here.
hub.speaker.beep()
```

**Using Random**
```python
from mindstorms import MSHub, ColorSensor
from random import randint

hub = MSHub()

# Create a random number between 1 and 10
random_number = randint(1, 10)
# Check if the random number is greater than 5, less than 5 or equal to 5
if random_number > 5 :
    hub.light_matrix.write( 'Random number > 5')
elif random_number < 5:
    hub.light_matrix.write( 'Random number < 5')
else :
    hub.light_matrix.write( 'Random number = 5')
```
**Imports**
```python
from mindstorms import MSHub, Motor, MotorPair, ColorSensor, DistanceSensor, App
from mindstorms.control import wait_for_seconds, wait_until, Timer
from mindstorms.operator import greater_than, greater_than_or_equal_to, less_than, less_than_or_equal_to, equal_to, not_equal_to
import math
```

**Objects**
```python
# Initialize the hub.
hub = MSHub()
# Initialize the motors connected to Ports A and B.
motor_a = Motor('A')
motor_b = Motor('B')
# Initialize the Color Sensor connected to Port C.
color_sensor = ColorSensor('C')
# Initialize the Distance Sensor connected to Port D.
distance_sensor = DistanceSensor('D')
```

**Using Console**
```python
my_variable = 0
print('This text will be displayed in the console.')
print('my_variable:', my_variable)
```

**Controlling Lights**
```python
# Import the MSHub class.
from mindstorms import MSHub
from mindstorms.control import wait_for_seconds
# Initialize the Hub.
hub = MSHub()
# Show a smiley face for five seconds.
hub.light_matrix.show_image('HAPPY')
wait_for_seconds(5)
hub.light_matrix.off()
```

**Light Matrix #1**
```python
from mindstorms import MSHub
from mindstorms.control import wait_for_seconds

hub = MSHub()

# the For loop goes through all the character of the Mindstorms text
for character in 'Mindstorms':
    hub.light_matrix.write(character)
    wait_for_seconds(0.8)
```

**Light Matrix #2**
```python
# The method show_image() has a parameter called 'HAPPY.'
my_own_hub_object.light_matrix.show_image('HAPPY')
# The method stop() has no parameter.
motor.stop()
```

**Running Motor**
```python
# Import the Motor class.
from mindstorms import Motor
# Initialize the motor connected to Port A.
motor = Motor('A')
# Rotate clockwise for 2 seconds at 75% speed.
motor.run_for_seconds(2.0, 75)
```

**Running Motor for Degrees**
```python
# Import the Motor class.
from mindstorms import Motor
# Initialize the motor connected to Port A.
motor = Motor('A')
# Rotate the motor 360 degrees clockwise.
motor.run_for_degrees(360)
```

**Motor #3**
```python
# Import the Motor class.
from mindstorms import Motor
from mindstorms.control import wait_for_seconds
# Initialize the motor connected to Port A.
motor = Motor('A')
# Run the motor to position “0,” aligning the markers.
motor.run_to_position(0, 'shortest path', 75)
```

**Motor #4**
```python
# Run the motor to different positions, at different speeds.
wait_for_seconds(1)
motor.run_to_position(0, 'shortest path', 30)
wait_for_seconds(1)
motor.run_to_position(90, 'clockwise', 100)
```
**Color Sensor #1**
```python
from mindstorms import ColorSensor, Motor
from mindstorms.control import Timer
# Initialize the Color Sensor, two motors, and a timer.
color_sensor = ColorSensor('C')
motor_a = Motor('A')
motor_b = Motor('B')
timer = Timer()
# Present each colored beam to the Color Sensor and observe what happens.
# It will detect colors for 30 seconds.
while timer.now() < 30:
    color = color_sensor.wait_for_new_color()
    if color == 'red':
        motor_a.run_for_rotations(1)
    elif color == 'yellow':
        motor_b.run_for_rotations(1)
```

**Color Sensor #2**
```python
# This will use the reflected value of the colors to set the power of the motors.
# Yellow is approximately 80% and red approximately 60%.
while True:
    color = color_sensor.get_color()
    percentage = color_sensor.get_reflected_light()
    if color == 'red':
        motor_a.start_at_power(percentage)
    elif color == 'yellow':
        motor_b.start_at_power(percentage)
    else:
        motor_a.stop()
        motor_b.stop()
```

**Distance Sensor #1**
```python
from mindstorms import DistanceSensor, Motor
# Initialize the Distance Sensor and motor.
distance_sensor = DistanceSensor('D')
motor = Motor('A')
# Move your hand slowly toward and away from the Distance Sensor.
while True:
    distance_sensor.wait_for_distance_farther_than(20, 'cm')
    motor.start()
    distance_sensor.wait_for_distance_closer_than(20, 'cm')
    motor.stop()
```

**Distance Sensor #2**
```python
# Move your hand slowly toward and away from the Distance Sensor.
# The motor speed will change based on the distance detected.
while True:
    percentage = distance_sensor.get_distance_percentage()
    if percentage is not None:
        motor.start(100 - percentage)
    else:
        motor.stop()
```
**Motion Sensor #1**
```python
# Import the MSHub and App classes.
from mindstorms import MSHub, App
# Initialize the MSHub and the App.
hub = MSHub()
app = App()
while True:
    orientation = hub.motion_sensor.wait_for_new_orientation()
    if orientation == 'front':
        hub.light_matrix.show_image('ASLEEP')
        app.start_sound('Snoring')
    elif orientation == 'up':
        hub.light_matrix.show_image('HAPPY')
        app.start_sound('Triumph')
```
**Motion Sensor #2**
```python
while True:
    angle = abs(hub.motion_sensor.get_pitch_angle()) * 2
    hub.light_matrix.show_image('HAPPY', angle)
```

**Driving #1**
```python
from mindstorms import MotorPair
# Initialize the motor pair.
motor_pair = MotorPair('A', 'B')
# Initialize the default speed.
motor_pair.set_default_speed(50)
# Move in one direction for 2 seconds.
motor_pair.move(2, 'seconds')
```

**Driving #2**
```python
# Move in the other direction for 2 seconds.
motor_pair.set_default_speed(-50)
motor_pair.move(2, 'seconds')
```

**Driving #3 Point Turn**
```python
from mindstorms import MotorPair
# Initialize the motor pair.
motor_pair = MotorPair('A', 'B')
# Turn in one direction for 10 centimeters.
motor_pair.move_tank(10, 'cm', left_speed=75, right_speed=-75)
```

**Driving #4**
```python
# Move in the other direction for one rotation.
motor_pair.move_tank(1, 'rotations', left_speed=-50, right_speed=50)
```

**Word Blocks**

**Beep**
```python
hub.speaker.beep(60, 0.2)
```
**Play Sound**
```python
app.play_sound('Cat Meow 1')
```
**Light Matrix**
```python
hub.light_matrix.show_image('HAPPY')
wait_for_seconds(2)
hub.light_matrix.off()
```
**Motor**
```python
motor = Motor('A')
motor.run_for_seconds(1, 75)
```
**Motor #2**
```python
motor_pair = MotorPair('A', 'E')
motor_pair.move_tank(1, 'rotations', -75, 75)
```
**Motor #3**
```python
motor_pair = MotorPair('A', 'B')
motor_pair.set_default_speed(50)
motor_pair.move(10, 'cm')
```
**Distance #1**
```python
distance_sensor = DistanceSensor('D')
distance_sensor.wait_for_distance_closer_than(15, 'cm')
```
**Wait for** 
```python
wait_for_seconds(2)
```
**Repeat**
```python
for count in range(10):
    hub.light_matrix.write(count)
    wait_for_seconds(1)
```

**If Else**
```python
color_sensor = ColorSensor('A')
color = color_sensor.wait_for_new_color()
if color == 'yellow':
    print('Yellow')
else:
    print('Not Yellow')
```

**Sample**
```python
from mindstorms import MSHub, MotorPair, DistanceSensor
from mindstorms.control import wait_for_seconds

hub = MSHub()
motor_pair = MotorPair('A', 'B')
distance_sensor = DistanceSensor('D')

distance_sensor.light_up_all()
motor_pair.set_default_speed(80)
hub.light_matrix.show_image('GO_RIGHT')
wait_for_seconds(2)
hub.light_matrix.off()
motor_pair.move(10, 'cm')
```

**Sound**
```python
from mindstorms import App

app = App()

app.start_sound('Cat Meow 1')
wait_for_seconds(0.5)
app.stop_sound()
```
