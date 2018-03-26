from features.general_conversations import *
from features.tell_time import what_is_time
from features.weather import weather
from features.define_subject import define_subject
from features.control import control_light
from features.news import get_news
from wit import Wit
from pprint import pprint
from requests.exceptions import ConnectionError

#
from features.twitter_interaction import post_tweet
from features.imgur_handler import image_uploader, show_all_uploads
#from features.business_news_reader import news_reader
from features.play_music import play_random, play_specific_music, play_shuffle
from features.notes import note_something, show_all_notes
#from features.open_firefox import open_firefox
#

WIT_AI_KEY = "NCC2OIS54Y2ROFYCJ2XZDZREMXTNTIR5"


def brain(speech_text, bot_name, username, location, music_path, images_path):
    """
    The main function for logic and actions
    :param location: your location in the profile
    :param bot_name: bot name in the profile
    :param username: user name in the profile
    :param speech_text:
    :return: standby state
    """

    if not speech_text:
        return False

    def wit():
        """Handling the speech text with wit.ai for artificial actions"""
        client = Wit(access_token=WIT_AI_KEY)
        try:
            resp = client.message(speech_text)
        except ConnectionError as e:
            print('ConnectionError:', e)
            undefined()
            return None
        entities = resp.get('entities')
        pprint(resp)
        intent = entities.get('intent')
        on_off = entities.get('on_off')
        color = entities.get('color')
        datetime = entities.get('datetime')
        weather_location = entities.get('location')
        greetings = entities.get('greetings')
        thanks = entities.get('thanks')
        bye = entities.get('bye')
        wikipedia_search_query = entities.get('wikipedia_search_query')
        reminder = entities.get('reminder')

        if intent:
            intent_value = intent[0].get('value')
            if intent_value == 'lights':
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
                    control_light(action, light_color)
                else:
                    undefined()
            elif intent_value == 'weather':
                w_location = location
                if weather_location:
                    w_location = weather_location[0].get('value')
                weather(w_location)
            elif intent_value == 'define':
                query = speech_text
                if wikipedia_search_query:
                    query = wikipedia_search_query[0].get('value')
                define_subject(query)
            elif intent_value == 'doors':
                tts("Oh Sorry! I'm not connected with any doors")
                # code to control door
            elif intent_value == 'news ':
                # code to view latest news
                get_news()
            elif intent_value == 'welcome':
                how_are_you()
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
                tts(replay)
            elif intent_value == 'temp':
                tts("Oh Sorry! I can't do that without a temperature sensor!")
            elif intent_value == 'sleep':
                return 'sleep'
            elif intent_value == 'age':
                tts('Hahaaaa, I am just a baby who learning how to speak!')
        elif greetings:
            replies = [
                "Hi, How's it going?",
                "Hey, What's up?",
                'Hello, How are you?'
            ]
            tts(choice(replies))
        elif bye:
            # code to go sleep
            # tts('Bye!, I will go sleep now, Ping me if you need anything')
            return 'sleep'
        elif thanks:
            replies = [
                'You are welcome',
                'Anytime',
                'Glad to help'
            ]
            tts(choice(replies))
        elif reminder:
            to_do_value = reminder[0].get('value')
            tts('"{}", Successfully added to your TO-DO list'.format(to_do_value))
            # add this value to the database in the TO-DO list
        else:
            undefined()

    def check_message(check):
        words_of_message = speech_text.split()
        if set(check).issubset(set(words_of_message)):
            return True
        else:
            return False

    if check_message(['who', 'are', 'you']):
        who_are_you(bot_name)
    elif check_message(['how', 'i', 'look']) or check_message(['how', 'am', 'i']):
        how_am_i()
    elif check_message(['tell', 'joke']):
        tell_joke()
    elif check_message(['who', 'am', 'i']):
        who_am_i(username)
    elif check_message(['where', 'born']):
        where_born()
    # elif check_message(['how', 'are', 'you']):
    #     how_are_you()
    elif check_message(['time']):
        what_is_time()
    elif check_message(['weather']):
        try:
            w_location = speech_text.split('in')[1].strip()
        except:
            w_location = location
        weather(w_location)
    elif check_message(['define']):
        define_subject(speech_text)
    elif check_message(['sleep']) or check_message(['bye']):
        # tts('Bye!, I will go sleep now, Ping me if you need anything')
        return True
    elif check_message(['news']):
        get_news()

    # kareem
    elif check_message(['tweet']):
        post_tweet(speech_text)
    elif check_message(['upload']):
        image_uploader(speech_text, images_path)
    elif check_message(['all', 'uploads']) or check_message(['all', 'images']) or check_message(['uploads']):
        show_all_uploads()
    #

    # khaled
    #elif check_message(['business', 'news']):
    #    news_reader()
    elif check_message(['play', 'music']) or check_message(['music']):
        play_random(music_path)
    elif check_message(['play']):
        play_specific_music(speech_text, music_path)
    elif check_message(['party', 'time']) or check_message(['party', 'mix']):
        play_shuffle(music_path)
    elif check_message(['note']):
        note_something(speech_text)
    elif check_message(['all', 'notes']) or check_message(['notes']):
        show_all_notes()
    #elif check_message(['open', 'firefox']):
    #    open_firefox()
    #

    else:
        state = wit()
        if state == 'sleep':
            return True
