import requests
import json
import pyowm
from pprint import pprint
import quizlet
from random import randint
import SpeechControl as SC


class KnowledgeController:

    def __init__(self):

        self.apikey = 'AIzaSyCAFSilFospcrlGlROf4NLNG4z1coYCHtc'
        self.serviceurl = 'https://kgsearch.googleapis.com/v1/entities:search'
        self.quizletid = 'EGeXd4J2jH'
        self.Speech = SC.SpeechController('Gideon', 'en-uk')
        self.quizletkey = 'wJ5qBU5SmcTa4NTq92jAHh'
        self.weatherkey = 'c51599edbd4fdc796ccd41fcf12b80c0'
        self.quizlet = quizlet.QuizletClient(
            client_id=self.quizletid, login=self.quizletkey)
        self.owm = pyowm.OWM(self.weatherkey)

        self.junkQueries = {'whatis': ['what is', 'who is']}

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

    def getWeather(self, response):

        location = response['parameters']['location']

        observation = self.owm.weather_at_place(location)
        w = observation.get_weather()

        output = 'The temperature is ' + str(w.get_temperature('celsius')['temp']) + ' degrees celsius. Humidity is ' + str(
            w.get_humidity()) + ' percent. Status is ' + w.get_status()

        return output

    def quiz(self, response):

        name = response['parameters']['quizname']
        self.Speech.say('Starting quiz ... ' + name)
        setid = 0
        for sett in self.quizlet.api.search.sets.get(params={'q': name})[
                'sets']:
            if sett['has_images'] == False:
                setid = sett['id']
        if not setid:
            setid = self.quizlet.api.search.sets.get(params={'q': name})[
                'sets'][0]['id']
        pprint(setid)
        my_set = self.quizlet.api.sets.get(setid)
        my_terms = my_set['terms']
        setcount = my_set["term_count"]
        for i in range(setcount):
            x = randint(0, setcount - 1)
            term = my_terms[x]['term']
            definition = my_terms[x]['definition']
            self.Speech.say("Definition,,,,, " +
                            definition + " ....Whats the term?")
            answer = self.Speech.listen()
            print(answer)
            if answer.lower() in term.lower():
                self.Speech.say("You are correct! The term is " + term)
            else:
                self.Speech.say("Incorrect! The term is " + term)
            if 'stop playing' in answer.lower():
                return 'Ok. Good Luck!'
        return "Good luck!"
