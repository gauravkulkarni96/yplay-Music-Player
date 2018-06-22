# Yplay Music Player

Yplay player is based on youtube videos for downloading songs based on the keywords provided. The song, if not already present is downloaded and played using VLC player.

# Installation
1. ```pip install -r requirements.txt```
2. ```sudo apt-get install ffmpeg```

# Using Yplay
- Run ```python yplay.py [song keywords]``` eg. ```python yplay.py the night we met```
- To play multiple songs, run the command with comma separated song keywords. 

eg.```python yplay.py lonestar amazed, with or without you```

## Options
1. -r : To play any random song from downloaded ones.

```python yplay.py -r``` or just run ```python yplay.py```

To play multiple random songs, run the command with number of songs you wish to play eg. ```python yplay.py -r 5```
