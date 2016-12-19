from pygame import mixer
mixer.init()
mixer.music.load(r'..\audio\song.mp3')
mixer.music.play()
print("\n\n")
try:
    while True:
        pass
except KeyboardInterrupt:
    pass
