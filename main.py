#!/usr/bin/env python3

import speech_recognition as sr
import json
from wit import Wit
from features.respond.tts import tts

# Load profile data
with open('profile.json') as f:
    profile = json.load(f)
name = profile['name']
city_name = profile['city_name']

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
            speech_text = r.recognize_google(audio)
            print(f'Jarvis thinks you said "{speech_text}"')
            break
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))

        # recognize speech using Wit.ai
        WIT_AI_KEY = "NCC2OIS54Y2ROFYCJ2XZDZREMXTNTIR5"
        try:
            speech_text = r.recognize_wit(audio, key=WIT_AI_KEY)
            print(f'Jarvis thinks you said "{speech_text}"')
            break
        except sr.UnknownValueError:
            print("Wit.ai could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Wit.ai service; {0}".format(e))

        # recognize speech using Sphinx
        try:
            speech_text = r.recognize_sphinx(audio)
            print(f'Jarvis thinks you said "{speech_text}"')
            break
        except sr.UnknownValueError:
            print("Sphinx could not understand audio")
        except sr.RequestError as e:
            print("Sphinx error; {0}".format(e))

    tts(speech_text)
    tts(f'Bye My friend {name}')


if __name__ == '__main__':
    main()

# client = Wit(access_token=WIT_AI_KEY)
# resp = client.message(speech_text)
# print('Yay, got Wit.ai response: ' + str(resp))

# ---------------------------------------------------------------
# # recognize speech using Microsoft Bing Voice Recognition
# Endpoint: https://api.cognitive.microsoft.com/sts/v1.0
# Key 1: 0d6a77ea6cb648a5a123639dd5b4932b
# Key 2: 92cf7a2c73424f31b6424e4148e37e4f
# BING_KEY = "INSERT BING API KEY HERE"  # Microsoft Bing Voice Recognition API keys 32-character lowercase hexadecimal strings
# try:
#     print("Microsoft Bing Voice Recognition thinks you said " + r.recognize_bing(audio, key=BING_KEY))
# except sr.UnknownValueError:
#     print("Microsoft Bing Voice Recognition could not understand audio")
# except sr.RequestError as e:
#     print("Could not request results from Microsoft Bing Voice Recognition service; {0}".format(e))
