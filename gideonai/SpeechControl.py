import speech_recognition as sr
import subprocess
from gtts import gTTS
import os
import random

if os.name == 'nt':
    from pygame import mixer
    mixer.init(30000)
    subprocess.call("rd /S /Q audio", shell=True)
    subprocess.call("md audio", shell=True)
elif os.name == 'posix':
    subprocess.call("rm -rf audio;mkdir -p audio", shell=True)


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

    def sayagain(self):
        with open('log.txt', 'r') as openfile:
            self.lastsaid = openfile.readlines()[-1][:-2]
        self.say(self.lastsaid)
        return ""

    def listenForStart(self):
        if self.inputmode == 'input':
            micIn = ''
            x = input('>')
            if x == '':
                micIn = self.listen().lower()
                print(micIn)
                return micIn
            return x
        if self.inputmode == 'continuous':
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
        else:
            self.inputmode == 'input'
            return 'error:audio'

    def say(self, txt):
        txt = str(txt)
        with open('log.txt', 'a') as openfile:
            openfile.write(txt + "\n")
        print(txt)
        try:
            if os.name == 'nt':
                audio_file = r"audio\hello_" + \
                    str(random.randint(1, 1000)) + ".mp3"
                tts = gTTS(text=txt, lang="en-uk")
                tts.save(audio_file)
                mixer.music.load(audio_file)
                mixer.music.play()
            elif os.name == 'posix':
                audio_file = "audio/hello.mp3"
                tts = gTTS(text=txt, lang="en-uk")
                tts.save(audio_file)
                return_code = subprocess.call(
                    ["afplay", "-r", "1.3", audio_file])
        except KeyboardInterrupt:
            pass
