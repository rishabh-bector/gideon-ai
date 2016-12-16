import requests
import json
import pyowm
from pprint import pprint
from quizlet import QuizletClient
from random import randint
import SpeechControl as SC
import RequestControl as RC
import wikipedia
import pyjokes




class KnowledgeController:

    def __init__(self):

        self.apikey = 'AIzaSyCAFSilFospcrlGlROf4NLNG4z1coYCHtc'
        self.serviceurl = 'https://kgsearch.googleapis.com/v1/entities:search'
        self.quizletid = 'EGeXd4J2jH'
        self.Speech = SC.SpeechController('Gideon', 'en-uk')
        self.quizletkey = 'wJ5qBU5SmcTa4NTq92jAHh'
        self.weatherkey = 'c51599edbd4fdc796ccd41fcf12b80c0'
        self.quizlet = QuizletClient(
            client_id=self.quizletid, login=self.quizletkey)
        self.owm = pyowm.OWM(self.weatherkey)
        self.RequestHandler = RC.RequestController()
        self.junkQueries = {'whatis': ['what is', 'who is']}

    def askGoogle(self, response):

        query = response['resolvedQuery']

        # print(response)

        if 'parameters' in response:
            query = response['parameters']['q'].lower()
            rtype = response['parameters']['request_type'].lower()

        ### Query Formatting ###

        if rtype in self.junkQueries:
            for junk in self.junkQueries[rtype]:
                query = query.replace(junk, '')
        else:
            query = rtype + ' ' + query

        ###                  ###

        print('Requesting Query... ' + query)

        payload = {
            'query': query,
            'limit': 10,
            'indent': True,
            'key': self.apikey,
        }

        r = requests.get(self.serviceurl, params=payload).json()
        pprint(r)

        descriptions = ''

        try:
            for element in r['itemListElement']:
                try:

                    descriptions += str(element['result'][
                        'detailedDescription']['articleBody']) + '.,.,.,'
                except Exception:
                    pass

        except Exception:
            descriptions = 'Not found'

        return descriptions

    def ask(self, response):

        query = response['resolvedQuery']

        # print(response)

        if 'parameters' in response:
            query = response['parameters']['q'].lower()
            rtype = response['parameters']['request_type'].lower()

        ### Query Formatting ###

        if rtype in self.junkQueries:
            for junk in self.junkQueries[rtype]:
                query = query.replace(junk, '')
        else:
            query = rtype + ' ' + query

        ###                  ###

        print('Requesting Query... ' + query)

        resp = wikipedia.summary(query, sentences=2)

        try:
            resp = resp.replace(resp[resp.index('('):resp.index(')') + 1], '')
        except Exception:
            pass

        return resp

    def getWeather(self, response):

        location = response['parameters']['location']

        observation = self.owm.weather_at_place(location)
        w = observation.get_weather()

        output = 'The temperature is ' + str(w.get_temperature('celsius')['temp']) + ' degrees celsius. Humidity is ' + str(
            w.get_humidity()) + ' percent. Status is ' + w.get_status()

        return output
