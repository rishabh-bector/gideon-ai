import speech_recognition as sr
import subprocess
from gtts import gTTS


class SpeechController:

    def __init__(self, name, language):

        self.lang = language
        self.name = name.lower()
        self.r = sr.Recognizer()
        self.m = sr.Microphone()
        self.inputmode = 'keyword'

    def switchmode(self, response):
        self.inputmode = response['parameters']['mode']
        return 'Input mode switched to ' + self.inputmode

    def listen(self):
        with self.m as source:
            audio = self.r.listen(source)
        try:
            return self.r.recognize_google(audio)
        except sr.UnknownValueError:
            return 'Error:Audio'

    def listenForStart(self):
        if self.inputmode == 'input':
            micIn = ''
            input('>')
            micIn = self.listen().lower()
            # print(micIn)
            return micIn

        if self.inputmode == 'continuous':
            micIn = self.listen().lower()
            # print(micIn)
            if micIn == 'error:audio':
                return 'No Audio'
            return micIn

        if self.inputmode == 'keyword':
            print('Waiting for keyword ' + "'" + self.name + "'")
            micIn = ''
            while self.name not in micIn:
                micIn = self.listen().lower()
                print('Buffer: ' + micIn)
            self.say("I'm listening")
            micIn = self.listen().lower()
            return micIn

        else:
            self.inputmode = 'continuous'
            self.say('Sorry about that. Switching back to continuous.')

    def say(self, txt):
        try:
            audio_file = 'hello.mp3'
            tts = gTTS(text=txt, lang=self.lang)
            tts.save(audio_file)
            return_code = subprocess.call(['afplay', '-r', '1.3', audio_file])
        except KeyboardInterrupt:
            pass
