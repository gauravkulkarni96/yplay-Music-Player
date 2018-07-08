from __future__ import unicode_literals
import youtube_dl
import requests
import random
import sys
import re
import os

DOWNLOAD_PATH = os.path.expanduser("~")+'/Documents/.yplay/'
HEADERS = {
	'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
	}
YOUTUBE_SEARCH_URL = "https://www.youtube.com/results?search_query="
YOUTUBE_VIDEO_BASE_URL = "https://www.youtube.com/watch?v="
VLC_BASE_COMMAND = "vlc --play-and-exit "
YDL_OPTS = {
		'outtmpl': DOWNLOAD_PATH+'%(id)s.%(ext)s',
	    'format': 'bestaudio/best',
	    'postprocessors': [{
	        'key': 'FFmpegExtractAudio',
	        'preferredcodec': 'mp3',
	        'preferredquality': '192',
	    }],
	}

def download_song_by_link(link):
	video_id = link.strip(" /").split("/")[-1]
	song_exists = search_downloaded_songs(video_id)
	if not song_exists:
		with youtube_dl.YoutubeDL(YDL_OPTS) as ydl:
		    ydl.download([link])

def download_song_by_id(video_id):
	song_link = YOUTUBE_VIDEO_BASE_URL + video_id
	download_song_by_link(song_link)
	return

def get_video_id(song_name):
	song_search_url = YOUTUBE_SEARCH_URL+song_name
	page = requests.get(song_search_url, headers = HEADERS)

	video_ids = re.findall(r"\"videoId\":\"\w+\"", str(page._content))[0]
	video_id = video_ids.split(":")[1].strip("\"")
	return video_id

def search_downloaded_songs(video_id):
	return os.path.exists(DOWNLOAD_PATH+video_id+'.mp3')

def get_songs_list_from_arguments(system_arguments):
	songs = "%20".join(system_arguments)
	songs = songs.replace("%20,", ",").replace(",%20", ",")
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
	regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

	if "youtube" in link and re.match(regex, link) is not None:
		return True
	return

def get_cleaned_link(link):
	link = link.split("&")[0].strip(" /")
	if not link.startswith("https://"):
		link = "https://"+link
	return link

def play_songs(song_files_list):
	for song_file_name in song_files_list:
		if not song_file_name.endswith(".mp3"):
			song_file_name+=".mp3"
		command = VLC_BASE_COMMAND + DOWNLOAD_PATH + song_file_name
		os.system(command)

def get_video_id_from_link(link):
	return link.split("=")[-1]

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
		song_link = get_cleaned_link(song_link)
		download_song_by_link(song_link)
		if "-noplay" not in sys.argv:
			video_id = get_video_id_from_link(song_link)
			play_songs([video_id])
	else:
		songs_list = get_songs_list_from_arguments(sys.argv[1:])
		for song_name in songs_list:
			video_id = get_video_id(song_name)
			song_exists = search_downloaded_songs(video_id)
			if not song_exists:
				try:
					download_song_by_id(video_id)
				except:
					print("Could not download the song. Try again!\n")
					exit(0)
			if "-noplay" not in sys.argv:
				print("Now Playing: {}".format(" ".join(song_name.split("%20"))))
				play_songs([video_id])