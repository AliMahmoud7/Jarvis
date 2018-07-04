import time
from app.views.features.respond.tts import tts

try:
    import RPi.GPIO as GPIO
    PI = True
except:
    PI = False

# Light colors with Pin numbers

# Define global Pins
RED_PIN = 11
GREEN_PIN = 13
YELLOW_PIN = 15
BLUE_PIN = 19

# Setup GPIO Pins for outputs or inputs
if PI:
    GPIO.setwarnings(False)  # Disable warnings
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(RED_PIN, GPIO.OUT)
    GPIO.setup(GREEN_PIN, GPIO.OUT)
    GPIO.setup(YELLOW_PIN, GPIO.OUT)
    GPIO.setup(BLUE_PIN, GPIO.OUT)


def control_light(action, light_color=None):
    """
    Control lights using raspberry pi
    :param action: string on/off to turn on or off
    :param light_color: string contain led color
    """
    if not PI:
        print("I can't find the raspberry pi to do the control actions")
        return None

    if action == 'on':
        if light_color == 'red':
            GPIO.output(RED_PIN, True)
            return tts('{} light {}.'.format(light_color, action))
        elif light_color == 'green':
            GPIO.output(GREEN_PIN, True)
        elif light_color == 'yellow':
            GPIO.output(YELLOW_PIN, True)
        elif light_color == 'blue':
            GPIO.output(BLUE_PIN, True)
            return tts('{} light {}.'.format(light_color, action))
        else:
            GPIO.output(RED_PIN, True)
            GPIO.output(GREEN_PIN, True)
            GPIO.output(YELLOW_PIN, True)
            GPIO.output(BLUE_PIN, True)
    elif action == 'off':
        if light_color == 'red':
            GPIO.output(RED_PIN, False)
            return tts('{} light {}.'.format(light_color, action))
        elif light_color == 'green':
            GPIO.output(GREEN_PIN, False)
        elif light_color == 'yellow':
            GPIO.output(YELLOW_PIN, False)
        elif light_color == 'blue':
            GPIO.output(BLUE_PIN, False)
            return tts('{} light {}.'.format(light_color, action))
        else:
            GPIO.output(RED_PIN, False)
            GPIO.output(GREEN_PIN, False)
            GPIO.output(YELLOW_PIN, False)
            GPIO.output(BLUE_PIN, False)
    else:
        return tts('You should tell me explicitly to turn on or off the lights')
