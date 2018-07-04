from selenium import webdriver

from features.respond.tts import tts


def open_firefox():
    tts('Aye aye captain, opening Firefox')
    return webdriver.Firefox()
