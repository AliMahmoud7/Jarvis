from time import sleep
try:
    import RPi.GPIO as GPIO
except:
    PI = False
from features.respond.tts import tts

# Light colors with Pin numbers
"""
Red >> PIN 11
Blue >> PIN 10
Green >> PIN 9
Yellow >> PIN 8
"""


def setup_GPIO():
    """
    Setup GPIO Pins for outputs or inputs
    """
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(11, GPIO.OUT)


def control_light(action, light_color=None):
    """
    Control lights using raspberry pi
    :param action:
    :param light_color:
    :return:
    """
    if not PI:
        tts("I can't find the raspberry pi to do the control actions")
        return None
    setup_GPIO()
    if action == 'on':
        if light_color == 'red':
            GPIO.output(11, True)
        elif light_color == 'blue':
            GPIO.output(10, True)
        elif light_color == 'green':
            GPIO.output(9, True)
        elif light_color == 'yellow':
            GPIO.output(8, True)
        else:
            GPIO.output(11, True)
            GPIO.output(10, True)
            GPIO.output(9, True)
            GPIO.output(8, True)
    elif action == 'off':
        if light_color == 'red':
            GPIO.output(11, False)
        elif light_color == 'blue':
            GPIO.output(10, False)
        elif light_color == 'green':
            GPIO.output(9, False)
        elif light_color == 'yellow':
            GPIO.output(8, False)
        else:
            GPIO.output(11, False)
            GPIO.output(10, False)
            GPIO.output(9, False)
            GPIO.output(8, False)
    else:
        tts('You should tell me explicitly to turn on or off the lights')
