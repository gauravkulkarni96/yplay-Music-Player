from __future__ import unicode_literals
import youtube_dl
import requests
import random
import sys
import re
import os

DOWNLOAD_PATH = os.path.expanduser("~")+'/Documents/.yplay/'

def download_song(video_id):
	ydl_opts = {
		'outtmpl': DOWNLOAD_PATH+'%(id)s.%(ext)s',
	    'format': 'bestaudio/best',
	    'postprocessors': [{
	        'key': 'FFmpegExtractAudio',
	        'preferredcodec': 'mp3',
	        'preferredquality': '192',
	    }],
	}
	link = "https://www.youtube.com/watch?v="+video_id
	with youtube_dl.YoutubeDL(ydl_opts) as ydl:
	    ydl.download([link])
	return

def get_video_id(song_name):
	youtube_search_url = "https://www.youtube.com/results?search_query="+song_name

	headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
	page = requests.get(youtube_search_url, headers = headers)

	video_ids = re.findall(r"\"videoId\":\"\w+\"", str(page._content))[0]
	video_id = video_ids.split(":")[1].strip("\"")
	return video_id

def search_songs(video_id):
	return os.path.exists(DOWNLOAD_PATH+video_id+'.mp3')

def select_random_song():
	songs = os.listdir(DOWNLOAD_PATH)
	if len(songs) == 0:
		print("No downloaded songs!")
		exit(0)
	return random.choice(songs).split(".")[0]


if __name__ == "__main__":
	if len(sys.argv) == 1 or sys.argv[1] == "-random":
		video_id = select_random_song()
		command = "vlc --play-and-exit "+DOWNLOAD_PATH+video_id+".mp3"
		os.system(command)
	else:
		songs = "%20".join(sys.argv[1:])
		songs = songs.replace("%20,", ",")
		songs = songs.replace(",%20", ",")
		songs_list = songs.split(",")
		for song_name in songs_list:
			video_id = get_video_id(song_name)
			song_exists = search_songs(video_id)
			if not song_exists:
				try:
					download_song(video_id)
				except:
					print("Could not download the song. Try again!\n")
					exit(0)
			print("Now Playing: {}".format(" ".join(song_name.split("%20"))))
			command = "vlc --play-and-exit "+DOWNLOAD_PATH+video_id+".mp3"
			os.system(command)