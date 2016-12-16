import apiai
import json
import SpeechControl as SC
import KnowledgeControl as KC
import RequestControl as RC
import re


class LogicController:

    def __init__(self, name, language):
        self.name = name
        self.language = language

        self.Speech = SC.SpeechController(self.name, self.language)
        self.Knowledge = KC.KnowledgeController()
        self.RequestHandler = RC.RequestController()

        self.actions = {'weather.search': self.Knowledge.getWeather,
                        'wisdom': self.Knowledge.ask,
                        'quizlet': self.Knowledge.quiz,
                        'switchmode': self.Speech.switchmode,
                        'sayagain': self.Speech.sayagain}

    def run(self):
        while True:
            query = self.Speech.listenForStart()  # listen for query
            output = self.RequestHandler.handle_request(
                query)  # handle request
            ###   Check for API Speech response ###
            try:
                actionOutput = output['result']['fulfillment']['speech']
            except Exception:
                actionOutput = 'Sorry, my neural core seems to have malfunctioned.'

            # print('actionOutput : ' + actionOutput)

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
