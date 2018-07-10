import os
import sys
import random

# from app.views.features.respond.tts import tts
from pygame import mixer


def mp3gen(music_path):
    """
    This function finds all the mp3 files in a folder and it's subfolders and returns a list.
    """
    music_list = []
    for root, dirs, files in os.walk(music_path):
        for filename in files:
            if os.path.splitext(filename)[1] == ".mp3":
                music_list.append(os.path.join(root, filename.lower()))
    return music_list


def music_player(file_name):
    """
    This function takes the name of a music file as an argument and plays it depending on the OS.
    """
    if sys.platform == 'darwin':
        player = "afplay '" + file_name + "'"
        return os.system(player)
    elif sys.platform == 'linux2' or sys.platform == 'linux':
        player = "mpg123 '" + file_name + "'"
        return os.system(player)
    else:
        return os.startfile(file_name)
        # mixer.init()
        # mixer.music.load(file_name)
        # mixer.music.play()


def play_random(music_path):
    try:
        music_listing = mp3gen(music_path)
        music_playing = random.choice(music_listing)
        print('music_playing: ', music_playing)
        music_player(music_playing)
        return "Now playing your music!"

    except IndexError as e:
        print("No music files found: {0}".format(e))
        return 'No music files found.'


def play_specific_music(speech_text, music_path):
    words_of_message = speech_text.split()
    words_of_message.remove('play')
    cleaned_message = ' '.join(words_of_message)
    music_listing = mp3gen(music_path)

    for i in range(0, len(music_listing)):
        if cleaned_message in music_listing[i]:
            return music_player(music_listing[i])


def play_shuffle(music_path):
    try:
        music_listing = mp3gen(music_path)
        random.shuffle(music_listing)
        for i in range(0, len(music_listing)):
            return music_player(music_listing[i])
    except IndexError as e:
        print("No music files found: {0}".format(e))
        return 'No music files found.'
