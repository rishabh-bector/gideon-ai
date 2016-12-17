from pygame import mixer
mixer.init()
mixer.music.load(r'..\audio\song.mp3')
mixer.music.play()
print("\n\n")
while True:
    try:
        pass
    except KeyboardInterrupt:
        break
