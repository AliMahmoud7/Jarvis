from flask import Blueprint, render_template, request
from app import app
import os
from .features.respond.tts import tts
from .features.control import lcd
from .main import serve_voice, serve_text
import time
from threading import Thread

from playsound import playsound
from pygame import mixer
import sys

home = Blueprint('home', __name__)

BASE_DIR = app.config['BASE_DIR']
# Profile data
bot_name = 'Jarvis'
username = 'Sir'
location = 'Minya, Egypt'
music_path = os.path.join(BASE_DIR, 'data/music')
images_path = os.path.join(BASE_DIR, 'data/images')
database_path = os.path.join(BASE_DIR, 'data/memory.db')
recorded_audio_path = os.path.join(BASE_DIR, "audio.wav")
jarvis_beep_audio_path = os.path.join(BASE_DIR, "data/music/jarvis_beep.mp3")

# def process_waiting():
#     tts('I am processing your request!')
#     tts('Please Wait!')
#     return None


def show_sys_stable():
    """Show system stable message on LCD"""
    time.sleep(10)
    lcd.clear()
    lcd.message('System Stable :)')
    return True


def jarvis_beep():
    """Jarvis is on"""
    if sys.platform == "win32":
        # print('on windows')
        # mixer.init()
        # mixer.music.load(output)
        # mixer.music.play()
        # while mixer.music.get_busy():
        #     continue
        return playsound(jarvis_beep_audio_path)
        # os.startfile(output)
    else:
        # the following works on Mac and Linux. (Darwin = mac, xdg-open = linux).
        # opener = "open" if sys.platform == "darwin" else "xdg-open"
        # print([opener, output])
        # subprocess.call([opener, output])
        mixer.init()
        mixer.music.load(jarvis_beep_audio_path)
        mixer.music.play()
        while mixer.music.get_busy():
            continue
    return True


@home.route('/')
def index():
    return render_template('index.html')


@home.route('/voice', methods=['GET', 'POST'])
def voice():
    if request.method == 'POST':
        audio = request.data

        Thread(target=jarvis_beep).start()

        with open(recorded_audio_path, "wb") as file:
            file.write(audio)

        server_msg = serve_voice(recorded_audio_path, bot_name, username, location, music_path, images_path, database_path)

        if lcd:
            lcd.clear()
            lcd.message('Process Done!')
            t1 = Thread(target=show_sys_stable)
            t1.start()

        # t1.join()
        jarvis_beep()
        tts(server_msg)
        return server_msg

    return render_template('voice.html')


@home.route('/text', methods=['GET', 'POST'])
def text():
    if request.method == 'POST':
        user_msg = request.data.decode()

        server_msg = serve_text(user_msg, bot_name, username, location, music_path, images_path, database_path)
        return server_msg

    return render_template('chat.html')
