import speech_recognition as sr
import subprocess
from gtts import gTTS
import os


class SpeechController:

    def __init__(self, name, language):

        self.lang = language
        self.name = name.lower()
        self.r = sr.Recognizer()
        self.m = sr.Microphone()
        self.inputmode = 'input'

    def switchmode(self, response):
        self.inputmode = response['parameters']['mode']
        return 'Input mode switched to ' + self.inputmode

    def listen(self):
        with self.m as source:
            audio = self.r.listen(source)
        try:
            return self.r.recognize_google(audio, language=self.lang)
        except sr.UnknownValueError:
            return 'Error:Audio'

    def sayagain(self, msg):
        self.say(self.lastsaid)
        return msg

    def listenForStart(self):
        if self.inputmode == 'input':
            micIn = ''
            input('>')
            micIn = self.listen().lower()
            print(micIn)
            return micIn
        if self.inputmode == 'continous':
            micIn = self.listen().lower()
            print(micIn)
            return micIn
        if self.inputmode == 'keyword':
            print('Waiting for keyword ' + "'" + self.name + "'")
            micIn = ''
            while self.name not in micIn:
                micIn = self.listen().lower()
            self.say("I'm listening")
            micIn = self.listen().lower()
            return micIn

    def say(self, txt):
        txt = str(txt)
        self.lastsaid = txt
        try:
            if os.name == 'nt':
                try:
                    return_code = subprocess.call(
                        'echo ' + txt + ' | cscript "C:\Program Files\Jampal\ptts.vbs" -r 2 1>dank 2>meme', shell=True)
                except Exception:
                    print("Get Jampal TTS at http://jampal.sourceforge.net/ptts.html")
            elif os.name == 'posix':
                return_code = subprocess.call("say " + txt, shell=True)
        except KeyboardInterrupt:
            pass
