from features.general_conversations import *
from features.tell_time import what_is_time
from features.weather import weather
from features.define_subject import define_subject
from features.control import control_light
from wit import Wit
from pprint import pprint
from requests.exceptions import ConnectionError


WIT_AI_KEY = "NCC2OIS54Y2ROFYCJ2XZDZREMXTNTIR5"


def brain(speech_text, name, location):
    """
    The main function for logic and actions
    :param location:
    :param name: user name founded in the profile
    :param speech_text:
    :return: standby state
    """

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
                # code to control door
                pass
            elif intent_value == 'news ':
                # code to view latest news
                pass
            elif intent_value == 'alarm':
                if datetime:
                    time = datetime[0].get('value')
                    # code to set alarm
                    tts('Setting alarm at {}'.format(time))
        elif greetings:
            replies = [
                'Hi',
                "Hey, What's up",
                'Hello, How are you?'
            ]
            tts(choice(replies))
        elif bye or on_off[0].get('value') == 'off':
            # code to go sleep
            tts('Bye!, I will go sleep now, Ping me if you need anything')
            return 'sleep'
        elif thanks:
            replies = [
                'You are welcome',
                'anytime',
                'glad to help'
            ]
            tts(choice(replies))
        elif reminder:
            to_do_value = reminder[0].get('value')
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
        who_are_you()
    elif check_message(['how', 'i', 'look']) or check_message(['how', 'am', 'i']):
        how_am_i()
    elif check_message(['tell', 'joke']):
        tell_joke()
    elif check_message(['who', 'am', 'i']):
        who_am_i(name)
    elif check_message(['where', 'born']):
        where_born()
    elif check_message(['how', 'are', 'you']):
        how_are_you()
    elif check_message(['time']):
        what_is_time()
    elif check_message(['weather']):
        weather(location)
    elif check_message(['define']):
        define_subject(speech_text)
    elif check_message(['sleep']) or check_message(['bye']):
        tts('Bye!, I will go sleep now, Ping me if you need anything')
        return True
    else:
        state = wit()
        if state == 'sleep':
            return True
