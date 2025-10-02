#!/bin/python3
#
# kyosk.py
#
# Author:  Torres Anguiano Azael Arturo
# Date:    2025-09-29
# License: MIT
#
# Plays a video file using VLC with the Raspberry Pi
#

import vlc
import time

def video_Ejer1():
   player = vlc.MediaPlayer()
   video = vlc.Media('/home/artsol/videos/video.mp4')
   player.set_media(video)
   player.play()
   time.sleep(5)
   player.stop()

def image_Ejer1():
   vlc_instance = vlc.Instance()
   player = vlc_instance.media_list_player_new()

   photos = ['/home/artsol/pictures/pic01.jpg',
	     '/home/artsol/pictures/pic02.jpg',
	     '/home/artsol/pictures/pic03.jpg',
	     '/home/artsol/pictures/pic04.jpg']

   Media = vlc_instance.media_list_new(photos)
   player.set_media_list(Media)

   while True:
       for i, name in enumerate(photos):
           player.play_item_at_index(i)
           time.sleep(5)

def main():
   video_Ejer1()
   image_Ejer1()

main()

