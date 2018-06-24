import tweepy
from features.respond.tts import tts

access_token = '931160532203294720-o5HjeKUHz3XtNmwH2ELOzrkTfUtrLCW'
access_token_secret = 'e6IBO20HGmpGblUOpHzHENLmFIdRKdN4LwcJP4eu7VneC'
consumer_key = 'lCvcWMMNGSUTdtUmmws2qEksy'
consumer_secret = 'gcYCgFv6IEF6CwSHA3NWc6OGTiGpaFvyyp8hCBtMDWYuS9m7kr'


def post_tweet(speech_text):
    words_of_message = speech_text.split()
    words_of_message.remove('tweet')
    cleaned_message = ' '.join(words_of_message).capitalize()
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    print('cleaned msg: ', cleaned_message)
    api.update_status(status=cleaned_message)

    return tts('Your tweet has been posted on your twitter account')

# post_tweet(speech_text, consumer_key, consumer_secret, access_token, access_token_secret)
