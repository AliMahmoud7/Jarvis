import re
import wikipedia
# from app.views.features.respond.tts import tts


def define_subject(speech_text):
    words = speech_text.split()
    for word in words[:3]:
        if word == 'define' or word == 'who' or word == 'are' or words == 'what' or words == 'is':
            words.remove(word)
    cleaned_message = ' '.join(words)

    try:
        wiki_data = wikipedia.summary(cleaned_message, sentences=2)
        print('1:: wiki_data:: ', wiki_data)
        regEx = re.compile(r'([^\(]*)\([^\)]*\) *(.*)')
        m = regEx.match(wiki_data)
        print('2:: wiki_data:: ', m)
        while m:
            wiki_data = m.group(1) + m.group(2)
            m = regEx.match(wiki_data)
        print('3:: wiki_data:: ', m)
        # wiki_data = wiki_data.replace("'", "")
        return wiki_data
    except wikipedia.exceptions.DisambiguationError as e:
        return "Can you please be more specific? You may choose something from the following.; {0}".format(e)
    except wikipedia.exceptions.PageError:
        return 'Page id "{}" does not match any pages. Try another id!'.format(cleaned_message)
