import wget
from wget import *
import os
from os import *
import requests
import progressbar
import urllib
import time
import threading
import ffmpeg
import shutil

def MyFidelio(name, src):
	def audio_process():
		global aud_seg
		audio_init_done = ''
		print('Initializing audio...')
		aud_seg = 500
		ID = str(aud_seg)
		url = aud_src+'segment_'+ID+'.m4s'
		valid = []
		invalid = []
		i = 1000
		case = aud_seg
		if aud_seg == 0:
			case = 1
		while bool(audio_init_done)==False:
			if i==1000:
				aud_seg = aud_seg*2
				
			elif i ==1:
				aud_seg = aud_seg+i*3
				
			else:
				aud_seg = aud_seg+1
			if len(valid) != 0:
				while aud_seg <= valid[-1]:
					aud_seg = aud_seg+1
			ID = str(aud_seg)
			url = aud_src+'segment_'+ID+'.m4s'
			try:
				response = urllib.request.urlopen(url)
				valid.append(aud_seg)
			except urllib.error.HTTPError as exception:
				if aud_seg in invalid:
					audio_init_done = '.'
					
				else:
					invalid.append(aud_seg)
					if i==1000:
						aud_seg = int(aud_seg/4)*3
						i = 1
						
					else:
						aud_seg = aud_seg-int(i)
						
					i = i+1
			else:
				valid.append(aud_seg)    
			#DEBUG: print(aud_seg)
		print('Done initializing audio.')
		#return aud_seg
		print('')
		print('')
		global seg_id
		global seg_id_use
		global aud_range
		aud_range = aud_seg-1
		for seg_id in range(aud_range):
			seg_id_use = seg_id
			aud_ID = str(seg_id)
			aud_url = aud_src+'segment_'+aud_ID+'.m4s'

			while len(aud_ID)<len(str(aud_seg)):
				aud_ID = '0'+aud_ID
			download(aud_url, out='aud_seg_'+aud_ID+'.m4s',bar='')
			system('cat aud_seg_'+aud_ID+'.m4s >> audio.mp4')
			system('rm -f aud_seg_'+aud_ID+'.m4s')
				
		aud_done = '.'

	def video_process():
		global vid_seg
		print('Initializing video...')
		video_init_done = ''
		vid_seg = 500
		ID_vid = str(vid_seg)
		url_vid = vid_src+'segment_'+ID_vid+'.m4s'
		valid_vid = []
		invalid_vid = []
		i_vid = 1000
		while bool(video_init_done)==False:
			if i_vid==1000:
				vid_seg = vid_seg*2
				
			elif i_vid ==1:
				vid_seg = vid_seg+i*3
				
			else:
				vid_seg = vid_seg+1
				
			if len(valid_vid) != 0:
				while vid_seg <= valid_vid[-1]:
					vid_seg = vid_seg+1
					
			ID_vid = str(vid_seg)
			vid_url = vid_src+'segment_'+ID_vid+'.m4s'
			try:
				response = urllib.request.urlopen(vid_url)
			except urllib.error.HTTPError as vid_exception:
				#print(vid_exception)
				if vid_seg in invalid_vid:
					video_init_done = '.'
				else:
					invalid_vid.append(vid_seg)
					if i_vid==1000:
						vid_seg = int(vid_seg/4)*3
						i_vid = 1
						
					else:
						vid_seg = vid_seg-int(i_vid)
						
					i_vid = i_vid+1
			else:
				valid_vid.append(vid_seg)
			    
			#DEBUG: print(vid_seg)
		print('Done initializing video.')
		
		print('')
		print('')
		
		global iden
		global iden_use
		global vid_range
		vid_range = vid_seg-1
		for iden in range(vid_range):
			iden_use = iden
			ID = str(iden)
			vid_url = vid_src+'segment_'+ID+'.m4s'
			
			while len(ID)<len(str(vid_seg)):
				ID = '0'+ID
			download(vid_url, out='vid_seg_'+ID+'.m4s',bar='')
			system('cat vid_seg_'+ID+'.m4s >> video.mp4')
			system('rm -f vid_seg_'+ID+'.m4s')
		global vid_done
		vid_done = '.'


	aud_opt = ['1_stereo_128000','1_stereo_360000','1_stereo_640000']
	aud_opt_man = ['128 kbps','360 kbps','640 kbps']

	vid_opt = ['144_190464','288_380928','360_688128','432_1097728','576_1404928','720_2287616','1080_3112960']
	vid_opt_man = ['144p - 190 kbps','288p - 381 kbps','360p - 688 kbps','432p - 1098 kbps','576p - 1405 kbps','HD 720p - 2288 kbps','Full HD 1080p - 3113 kbps']

	print('Audio resolution selection:')

	for l in range(len(aud_opt)):
		print('['+str(l)+'] '+aud_opt_man[l])

	a = int(input('Enter preferred audio resolution id: '))

	print('')

	print('Video resolution selection:')

	for l in range(len(vid_opt)):
		print('['+str(l)+'] '+vid_opt_man[l])

	v = int(input('Enter preferred video resolution id: '))

	global aud_src
	global vid_src
	aud_src = src+'/audio/'+aud_opt[a]+'/dash/'
	vid_src = src+'/video/'+vid_opt[a]+'/dash/'

	download(aud_src+'init.mp4',out='aud_init.mp4',bar='')
	download(vid_src+'init.mp4',out='vid_init.mp4',bar='')
	system('cat aud_init.mp4 > audio.mp4')
	system('rm -f aud_init.mp4')
	system('cat vid_init.mp4 > video.mp4')
	system('rm -f vid_init.mp4')

	print('')
	print('Initializing, this may take a while.')

	threading.Thread(target=audio_process).start()
	threading.Thread(target=video_process).start()

	global aud_done
	global vid_done
	aud_done = ''
	vid_done = ''
	check = '.'
	global audio_init_done
	global video_init_done
	audio_init_done = ''
	video_init_done = ''
	adone = audio_init_done
	vdone = video_init_done
	todone = '.'

	if adone == '' or vdone == '':
		print('')

	while bool(todone):
		try:
			aud_range
			vid_range
		except NameError:
			JustARandomUselessVariable = ''
		else:
			todone = ''
			
	aseg = aud_range
	vseg = vid_range
	print('Pieces to download: Audio -',aseg,'; Video -',vseg)
	tot = aseg+vseg
	print('Total:',tot)
	total = progressbar.ProgressBar(max_value=aud_range+vid_range)
	totdone = '.'

	#while bool(totdone):
	#	try:
	#		aud_seg_use
	#		iden_use
	#	except NameError:
	#		UselessVariable = ''
	#	else:
	#		totdone = ''

	tdone = seg_id_use+iden_use
	while tdone<tot:
		tdone = seg_id_use+iden_use
		total.update(tdone)

print('''
StreamDownloader
__________________________________________________
|                      |                         |
|Manual:               |  README                 |
|----------------------|-------------------------|
|Author:               |  Reina Chen             |
|----------------------|-------------------------|
|Version:              |  1.0.1                  |
|______________________|_________________________|

Thank you for using our software.

Disclaimer: This script has been created specifically for Sites Said in menu. It hasn't been tested on other streaming sites.
''')

#NOTE: get other resolutions. Give options.

#1080p

#NOTE: DONE!

name = input('Enter project name: ')
mkdir(name)
chdir(name)
menu = ['MyFidelio']

for men in range(len(menu)):
	print('['+str(men)+'] '+menu[men])

sel = int(input('Select site by id: '))	

mkdir('temp')
chdir('temp')
src = input('Enter source (see README): ')

if sel == 0:
	MyFidelio(name, src)

while bool(check):
	if aud_done == '.' and vid_done == '.':
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
		#system('rm -rf temp')

		print('''Download completed successfuly.
		Thank you for using my script.
		''')
		exit()
