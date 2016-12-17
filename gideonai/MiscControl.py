import requests
import json
import pyowm
from pprint import pprint
from quizlet import QuizletClient
from random import randint
from gideonai import SpeechControl as SC
from gideonai import RequestControl as RC
import pyjokes
import pafy
from bs4 import BeautifulSoup
import subprocess


class MiscController:

    def __init__(self):
        self.quizletid = 'EGeXd4J2jH'
        self.Speech = SC.SpeechController('Gideon', 'en-uk')
        self.quizletkey = 'wJ5qBU5SmcTa4NTq92jAHh'
        self.quizlet = QuizletClient(
            client_id=self.quizletid, login=self.quizletkey)
        self.RequestHandler = RC.RequestController()
        self.junkQueries = {'whatis': ['what is', 'who is']}

    def quiz(self, response):

        name = response['parameters']['quizname']
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
        x = randint(0, setcount - 1)
        for i in range(setcount):
            x += 1
            if x == setcount:
                x = 0
            term = my_terms[x]['term']
            definition = my_terms[x]['definition']
            self.Speech.say("Definition,,,,, " +
                            definition + " ....Whats the term?")
            answer = self.Speech.listen()
            print(answer)
            if answer.lower() in term.lower():
                self.Speech.say("You are correct! The term is " + term)
            elif answer.lower() == "interrupt":
                query = self.Speech.listen()
                self.RequestHandler.handle_request(query)
            else:
                self.Speech.say("Incorrect! The term is " + term)
            if answer.lower() == 'stop playing':
                return 'Ok. Good Luck!'
        return "Good luck!"

    def getJoke(self, response):
        return pyjokes.get_joke()

    def getMusic(self, response):

        song = response['parameters']['songname']

        try:
            artist = response['parameters']['artist']
        except Exception:
            artist = ''

        textToSearch = song

        if artist != '':
            textToSearch += ' by ' + artist

        url = 'https://www.youtube.com/results'
        response = requests.get(
            url, params={'search_query': textToSearch + ' lyrics'})
        html = response.text

        soup = BeautifulSoup(html, 'lxml')

        vids = []

        for vid in soup.findAll(attrs={'class': 'yt-uix-tile-link'}):

            vids.append('https://www.youtube.com' + vid['href'])

        video = pafy.new(vids[0])
        streams = video.audiostreams

        cstream = None

        for s in streams:
            # print(s.extension)
            if s.extension == 'm4a':
                cstream = s
                break

        cstream.download('song.m4a')

        subprocess.call(['ffmpeg', '-y', '-i', 'song.m4a', '-acodec',
                         'libmp3lame', '-ab', '256k', 'song.mp3'])

        return_code = subprocess.call(['afplay', 'song.mp3'])
