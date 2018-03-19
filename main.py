#!/usr/bin/env python3

import speech_recognition as sr
import yaml
from features.respond.tts import tts
from brain import brain
import time
from features.control import control_light


# Load profile data
with open('profile.yaml') as f:
    profile = yaml.safe_load(f)
bot_name = profile['bot_name']
username = profile['username']
location = '{}, {}'.format(profile['city'], profile['country'])

# Welcome message
tts('Hi {}, I am {}. How can I help you?'.format(username, bot_name))


def recognize():
    """
    Handling the Speech to text recognition (STT)
    :return: speech text (a string)
    """

    # obtain audio from the microphone
    r = sr.Recognizer()
    with sr.Microphone() as source:
        # listen for 1 second to calibrate the energy threshold for ambient noise levels
        control_light('off', 'red')
        control_light('on', 'green')
        r.adjust_for_ambient_noise(source)
        # print("Say something!")
        audio = r.listen(source)

    # write audio to a WAV file
    # with open("microphone-results.wav", "wb") as f:
    #     f.write(audio.get_wav_data())

    speech_text = ''
    control_light('on', 'red')
    control_light('off', 'green')

    # recognize speech using Google Speech Recognition
    try:
        speech_text = r.recognize_google(audio).lower()
        print('Google -{} thinks you said "{}"'.format(bot_name, speech_text))
        return speech_text
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

    # recognize speech using Microsoft Bing Voice Recognition
    # Endpoint: https://api.cognitive.microsoft.com/sts/v1.0
    # Key 1: 0d6a77ea6cb648a5a123639dd5b4932b
    # Key 2: 92cf7a2c73424f31b6424e4148e37e4f
    BING_KEY = "0d6a77ea6cb648a5a123639dd5b4932b"
    try:
        speech_text = r.recognize_bing(audio, key=BING_KEY).lower()
        print('BING -{} thinks you said "{}"'.format(bot_name, speech_text))
        return speech_text
    except sr.UnknownValueError:
        print("Microsoft Bing Voice Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Microsoft Bing Voice Recognition service; {0}".format(e))

    # recognize speech using IBM Speech to Text
    # "url": "https://stream.watsonplatform.net/speech-to-text/api"
    # "username": "6ce9b92d-21c7-40f2-a7f5-3e89e247b0b7"
    # "password": "PMDair8fVjmu"
    IBM_USERNAME = "6ce9b92d-21c7-40f2-a7f5-3e89e247b0b7"
    IBM_PASSWORD = "PMDair8fVjmu"
    try:
        speech_text = r.recognize_ibm(audio, username=IBM_USERNAME, password=IBM_PASSWORD).lower()
        print('IBM -{} thinks you said "{}"'.format(bot_name, speech_text))
        return speech_text
    except sr.UnknownValueError:
        print("IBM Speech to Text could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from IBM Speech to Text service; {0}".format(e))

    # recognize speech using Wit.ai
    WIT_AI_KEY = "NCC2OIS54Y2ROFYCJ2XZDZREMXTNTIR5"
    try:
        speech_text = r.recognize_wit(audio, key=WIT_AI_KEY).lower()
        print('WIT -{} thinks you said "{}"'.format(bot_name, speech_text))
        return speech_text
    except sr.UnknownValueError:
        print("Wit.ai could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Wit.ai service; {0}".format(e))

    # recognize speech using Sphinx
    try:
        speech_text = r.recognize_sphinx(audio).lower()
        print('Sphinx -{} thinks you said "{}"'.format(bot_name, speech_text))
        return speech_text
    except sr.UnknownValueError:
        print("Sphinx could not understand audio")
    except sr.RequestError as e:
        print("Sphinx error; {0}".format(e))

    return speech_text


def standby():
    """Make the raspberry pi in the standby state"""
    tts('I am in standby state!')
    speech_text = recognize()
    if 'jarvis' in speech_text:
        tts('Hi Sir, How can I help you?')
        main()
    else:
        standby()


def main():
    """Active state"""
    tts('I am in active state')
    speech_text = recognize()
    standby_state = brain(speech_text, username, location)
    if standby_state:
        standby()
    else:
        time.sleep(3)
        main()

    # print('Bye My friend {}'.format(username))
    # tts('Bye My friend {}'.format(username))


if __name__ == '__main__':
    main()
