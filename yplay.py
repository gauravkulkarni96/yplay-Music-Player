from __future__ import unicode_literals
import youtube_dl
import requests
import random
import sys
import re
import os

DOWNLOAD_PATH = os.path.expanduser("~")+'/Documents/.yplay/'

ydl_opts = {
		'outtmpl': DOWNLOAD_PATH+'%(id)s.%(ext)s',
	    'format': 'bestaudio/best',
	    'postprocessors': [{
	        'key': 'FFmpegExtractAudio',
	        'preferredcodec': 'mp3',
	        'preferredquality': '192',
	    }],
	}

def download_song_by_link(link):
	with youtube_dl.YoutubeDL(ydl_opts) as ydl:
	    ydl.download([link])

def download_song_by_id(video_id):
	link = "https://www.youtube.com/watch?v="+video_id
	download_song_by_link(link)
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

def get_songs_list_from_arguments(system_arguments):
	songs = "%20".join(system_arguments)
	songs = songs.replace("%20,", ",")
	songs = songs.replace(",%20", ",")
	songs_list = songs.split(",")
	return songs_list

def select_n_random_songs(n):
	songs = os.listdir(DOWNLOAD_PATH)
	if len(songs) == 0:
		print("No downloaded songs!")
		exit(0)
	if n > len(songs):
		n = len(songs)
	return random.sample(songs, n)

def youtube_link_is_valid(link):
	# TODO
	return True

def play_songs(song_files_list):
	for song_file_name in song_files_list:
		if not song_file_name.endswith(".mp3"):
			song_file_name+=".mp3"
		command = "vlc --play-and-exit " + DOWNLOAD_PATH + song_file_name
		os.system(command)

def get_video_id_from_link(link):
	return link.split("/")[-1]

if __name__ == "__main__":
	if len(sys.argv) == 1 or sys.argv[1] == "-random" or sys.argv[1] == "-r":
		count = 1
		if len(sys.argv) == 3:
			try:
				count = int(sys.argv[2])
			except:
				pass
		selected_songs = select_n_random_songs(count)
		play_songs(selected_songs)
			
	elif sys.argv[1] == "-manual" or sys.argv[1] == "-m":
		song_link = sys.argv[2]
		if not youtube_link_is_valid(song_link):
			print("Incorrect youtube Link!!")
			exit(0)
		download_song_by_link(link)
		video_id = get_video_id_from_link(link)
		play_songs([video_id])
	else:
		songs_list = get_songs_list_from_arguments(sys.argv[1:])
		for song_name in songs_list:
			video_id = get_video_id(song_name)
			song_exists = search_songs(video_id)
			if not song_exists:
				try:
					download_song_by_id(video_id)
				except:
					print("Could not download the song. Try again!\n")
					exit(0)
			print("Now Playing: {}".format(" ".join(song_name.split("%20"))))
			play_songs([video_id])