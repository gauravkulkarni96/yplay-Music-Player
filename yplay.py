from __future__ import unicode_literals
import youtube_dl
import requests
from bs4 import BeautifulSoup as bs
import sys
import re

def download_song(link):
	ydl_opts = {
	    'format': 'bestaudio/best',
	    'postprocessors': [{
	        'key': 'FFmpegExtractAudio',
	        'preferredcodec': 'mp3',
	        'preferredquality': '192',
	    }],
	    # 'outtmpl': '/home/gaurav/Desktop/file.mp4',
	}
	with youtube_dl.YoutubeDL(ydl_opts) as ydl:
	    ydl.download([link])

def get_link(song_name):
	youtube_search_url = "https://www.youtube.com/results?search_query="+song_name

	headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
	page = requests.get(youtube_search_url, headers = headers)
	# soup = bs((page._content), "html.parser")
	# area = soup.findAll("a", {"id":"video-title"})
	video_ids = re.findall(r"\"videoId\":\"\w+\"", str(page._content))[0]
	video_id = video_ids.split(":")[1].strip("\"")
	link = "https://www.youtube.com/watch?v="+video_id
	return link


if __name__ == "__main__":
	if len(sys.argv) == 1:
		print("Please pass the song name")
		exit(0)
	song_name = "%20".join(sys.argv[1:])
	link = get_link(song_name)
	download_song(link)
