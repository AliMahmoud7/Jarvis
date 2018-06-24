import re
import wikipedia
from features.respond.tts import tts


def define_subject(speech_text):
    # words_of_message = speech_text.split()
    # words_of_message.remove('who')
    # words_of_message.remove('are')
    # words_of_message.remove('what')
    # words_of_message.remove('is')
    # words_of_message.remove('define')
    # cleaned_message = ' '.join(words_of_message)
    # cleaned_message = speech_text.replace('define', '').replace('who are', '').replace('what is', '').strip()

    words = speech_text.split()
    for word in words[:3]:
        if word == 'define' or word == 'who' or word == 'are' or words == 'what' or words == 'is':
            words.remove(word)
    cleaned_message = ' '.join(words)

    try:
        wiki_data = wikipedia.summary(cleaned_message, sentences=5)
        regEx = re.compile(r'([^\(]*)\([^\)]*\) *(.*)')
        m = regEx.match(wiki_data)
        while m:
            wiki_data = m.group(1) + m.group(2)
            m = regEx.match(wiki_data)
        print('AFTER::: ', wiki_data)
        wiki_data = wiki_data.replace("'", "")
        return tts(wiki_data)
    except wikipedia.exceptions.DisambiguationError as e:
        print("Can you please be more specific? You may choose something from the following.; {0}".format(e))
        return tts('Can you please be more specific? You may choose something from the following.')
    except wikipedia.exceptions.PageError:
        return tts('Page id "{}" does not match any pages. Try another id!'.format(cleaned_message))
