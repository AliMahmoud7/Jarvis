# -*- coding: utf-8 -*-

import requests
import pyowm
# from darksky import forecast
from app.views.features.respond.tts import tts

google_api_key = 'AIzaSyBoH7qwxOf6z-QQQL84iKXMGS__ZOHsVog'
OpenWeatherMap_API_key = '05f12b7800aae01aef77b1cecb5f6571'
Dark_Sky_API_KEY = 'c1d41ad7a9447622dc2b089eba50e4a8'


def geocode_location(location):
    print(location)
    params = {'address': location, 'key': google_api_key}
    url = 'https://maps.googleapis.com/maps/api/geocode/json'
    result = requests.get(url, params).json()
    lat = result['results'][0]['geometry']['location']['lat']
    lng = result['results'][0]['geometry']['location']['lng']
    return lat, lng


def weather(location):
    lat, lng = geocode_location(location)

    owm = pyowm.OWM(OpenWeatherMap_API_key)

    # Search for current weather
    w = owm.weather_at_coords(lat, lng).get_weather()

    # Weather details
    status = w.get_detailed_status()
    temp = round(w.get_temperature('celsius')['temp'])

    return tts("Now, It is {} and {} degree celsius in {}".format(status, temp, location))

    #############################################
    # with forecast(Dark_Sky_API_KEY, lat, lng) as boston:
    #     tomorrow = boston.daily[1]
    #     print(tomorrow.summary)
    #     print(round((tomorrow.temperatureMin - 32) * (5 / 9)))
    #     print(round((tomorrow.temperatureMax - 32) * (5 / 9)))
