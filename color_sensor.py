import RPi.GPIO as GPIO
import time
from app.views.features.respond.tts import tts


s2 = 22
s3 = 27
signal = 17
NUM_CYCLES = 10


def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(signal, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(s2, GPIO.OUT)
    GPIO.setup(s3, GPIO.OUT)
    print("\n")


def loop():
    temp = 1
    while (1):

        GPIO.output(s2, GPIO.LOW)
        GPIO.output(s3, GPIO.LOW)
        time.sleep(0.3)
        start = time.time()
        for impulse_count in range(NUM_CYCLES):
            GPIO.wait_for_edge(signal, GPIO.FALLING)
        duration = time.time() - start
        red = NUM_CYCLES / duration
        print("red value - ", red)

        GPIO.output(s2, GPIO.LOW)
        GPIO.output(s3, GPIO.HIGH)
        time.sleep(0.3)
        start = time.time()
        for impulse_count in range(NUM_CYCLES):
            GPIO.wait_for_edge(signal, GPIO.FALLING)
        duration = time.time() - start
        blue = NUM_CYCLES / duration
        print("blue value - ", blue)

        GPIO.output(s2, GPIO.HIGH)
        GPIO.output(s3, GPIO.HIGH)
        time.sleep(0.3)
        start = time.time()
        for impulse_count in range(NUM_CYCLES):
            GPIO.wait_for_edge(signal, GPIO.FALLING)
        duration = time.time() - start
        green = NUM_CYCLES / duration
        print("green value - ", green)

        # time.sleep(3)
        print('temp= %s \n' % temp)

        if green < 7000 and blue < 7000 and red > 12000:
            print("red")
            tts('STOP!')
            temp = 1
        elif red < 12000 and blue < 12000 and green > 12000:
            print("green")
            tts('MOVE!')
            temp = 1
        elif green < 7000 and red < 7000 and blue > 12000:
            print("blue")
            temp = 1
        elif red > 10000 and green > 10000 and blue > 10000 and temp == 1:
            print("place the object.....")
            temp = 0

        """
        if green < red and blue < red:
            print("red")
            tts('STOP!')
            temp = 1
        elif red < green and blue < green:
            print("green")
            tts('MOVE!')
            temp = 1
        elif green < blue and red < blue:
            print("blue")
            temp = 1
        """


def endprogram():
    GPIO.cleanup()


if __name__ == '__main__':

    setup()

    try:
        loop()

    except KeyboardInterrupt:
        endprogram()
