import time
# from app.views.features.respond.tts import tts

try:
    import RPi.GPIO as GPIO
    import Adafruit_CharLCD as LCD

    # Raspberry Pi pin setup
    lcd_rs = 25
    lcd_en = 24
    lcd_d4 = 23
    lcd_d5 = 2
    lcd_d6 = 18
    lcd_d7 = 10
    lcd_backlight = 2
    # Define LCD column and row size for 16x2 LCD.
    lcd_columns = 16
    lcd_rows = 2

    lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows, lcd_backlight)
    lcd.clear()
    lcd.message('System Stable :)')
    PI = True
except:
    lcd = False
    PI = False

# Light colors with Pin numbers

# Define global Pins
RED_PIN = 17
GREEN_PIN = 27
YELLOW_PIN = 22
BLUE_PIN = 9

# Setup GPIO Pins for outputs or inputs
if PI:
    GPIO.setwarnings(False)  # Disable warnings
    GPIO.setmode(GPIO.BCM)
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
        return "I can't find the raspberry pi to do the control actions"

    if action == 'on':
        if light_color == 'red':
            GPIO.output(RED_PIN, True)
            return '{} light {}.'.format(light_color, action)
        elif light_color == 'green':
            GPIO.output(GREEN_PIN, True)
            return '{} light {}.'.format(light_color, action)
        elif light_color == 'yellow':
            GPIO.output(YELLOW_PIN, True)
            return '{} light {}.'.format(light_color, action)
        elif light_color == 'blue':
            GPIO.output(BLUE_PIN, True)
            return '{} light {}.'.format(light_color, action)
        else:
            GPIO.output(RED_PIN, True)
            GPIO.output(GREEN_PIN, True)
            GPIO.output(YELLOW_PIN, True)
            GPIO.output(BLUE_PIN, True)
            return 'Light {}.'.format(action)
    elif action == 'off':
        if light_color == 'red':
            GPIO.output(RED_PIN, False)
            return '{} light {}.'.format(light_color, action)
        elif light_color == 'green':
            GPIO.output(GREEN_PIN, False)
            return '{} light {}.'.format(light_color, action)
        elif light_color == 'yellow':
            GPIO.output(YELLOW_PIN, False)
            return '{} light {}.'.format(light_color, action)
        elif light_color == 'blue':
            GPIO.output(BLUE_PIN, False)
            return '{} light {}.'.format(light_color, action)
        else:
            GPIO.output(RED_PIN, False)
            GPIO.output(GREEN_PIN, False)
            GPIO.output(YELLOW_PIN, False)
            GPIO.output(BLUE_PIN, False)
            return 'Light {}.'.format(action)
    else:
        return 'You should tell me explicitly to turn on or off the lights'
