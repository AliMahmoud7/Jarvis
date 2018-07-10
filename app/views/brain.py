# from .features.respond.tts import tts
from random import choice
from datetime import datetime
from .features.control import control_light
from .features.weather import weather
from .features.define_subject import define_subject
from .features.news import get_news
from wit import Wit
from pprint import pprint
from requests.exceptions import ConnectionError

#
from .features.twitter_interaction import post_tweet
from .features.imgur_handler import image_uploader, show_all_uploads
#from features.business_news_reader import news_reader
from .features.play_music import play_random, play_specific_music, play_shuffle
from .features.notes import note_something, show_all_notes
from .features.open_firefox import open_firefox
#


def brain(speech_text, bot_name, username, location, music_path, images_path):
    """
    The main function for logic and actions
    :param location: your location in the profile
    :param bot_name: bot name in the profile
    :param username: user name in the profile
    :param speech_text:
    :return: standby state
    """

    def undefined():
        return "Oh! Sorry, I Couldn't understand you"

    def check_message(check):
        words_of_message = speech_text.split()
        if set(check).issubset(set(words_of_message)):
            return True
        else:
            return False

    def wit():
        """Handling the speech text with wit.ai for artificial actions"""
        WIT_AI_KEY = "NCC2OIS54Y2ROFYCJ2XZDZREMXTNTIR5"

        client = Wit(access_token=WIT_AI_KEY)
        try:
            resp = client.message(speech_text)
        except ConnectionError as e:
            print('ConnectionError:', e)
            return 'Please, Check your internet connection!'
        pprint(resp)

        entities = resp.get('entities')
        intent = entities.get('intent')
        on_off = entities.get('on_off')
        color = entities.get('color')
        datetime = entities.get('datetime')
        weather_location = entities.get('location')
        greetings = entities.get('greetings')
        thanks = entities.get('thanks')
        bye = entities.get('bye')
        wikipedia_search_query = entities.get('wikipedia_search_query')
        # reminder = entities.get('reminder')

        if intent:
            intent_value = intent[0].get('value')

            if intent_value == 'unknown':
                return undefined()
            elif intent_value == 'curse':
                return "I'm sorry sir, Please don't kick me!"
            elif intent_value == 'lights':
                light_color = 'all'
                if color:
                    light_color = color[0].get('value')
                elif 'red' in speech_text:
                    light_color = 'red'
                elif 'yellow' in speech_text:
                    light_color = 'yellow'
                elif 'blue' in speech_text:
                    light_color = 'blue'
                elif 'green' in speech_text:
                    light_color = 'green'
                elif 'white' in speech_text:
                    light_color = 'white'

                if on_off:
                    action = on_off[0].get('value')
                    return control_light(action, light_color)
                else:
                    return undefined()
            elif intent_value == 'weather':
                w_location = location
                if weather_location:
                    w_location = weather_location[0].get('value')
                return weather(w_location)
            elif intent_value == 'define':
                query = speech_text
                if wikipedia_search_query:
                    query = wikipedia_search_query[0].get('value')
                return define_subject(query)
            elif intent_value == 'doors':
                return "Oh Sorry! I'm not connected with any doors"
                # code to control door
            elif intent_value == 'news':
                # code to view latest news
                return get_news()
            elif intent_value == 'welcome':
                return choice([
                    'I am fine, Thank you.',
                    'Pretty good',
                    "Can't be better",
                    'Not bad'
                ])
            elif intent_value == 'alarm':
                # code to set alarm
                replay = "I can't set the alarm, please try again"
                if datetime:
                    try:
                        date, time = datetime[0].get('value').split('T')
                        print('date is', date)
                        print('time is: ', time)
                        replay = 'Setting alarm at {}'.format(time[:5])
                    except:
                        pass
                return replay
            elif intent_value == 'temp':
                return "Oh Sorry! I can't do that without a temperature sensor!"
            elif intent_value == 'sleep':
                return 0
            elif intent_value == 'age':
                return 'Oh! I am just a baby who learning how to speak!'

        elif greetings:
            return choice([
                "Hi, How's it going?",
                "Hey, What's up?",
                'Hello, How are you?'
            ])
        elif bye:
            # code to go sleep
            # 'Bye!, I will go sleep now, Ping me if you need anything'
            return 0
        elif thanks:
            return choice([
                'You are welcome',
                'Anytime',
                'Glad to help'
            ])
        else:
            return undefined()

    if check_message(['who', 'are', 'you']):
        return choice([
            'I am {}, your smarter personal assistant.'.format(bot_name),
            'Oh, You forget me, I am {}'.format(bot_name),
            'I am your friend {}'.format(bot_name),
            "{}, didn't I tell you before?".format(bot_name)
        ])
    elif check_message(['how', 'i', 'look']) or check_message(['how', 'am', 'i']):
        return choice([
            'You are goddamn handsome!',
            'My knees go weak when I see you.',
            'You look like the kindest person that I have met.'
        ])
    elif check_message(['tell', 'joke']):
        return choice([
            'Why are mountains so funny? Because they are hill areas.',
            "This might make you laugh. How do robots eat guacamole? With computer chips.",
            'Have you ever tried to eat a clock?'
            'I hear it is very time consuming.',
            'What happened when the wheel was invented? A revolution.',
            'What do you call a fake noodle? An impasta!',
            'Did you hear about that new broom? It is sweeping the nation!',
            'What is heavy forward but not backward? Ton.',
            'No, I always forget the punch line.'
        ])
    elif check_message(['who', 'am', 'i']):
        return 'You are {}, a brilliant person. I love you!'.format(username)
    elif check_message(['where', 'born']):
        return 'I was created by a wonderful CSE team as a graduation project in the faculty of Engineering, ' \
               'Minya University - Egypt. '
    # elif check_message(['how', 'are', 'you']):
    #     how_are_you()
    elif check_message(['time']):
        return "The time is " + datetime.strftime(datetime.now(), '%I:%M %p')
    elif check_message(['weather']):
        try:
            w_location = speech_text.split(' in ')[1].strip()
        except:
            w_location = location
        return weather(w_location)
    elif check_message(['define']):
        return define_subject(speech_text)
    elif check_message(['sleep']) or check_message(['bye']):
        # 'Bye!, I will go sleep now, Ping me if you need anything'
        return 0
    elif check_message(['news']):
        return get_news()
    elif check_message(['remind']):
        words = speech_text.split()
        for word in words[:3]:
            if word == 'remind' or word == 'me' or word == 'to':
                words.remove(word)
        clean_msg = ' '.join(words)
        return '"{}", Successfully added to your TO-DO list'.format(clean_msg)

    # kareem
    elif check_message(['tweet']):
        return post_tweet(speech_text)
    elif check_message(['upload']):
        return image_uploader(speech_text, images_path)
    elif check_message(['all', 'uploads']) or check_message(['all', 'images']) or check_message(['uploads']):
        return show_all_uploads()
    #

    # khaled
    #elif check_message(['business', 'news']):
    #    news_reader()
    elif check_message(['play', 'music']) or check_message(['music']):
        return play_random(music_path)
    elif check_message(['play']):
        return play_specific_music(speech_text, music_path)
    elif check_message(['party', 'time']) or check_message(['party', 'mix']):
        return play_shuffle(music_path)
    elif check_message(['note']):
        return note_something(speech_text)
    elif check_message(['all', 'notes']) or check_message(['notes']):
        return show_all_notes()
    elif check_message(['open', 'firefox']):
       return open_firefox()
    #

    else:
        # state = wit()
        # return state
        return wit()
