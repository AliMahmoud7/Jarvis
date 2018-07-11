import requests
# from app.views.features.respond.tts import tts


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
        top_news = 'Top 3 headlines in the US are:\n'
        for article in articles:
            # print(article['title'])
            # tts(article['title'])
            top_news += '# {}. \n'.format(article['title'])
        return top_news
    return None
