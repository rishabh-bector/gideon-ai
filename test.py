import youtube_dl as yd
import requests
from bs4 import BeautifulSoup


options = {
    'format': 'bestaudio/best',  # choice of quality
    'extractaudio': True,      # only keep the audio
    'audioformat': "mp3",      # convert to mp3
    'outtmpl': '%(id)s',        # name the file the ID of the video
    'noplaylist': True,        # only download single song, not playlist
}


textToSearch = 'she will be loved by maroon 5'
url = "https://www.youtube.com/results"
response = requests.get(url, params={'search_query': textToSearch})
html = response.text
# print(html)

soup = BeautifulSoup(html, 'lxml')
for vid in soup.findAll(attrs={'class': 'yt-uix-tile-link'}):
    print('https://www.youtube.com' + vid['href'])


with youtube_dl.YoutubeDL(options) as ydl:
    ydl.download([url])
