from features.respond.tts import tts
from random import choice


def who_are_you():
    replies = [
        'I am Jarvis, your smarter personal assistant.',
        'Oh, You forget me, I am Jarvis',
        'I am your friend Jarvis',
        'Jarvis, didnt I tell you before?'
    ]
    tts(choice(replies))


def how_am_i():
    replies = [
        'You are goddamn handsome!',
        'My knees go weak when I see you.',
        'You look like the kindest person that I have met.'
    ]
    tts(choice(replies))


def tell_joke():
    jokes = [
        'What happens to a frogs car when it breaks down? It gets toad away.',
        'Why was six scared of seven? Because seven ate nine.',
        'No, I always forget the punch line.'
    ]
    tts(choice(jokes))


def who_am_i(name):
    tts('You are {}, a brilliant person. I love you!'.format(name))


def where_born():
    tts('I was created by a magician named Ali, in Egypt.')


def how_are_you():
    replies = [
        'I am fine, thank you.',
        'Pretty good',
        'Cannt be better',
        'Not bad'
    ]
    tts(choice(replies))


def undefined():
    tts("I Couldn't understand you")
