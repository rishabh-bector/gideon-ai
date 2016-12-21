import requests
import json
import pyowm
import os
from pprint import pprint
from quizlet import QuizletClient
from random import randint
from gideonai import SpeechControl as SC
from gideonai import RequestControl as RC
import pyjokes
import pafy
from bs4 import BeautifulSoup
import subprocess
from pydub import AudioSegment
from threading import Thread

if os.name == 'nt':
    from pygame import mixer


class MiscController:

    def __init__(self):
        self.quizletid = 'EGeXd4J2jH'
        self.Speech = SC.SpeechController('Gideon', 'en-uk')
        self.quizletkey = 'wJ5qBU5SmcTa4NTq92jAHh'
        self.quizlet = QuizletClient(
            client_id=self.quizletid, login=self.quizletkey)
        self.RequestHandler = RC.RequestController()
        self.junkQueries = {'whatis': ['what is', 'who is']}

    def quiz(self, actions, response):

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
            answer = self.Speech.listenForStart()
            print(answer)
            if answer.lower() in term.lower():
                self.Speech.say("You are correct! The term is " + term)
            elif answer.lower() == "interrupt":
                query = self.Speech.listen()
                msg = self.RequestHandler.handle_request(query)
                try:
                    msg = actions.get(msg["result"]["action"], str)() or msg["result"]["fulfillment"]["speech"] or "sorry, couldn't find a response..."
                except KeyError or NameError:
                    msg = ""
                if ' '.split(msg)[0] == "exec":
                    exec(code[1])
                else:
                    self.Speech.say(msg)
            else:
                self.Speech.say("Incorrect! The term is " + term)
            if answer.lower() == 'stop playing':
                return 'Ok. Good Luck!'
        return "Good luck!"
    def retrn(self):
        return "exec return"
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
        if not os.path.isdir('./gideonai'):
            os.chdir(input(
                'enter the path of your gideonai installation (where you cloned the repo): '))
        cstream = None

        for s in streams:
            # print(s.extension)
            if s.extension == 'm4a':
                cstream = s
                break
        try:
            if os.name == 'posix':
                cstream.download('audio/song.m4a')
                subprocess.call(['ffmpeg', '-y', '-i', 'audio/song.m4a', '-acodec',
                                 'libmp3lame', '-ab', '256k', 'audio/song.mp3'])

                return_code = subprocess.call(['afplay', 'audio/song.mp3'])
            elif os.name == 'nt':
                try:
                    os.remove(r"audio\song.m4a")
                except FileNotFoundError:
                    pass
                cstream.download(r"audio\song.m4a")
                m4a_file = AudioSegment.from_file(r"audio\song.m4a", "m4a")
                mp3_file = m4a_file.export(r"audio\song.mp3", format="mp3")
                mp3_file.close()
                # del mp3_file
                process = Thread(target=self.playMusic, name='song',
                                 args=(r'audio\song.mp3',))
                process.start()
                # process.join()
                return "pass"

        except KeyboardInterrupt:
            mixer.music.stop()
            # i don't know how to stop afplay

    def playMusic(self, fname):
        subprocess.call("cd gideonai && python playsong.py", shell=True)
