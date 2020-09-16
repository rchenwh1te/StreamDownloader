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


def MyFidelio(name, src):
	print('Detected source: https://www.myfidelio.at')
	def audio_process():
		global aud_seg
		audio_init_done = ''
		print('')
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
		while True:
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
				urllib.request.urlopen(url)
				valid.append(aud_seg)
			except urllib.error.HTTPError as exception:
				if aud_seg in invalid:
					audio_init_done = '.'
					break
					
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
		aud_range = aud_seg+1
		
		aud_file = open('audio.mp4','ab')
		#seg_id = 0
		debug_aud = open('../audio_rec.txt','a')
		for seg_id in range(aud_seg):
			seg_id_use = seg_id
			aud_ID = str(seg_id)
			aud_url = aud_src+'segment_'+aud_ID+'.m4s'
			while len(aud_ID)<len(str(aud_seg)):
				aud_ID = '0'+aud_ID
			download(aud_url, out='aud_seg_'+aud_ID+'.m4s',bar='')
			inaudsegfile = open('aud_seg_'+aud_ID+'.m4s','rb')
			aud_file.write(inaudsegfile.read())
			inaudsegfile.close()
			os.remove('aud_seg_'+aud_ID+'.m4s')
			debug_aud.write(aud_ID)
						
		print('Finished downloading audio.')
		aud_file.close()
		aud_done = '.'

	def video_process():
		global vid_seg
		print('')
		print('Initializing video...')
		
		video_init_done = ''
		vid_seg = 500
		ID_vid = str(vid_seg)
		url_vid = vid_src+'segment_'+ID_vid+'.m4s'
		valid_vid = []
		invalid_vid = []
		i_vid = 1000
		while True:
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
				urllib.request.urlopen(vid_url)
			except urllib.error.HTTPError as vid_exception:
				#print(vid_exception)
				if vid_seg in invalid_vid:
					video_init_done = '.'
					break
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
		vid_range = vid_seg+1
		debug_vid = open('../vid_debug.txt','a')
		vid_file = open('video.mp4','ab')
		#iden = 0
		for iden in range(vid_seg):
			iden_use = iden
			ID = str(iden)
			vid_url = vid_src+'segment_'+ID+'.m4s'
			while len(ID)<len(str(vid_seg)):
				ID = '0'+ID
			download(vid_url, out='vid_seg_'+ID+'.m4s',bar='')
			invidsegfile = open('vid_seg_'+ID+'.m4s','rb')
			vid_file.write(invidsegfile.read())
			invidsegfile.close()
			os.remove('vid_seg_'+ID+'.m4s')
			debug_vid.write(ID)

		global vid_done
		vid_file.close()
		vid_done = '.'
		print('Finished downloading video.')


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
	aud_src = 'https://'+src+'/audio/'+aud_opt[a]+'/dash/'
	vid_src = 'https://'+src+'/video/'+vid_opt[a]+'/dash/'
	
	audio_file = open('audio.mp4','wb')
	video_file = open('video.mp4','wb')
	
	download(aud_src+'init.mp4',out='aud_init.mp4',bar='')
	download(vid_src+'init.mp4',out='vid_init.mp4',bar='')
	
	audio_init_file = open('aud_init.mp4','rb')
	video_init_file = open('vid_init.mp4','rb')
	
	audio_file.write(audio_init_file.read())
	video_file.write(video_init_file.read())
	
	audio_file.close()
	video_file.close()
	
	os.system('cat aud_init.mp4 > audio.mp4')
	os.system('rm -f aud_init.mp4')
	os.system('cat vid_init.mp4 > video.mp4')
	os.system('rm -f vid_init.mp4')

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

	while True:
		try:
			aud_range
			vid_range
		except NameError:
			pass
		else:
			aseg = aud_seg
			vseg = vid_seg
			print('Pieces to download: Audio -',aseg,'| Video -',vseg)
			tot = aseg+vseg
			print('Total:',tot)
			total = progressbar.ProgressBar(max_value=aud_range+vid_range-2)

			while True:
				try:
					seg_id_use
					iden_use
				except Exception:
					pass
				else:
					break

			tdone = seg_id_use+iden_use
			while tdone<tot-2:
				tdone = seg_id_use+iden_use
				total.update(tdone)
			break
