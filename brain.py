from features.general_conversations import *
from features.tell_time import what_is_time
from features.weather import weather
from features.define_subject import define_subject
from wit import Wit


def brain(name, speech_text, location):
    """

    :param name: user name founded in the profile
    :param speech_text:
    :return: TTS
    """

    def wit():
        WIT_AI_KEY = "NCC2OIS54Y2ROFYCJ2XZDZREMXTNTIR5"
        client = Wit(access_token=WIT_AI_KEY)
        resp = client.message(speech_text)
        try:
            intention = resp['entities']['intent'][0]['value']
            print(intention)
        except:
            print('I cannot find the intention')

    wit()

    def check_message(check):
        words_of_message = speech_text.split()
        if set(check).issubset(set(words_of_message)):
            return True
        else:
            return False

    if check_message(['who', 'are', 'you']):
        who_are_you()
    elif check_message(['how', 'i', 'look']) or check_message(['how', 'am', 'i']):
        how_am_i()
    elif check_message(['tell', 'joke']):
        tell_joke()
    elif check_message(['who', 'am', 'i']):
        who_am_i(name)
    elif check_message(['where', 'born']):
        where_born()
    elif check_message(['how', 'are', 'you']):
        how_are_you()
    elif check_message(['time']):
        what_is_time()
    elif check_message(['weather']):
        weather(location)
    elif check_message(['define']):
        words_of_message = speech_text.split()
        words_of_message.remove('define')
        cleaned_message = ' '.join(words_of_message)
        define_subject(cleaned_message)
    else:
        undefined()
