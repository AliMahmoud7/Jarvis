from flask import Blueprint, render_template, request
from app import app
import os
from .main import serve_voice, serve_text

home = Blueprint('home', __name__)

BASE_DIR = app.config['BASE_DIR']
# Profile data
bot_name = 'Jarvis'
username = 'Sir'
location = 'Minya, Egypt'
music_path = os.path.join(BASE_DIR, 'data/music')
images_path = os.path.join(BASE_DIR, 'data/images')
recorded_audio_path = os.path.join(BASE_DIR, "audio.wav")


@home.route('/', methods=['GET', 'POST'])
@home.route('/voice', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        audio = request.data

        with open(recorded_audio_path, "wb") as file:
            file.write(audio)

        serve_voice(recorded_audio_path, bot_name, username, location, music_path, images_path)
        return "Successfully handled your voice!"

    return render_template('index.html')


@home.route('/text', methods=['GET', 'POST'])
def text():
    if request.method == 'POST':
        user_msg = request.data.decode()

        server_msg = serve_text(user_msg, bot_name, username, location, music_path, images_path)
        return server_msg

    return render_template('chat.html')
