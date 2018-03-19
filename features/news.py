import requests
from features.respond.tts import tts


def get_news():
    url = 'https://newsapi.org/v2/top-headlines'
    params = {
        'country': 'us',
        'apiKey': '578265f838fb4cc191ac00e7e60a73a2',
        'category': 'technology',
        'pageSize': 3
    }

    response = requests.get(url, params).json()
    if response['status'] == 'ok':
        articles = response['articles']
        tts('Top 3 headlines in the US are')
        for article in articles:
            print(article['title'])
            tts(article['title'])
