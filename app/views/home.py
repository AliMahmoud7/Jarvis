from flask import Blueprint, render_template, request
# from .main import sr

home = Blueprint('home', __name__)


@home.route('/', methods=['GET', 'POST'])
@home.route('/voice', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        audio = request.data

        with open("audio_test.wav", "wb") as file:
            file.write(audio)

        return "Done!!"

    return render_template('index.html')


@home.route('/text', methods=['GET', 'POST'])
def text():
    if request.method == 'POST':
        msg = request.data.decode()
        return "I have received your request '{}'".format(msg)

    return render_template('chat.html')
