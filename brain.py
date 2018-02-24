from features import *


def brain(name, speech_text):
    """

    :param name: user name founded in the profile
    :param speech_text:
    :return: TTS
    """
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
    else:
        undefined()
