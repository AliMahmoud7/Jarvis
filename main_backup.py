#!/usr/bin/env python3

import speech_recognition as sr
import yaml
from features.respond.tts import tts
from brain import brain
import time
import os
import sys
from features.control import control_light

if sys.platform == 'linux' or sys.platform == 'linux2':
    # Suppress ALSA lib error messages
    from ctypes import *

    # Define our error handler type
    ERROR_HANDLER_FUNC = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p)


    def py_error_handler(filename, line, function, err, fmt):
        pass


    c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)
    asound = cdll.LoadLibrary('libasound.so')
    # Set error handler
    asound.snd_lib_error_set_handler(c_error_handler)


BASE_DIR = os.path.abspath(os.path.dirname(__file__))
RECOGNIZE_ERRORS = 0
device_index = 0

# Load profile data
with open('profile.yaml') as f:
    profile = yaml.safe_load(f)
bot_name = profile['bot_name']
username = profile['username']
location = '{}, {}'.format(profile['city'], profile['country'])
music_path = os.path.join(BASE_DIR, profile['music_dir'])
images_path = os.path.join(BASE_DIR, profile['images_dir'])

del BASE_DIR
del profile


BING_KEY = "92cf7a2c73424f31b6424e4148e37e4f"
IBM_USERNAME = "6ce9b92d-21c7-40f2-a7f5-3e89e247b0b7"
IBM_PASSWORD = "PMDair8fVjmu"
WIT_AI_KEY = "NCC2OIS54Y2ROFYCJ2XZDZREMXTNTIR5"


def microphone_index():
    """Check Microphone index"""
    global device_index
    print('-------------------------------------------------------------------------------')
    for index, name in enumerate(sr.Microphone.list_microphone_names()):
        print("Microphone with name \"{1}\" found for `Microphone(device_index={0})`".format(index, name))
        if "USB PnP Sound".lower() in name.lower():
            device_index = index
            break
    print('device_index: ', device_index)
    print('-------------------------------------------------------------------------------')


microphone_index()


def recognize():
    """
    Handling the Speech to text recognition (STT)
    :return: speech text (a string)
    """

    # obtain audio from the microphone
    r = sr.Recognizer()
    with sr.Microphone(device_index=device_index) as source:
        control_light('off', 'red')
        control_light('on', 'green')
        # listen for 1 second to calibrate the energy threshold for ambient noise levels
        r.adjust_for_ambient_noise(source)
        print("Say something!")
        audio = r.listen(source, phrase_time_limit=5)

    # write audio to a WAV file
    # with open("microphone-results.wav", "wb") as f:
    #     f.write(audio.get_wav_data())

    speech_text = None
    control_light('on', 'red')
    control_light('off', 'green')

    # recognize speech using Google Speech Recognition
    try:
        speech_text = r.recognize_google(audio).lower()
        print('Google -{} thinks you said "{}"'.format(bot_name, speech_text))
        return speech_text
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
        return None
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

    # recognize speech using IBM Speech to Text
    # "url": "https://stream.watsonplatform.net/speech-to-text/api"
    # "username": "6ce9b92d-21c7-40f2-a7f5-3e89e247b0b7"
    # "password": "PMDair8fVjmu"
    try:
        speech_text = r.recognize_ibm(audio, username=IBM_USERNAME, password=IBM_PASSWORD).lower()
        print('IBM -{} thinks you said "{}"'.format(bot_name, speech_text))
        return speech_text
    except sr.UnknownValueError:
        print("IBM Speech to Text could not understand audio")
        return None
    except sr.RequestError as e:
        print("Could not request results from IBM Speech to Text service; {0}".format(e))

    # recognize speech using Microsoft Bing Voice Recognition
    # Endpoint: https://api.cognitive.microsoft.com/sts/v1.0
    # Key 1: 0d6a77ea6cb648a5a123639dd5b4932b
    # Key 2: 92cf7a2c73424f31b6424e4148e37e4f
    try:
        speech_text = r.recognize_bing(audio, key=BING_KEY).lower()
        print('BING -{} thinks you said "{}"'.format(bot_name, speech_text))
        return speech_text
    except sr.UnknownValueError:
        print("Microsoft Bing Voice Recognition could not understand audio")
        return None
    except sr.RequestError as e:
        print("Could not request results from Microsoft Bing Voice Recognition service; {0}".format(e))

    # recognize speech using Wit.ai
    try:
        speech_text = r.recognize_wit(audio, key=WIT_AI_KEY).lower()
        print('WIT -{} thinks you said "{}"'.format(bot_name, speech_text))
        return speech_text
    except sr.UnknownValueError:
        print("Wit.ai could not understand audio")
        return None
    except sr.RequestError as e:
        print("Could not request results from Wit.ai service; {0}".format(e))

    # recognize speech using Sphinx
    try:
        speech_text = r.recognize_sphinx(audio).lower()
        print('Sphinx -{} thinks you said "{}"'.format(bot_name, speech_text))
        return speech_text
    except sr.UnknownValueError:
        print("Sphinx could not understand audio")
        return None
    except sr.RequestError as e:
        print("Sphinx error; {0}".format(e))

    return speech_text


def standby():
    """Make the raspberry pi in the standby state"""
    print('I am in standby state!')
    speech_text = recognize()
    if speech_text:
        replies = ['{}'.format(bot_name).lower(), 'hi', 'hey', 'wake up', 'start', 'begin', 'help', 'need you']

        # CHECK THIS?
        for word in replies:
            if word in speech_text:
                tts('Hi {}, How can I help you?'.format(username))
                control_light('off', 'yellow')
                return main()
                # break
        else:
            return standby()

        if '{}'.format(bot_name).lower() in speech_text:
            tts('Hi {}, How can I help you?'.format(username))
            control_light('off', 'yellow')
            return main()
        else:
            # tts("Just call my name")
            return standby()
    else:
        time.sleep(5)
        return standby()


def main():
    """Active state"""
    global RECOGNIZE_ERRORS
    print('I am in active state')

    speech_text = recognize()
    if speech_text:
        standby_state = brain(speech_text, bot_name, username, location, music_path, images_path)
        if standby_state == 0:
            tts('Bye!, I will go sleep now, Ping me if you need anything')
            control_light('on', 'yellow')
            return standby()
        else:
            time.sleep(3)
            return main()
    else:
        # tts("I couldn't understand your audio, Try to say something!")
        RECOGNIZE_ERRORS += 1
        return main()

    # tts('Bye My friend {}'.format(username))


if __name__ == '__main__':
    # Welcome message
    tts('Hi {}, I am {}. How can I help you?'.format(username, bot_name))

    main()
    # standby()
