#http://www.inpharmix.com/jps/PID_Controller_For_Lego_Mindstorms_Robots.html
#https://thecodingfun.com/2020/06/16/lego-mindstorms-ev3-pid-line-follower-code-by-using-micropython-2-0/

def color_calibration():
  sensor = ColorSensor(Port.F)
  while not any(hub.buttons.pressed()):
    continue
  wait (1000)
  white_color = sensor.reflection()
  print(f"white color: {white_color}")
  while not any(hub.buttons.pressed()):
    continue
  wait(1000)
  black_color = color_sensor.reflection()
  print(f"black-color:", black_color)
  return (white_color, black_color)

WHITE_COLOR = 95
BLACK_COLOR = 16
SPEED = 46
KP = 0.25


def follow_line_3stage():
  motor_left = Motor(Port.A, Direction.COUNTERCLOCKWISE)
  motor_right = Motor(Port.D, Direction.CLOCKWISE)
  sensor = ColorSensor(Port.F)
  threshold_1 = int((WHITE_COLOR-BLACK_COLOR) / 3)+BLACK
  threshold_2 = WHITE_COLOR - int((WHITE_COLOR-BLACK_COLOR) / 3)
  
  while True:
    wait(1)
    refl = sensor.reflection()
    if (refl <= threshold_1):
      error = (refl - threshold_1) * KP
      motor_right.dc(SPEED + error)
      motor_left.dc(SPEED - error)
    elif (refl >= threshold_2):
      error = (refl - threshold_2) * KP
      motor_right.dc(SPEED - error)
      motor_left.dc(SPEED + error)
    else:
      motor_right.dc(SPEED)
      motor_left.dc(SPEED)

KI = 0.25
KD = 1.0
def follow_line_3stage_pid():
  motor_left = Motor(Port.A, Direction.COUNTERCLOCKWISE)
  motor_right = Motor(Port.D, Direction.CLOCKWISE)
  sensor = ColorSensor(Port.F)
  threshold_1 = int((WHITE_COLOR-BLACK_COLOR) / 3)+BLACK
  threshold_2 = WHITE_COLOR - int((WHITE_COLOR-BLACK_COLOR) / 3)

  integral = 0
  derivative = 0
  last_error = 0
  error = 0
  while True:
    wait(1)
    refl = sensor.reflection()
    
    if (refl <= threshold_1):
      error = (refl - threshold_1)
      integral = integral + error
      derivative = error - last_error
      turn_rate = error * KP + integral * KI + derivate * KD
      
    elif (refl >= threshold_2):
      error = (refl - threshold_2)
      integral = integral + error
      derivative = error - last_error
      turn_rate = (error * KP + integral * KI + derivate * KD)*-1
      
    else:
      error = 0
      integral = 0
      derivative = 0
      motor_right.dc(SPEED)
      motor_left.dc(SPEED)
    
    motor_right.dc(SPEED + turn_rate)
    motor_left.dc(SPEED - turn_rate)
    last_error = error
