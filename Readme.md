# Yplay Music Player

Yplay player is based on youtube videos for downloading songs based on the keywords provided. The song, if not already present is downloaded and played using VLC player.

# Installation
1. ```pip install -r requirements.txt```
2. ```sudo apt-get install ffmpeg```

# Using Yplay
- Run ```python yplay.py [song keywords]``` eg. ```python yplay.py the night we met```
- To play multiple songs, run the command with comma separated song keywords.  
    eg.```python yplay.py lonestar amazed, with or without you```  
- Tip: Add alias to run the file ```alias yplay="python <path_to_yplay.py>"``` for easy usage. All the commands can then be run using just ```yplay``` from anywhere on the computer unstead of running ```python yplay.py``` inside the folder.  
eg. If you have cloned the repository on Desktop, then  
```alias yplay="python ~/Desktop/yplay-Music-Player/yplay,py"```  
and the script can be run as  
```yplay lonestar amazed, with or without you```

## Options
1. -r : Play any random song from downloaded ones.  
    ```python yplay.py -r``` or just run ```python yplay.py```  
    To play multiple random songs, run the command with number of songs you wish to play eg. ```python yplay.py -r 5```
    
2. -m : Manual download by supplying link.  
    ```python yplay.py -m <youtube_link_to_video>``` eg. ```python yplay.py -m https://www.youtube.com/watch?v=x-skFgrV59A```
