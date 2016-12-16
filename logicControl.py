import apiai
import json
import SpeechControl as SC
import KnowledgeControl as KC
import re


class LogicController:

    def __init__(self, name, language):
        self.name = name
        self.language = language

        self.Speech = SC.SpeechController(self.name, self.language)
        self.Knowledge = KC.KnowledgeController()

        self.aiToken = '786ff37f7053431bb6ef050394521fcd'

        self.ai = apiai.ApiAI(self.aiToken)

        self.actions = {'weather.search': self.Knowledge.getWeather,
                        'wisdom': self.Knowledge.ask,
                        'quizlet': self.Knowledge.quiz,
                        'switchmode': self.Speech.switchmode}

    def run(self):

        while True:

            request = self.ai.text_request()
            request.lang = 'en'
            request.session_id = 's1'

            request.query = self.Speech.listenForStart()  # input('> ')
            print(request.query)
            if request.query == 'No Audio' or request.query == None:
                continue

            response = request.getresponse()
            x = str(response.read())

            output = ''

            ### Convert byte code into dict ###

            try:
                x = x.replace('false', 'False')
                x = x.replace('true', 'True')
                output = eval(eval(x))
            except NameError:
                print('Error in API response')

            print(output)

            ###   Check for API Speech response ###

            try:
                actionOutput = output['result']['fulfillment']['speech']
            except Exception:
                actionOutput = 'Sorry, my neural core seems to have malfunctioned.'

            ###   If None, check for actions   ###

            if actionOutput == '':
                print('No API Speech Response')

                action = output['result']['action']

                for a in self.actions:
                    if a in action:
                        actionOutput = self.actions[a](output['result'])

            print(actionOutput)

            try:
                self.Speech.say(actionOutput)
            except Exception:
                self.Speech.say('Nothing to say')


Brain = LogicController('Gideon', 'en-uk')
Brain.run()
