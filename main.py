#!/usr/bin/env python3

import speech_recognition as sr
import yaml
from features.respond.tts import tts
from brain import brain

# Load profile data
with open('profile.yaml') as f:
    profile = yaml.safe_load(f)
name = profile['name']
location = profile['location']

tts(f'Hi {name}, I am Jarvis. How can I help you?')


def main():
    speech_text = ''
    # obtain audio from the microphone
    r = sr.Recognizer()
    with sr.Microphone() as source:
        # listen for 1 second to calibrate the energy threshold for ambient noise levels
        r.adjust_for_ambient_noise(source)
        print("Say something!")
        audio = r.listen(source)

    # # write audio to a WAV file
    # with open("microphone-results.wav", "wb") as f:
    #     f.write(audio.get_wav_data())

    for i in range(2):
        # recognize speech using Google Speech Recognition
        try:
            speech_text = r.recognize_google(audio).lower()
            print(f'Google -Jarvis thinks you said "{speech_text}"')
            break
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))

        # recognize speech using Wit.ai
        WIT_AI_KEY = "NCC2OIS54Y2ROFYCJ2XZDZREMXTNTIR5"
        try:
            speech_text = r.recognize_wit(audio, key=WIT_AI_KEY).lower()
            print(f'WIT -Jarvis thinks you said "{speech_text}"')
            break
        except sr.UnknownValueError:
            print("Wit.ai could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Wit.ai service; {0}".format(e))

        # recognize speech using Microsoft Bing Voice Recognition
        # Endpoint: https://api.cognitive.microsoft.com/sts/v1.0
        # Key 1: 0d6a77ea6cb648a5a123639dd5b4932b
        # Key 2: 92cf7a2c73424f31b6424e4148e37e4f
        BING_KEY = "0d6a77ea6cb648a5a123639dd5b4932b"
        try:
            speech_text = r.recognize_bing(audio, key=BING_KEY).lower()
            print(f'BING -Jarvis thinks you said "{speech_text}"')
            break
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
            print(f'IBM -Jarvis thinks you said "{speech_text}"')
            break
        except sr.UnknownValueError:
            print("IBM Speech to Text could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from IBM Speech to Text service; {0}".format(e))

        # recognize speech using Sphinx
        try:
            speech_text = r.recognize_sphinx(audio).lower()
            print(f'Sphinx -Jarvis thinks you said "{speech_text}"')
            break
        except sr.UnknownValueError:
            print("Sphinx could not understand audio")
        except sr.RequestError as e:
            print("Sphinx error; {0}".format(e))

    brain(name, speech_text, location)
    tts(f'Bye My friend {name}')


if __name__ == '__main__':
    main()


