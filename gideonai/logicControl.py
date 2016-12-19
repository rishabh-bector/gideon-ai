import apiai
import json

from gideonai import SpeechControl as SC
from gideonai import KnowledgeControl as KC
from gideonai import RequestControl as RC
from gideonai import MiscControl as MC

import re


class LogicController:

    def __init__(self, name, language):
        self.name = name
        self.language = language

        self.Speech = SC.SpeechController(self.name, self.language)
        self.Knowledge = KC.KnowledgeController()
        self.RequestHandler = RC.RequestController()
        self.Misc = MC.MiscController()

        self.actions = {'weather.search': self.Knowledge.getWeather,
                        'wisdom': self.Knowledge.ask,
                        'quizlet': self.Misc.quiz,
                        'switchmode': self.Speech.switchmode,
                        'sayagain': self.Speech.sayagain,
                        'getjoke': self.Misc.getJoke,
                        'getmusic': self.Misc.getMusic}

    def run(self):
        while True:
            query = self.Speech.listenForStart()  # listen for query
            if query == '' or query == 'error:audio':
                # print('bad')
                continue
            output = self.RequestHandler.handle_request(
                query)  # handle request

            ###   Check for API Speech response ###

            try:
                actionOutput = output['result']['fulfillment']['speech']
            except Exception:
                actionOutput = 'Sorry, my neural core seems to have malfunctioned.'

            ###   If None, complete action   ###

            if actionOutput == '':
                print('No API Speech Response')

                action = output['result']['action']

                for a in self.actions:
                    if a in action:
                        actionOutput = self.actions[a](output['result'])
            try:
                self.Speech.say(actionOutput)
            except Exception:
                self.Speech.say('Nothing to say')

Brain = LogicController('Gideon', 'en-uk')
if __name__ == "__main__":
    Brain.run()
