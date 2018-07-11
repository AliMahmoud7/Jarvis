#!/usr/bin/env python3

import speech_recognition as sr
# from .features.respond.tts import tts
from .brain import brain
from string import punctuation


BING_KEY = "92cf7a2c73424f31b6424e4148e37e4f"
IBM_USERNAME = "6ce9b92d-21c7-40f2-a7f5-3e89e247b0b7"
IBM_PASSWORD = "PMDair8fVjmu"
WIT_AI_KEY = "NCC2OIS54Y2ROFYCJ2XZDZREMXTNTIR5"

# obtain the audio
r = sr.Recognizer()


def recognize(audio, bot_name):
    """
    Handling the Speech to text recognition (STT)
    :return: speech text (a string)
    """

    speech_text = None

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


def serve_voice(voice_file, bot_name, username, location, music_path, images_path, database_path):
    """Serve user voice speech"""

    with sr.WavFile(voice_file) as source:
        r.adjust_for_ambient_noise(source, duration=0.5)
        audio = r.record(source)

    speech_text = recognize(audio, bot_name)

    if speech_text:
        # cleaned_text = clean_text(speech_text)
        reply = brain(speech_text, bot_name, username, location, music_path, images_path, database_path)
        if reply:
            return reply
        # tts('I am listening. You can ask me again.')
        elif reply == 0:
            return 'I will go sleep now, Ping me if you need anything!'
        else:
            return 'An unexpected error has occurred!'
    else:
        return "I couldn't understand your audio, Try to say something!"


def serve_text(text_msg, bot_name, username, location, music_path, images_path, database_path):
    """Serve user text chat"""
    cleaned_msg = clean_text(text_msg)
    reply = brain(cleaned_msg, bot_name, username, location, music_path, images_path, database_path)

    if reply:
        return reply
    elif reply == 0:
        return 'I will go sleep now, Ping me if you need anything!'
    else:
        return 'An unexpected error has occurred!'


def clean_text(text):
    filtered_text = list(filter(lambda character: character not in punctuation, list(text.strip())))

    return ''.join(filtered_text).lower()

