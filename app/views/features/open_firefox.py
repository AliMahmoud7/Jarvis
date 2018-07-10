from selenium import webdriver


def open_firefox():
    webdriver.Firefox()
    return 'Opening Firefox'
