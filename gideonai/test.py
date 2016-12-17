import pafy
import requests
from bs4 import BeautifulSoup
import subprocess


textToSearch = 'payphone by maroon 5'
url = 'https://www.youtube.com/results'
response = requests.get(url, params={'search_query': textToSearch + ' lyrics'})
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
