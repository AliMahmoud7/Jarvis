from datetime import datetime
from features.respond.tts import tts


def what_is_time():
    tts("The time is " + datetime.strftime(datetime.now(), '%I:%M %p'))
