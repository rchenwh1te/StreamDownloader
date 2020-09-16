#!/bin/python3
import wget
from wget import *
import os
import requests
import progressbar
import urllib
import time
import threading
import ffmpeg
import shutil
import Sources.MyFidelio

print('''
StreamDownloader
__________________________________________________
|                      |                         |
|Manual:               |  README                 |
|----------------------|-------------------------|
|Author:               |  Reina Chen             |
|----------------------|-------------------------|
|Version:              |  1.0.4                  |
|______________________|_________________________|

Thank you for using our software.

Disclaimer: This script has been created specifically for Sites Said in manual. It hasn't been tested on other streaming sites.
''')

name = input('Enter project name: ')
os.mkdir(name)
os.chdir(name)

os.mkdir('temp')
os.chdir('temp')
src = input('Enter source (see README): ')

CheckSource = src.split('/')

if CheckSource[0] == 'd279gtpur1viyb.cloudfront.net':
	MyFidelio.MyFidelio(name, src)

print('merging audio and video...')
vid_in = ffmpeg.input('./video.mp4')
aud_in = ffmpeg.input('./audio.mp4')

ffmpeg.concat(vid_in,aud_in,v=1,a=1).output('../'+name+'.mp4').run

#system("ffmpeg -i video.mp4 -i audio.mp4 -c:v copy -c:a aac '"+name+".mp4'")

#print('moving temp file to folder...')
#system("mv '"+name+".mp4' ../")

print('deleting temp directory...')
chdir('../')
shutil.rmtree('./temp')
rmdir('./temp')

print('''Download completed successfuly.
Thank you for using my script.
''')
