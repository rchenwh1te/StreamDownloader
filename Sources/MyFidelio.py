import wget
from wget import *
import os
import sys
import requests
import progressbar
import urllib
import time
import threading
import ffmpeg
import shutil
import PySimpleGUI as sg

attempts = 0
maxAttempts = 15
sleepTime = 2

def MyFidelio(name, src):
	print('Detected source: https://www.myfidelio.at')
	def audio_process():
		global aud_seg
		audio_init_done = ''
		print('')
		print('Initializing audio...\n')
		
		aud_seg = 500
		ID = str(aud_seg)
		url = str(aud_src+'segment_'+ID+'.m4s')
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
			url = str(aud_src+'segment_'+ID+'.m4s')
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
		for seg_id in range(aud_seg):
			aud_size = os.stat('audio.mp4').st_size
			seg_id_use = seg_id
			aud_ID = str(seg_id)
			aud_url = str(aud_src+'segment_'+aud_ID+'.m4s')
			while len(aud_ID)<len(str(aud_seg)):
				aud_ID = '0'+aud_ID
			aud_outfilename = 'aud_seg_'+aud_ID+'.m4s'

			urllib.request.urlretrieve(str(aud_url),str(aud_outfilename))

			inaudsegfile = open(str('aud_seg_'+aud_ID+'.m4s'),'rb')
			aud_file.write(inaudsegfile.read())
			inaudsegfile.close()

			#if totalSize == aud_size+seg_size:
			#time.sleep(3)
			os.remove(aud_outfilename)
						
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
		url_vid = str(vid_src+'segment_'+ID_vid+'.m4s')
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
			vid_url = str(vid_src+'segment_'+ID_vid+'.m4s')
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
		vid_file = open('video.mp4','ab')
		#iden = 0
		for iden in range(vid_seg):
			iden_use = iden
			ID = str(iden)
			vid_url = vid_src+'segment_'+ID+'.m4s'
			while len(ID)<len(str(vid_seg)):
				ID = '0'+ID
			vidoutfilename = 'vid_seg_'+ID+'.m4s'
			
			while True:
				try:
					urllib.request.urlretrieve(str(vid_url), vidoutfilename)
				except Exception:
					pass
				else:
					break
			invidsegfile = open(str('vid_seg_'+ID+'.m4s'),'rb')
			vid_file.write(invidsegfile.read())
			invidsegfile.close()
			#sleep(3)
			os.remove(vidoutfilename)

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
	
	#download.Download(aud_src+'init.mp4','aud_init.mp4','aud_init.mp4')
	#download.Download(vid_src+'init.mp4','aud_init.mp4','aud_init.mp4')
	
	download(str(aud_src)+'init.mp4',out='aud_init.mp4',bar='')
	download((vid_src)+'init.mp4',out='vid_init.mp4',bar='')
	
	audio_init_file = open('aud_init.mp4','rb')
	video_init_file = open('vid_init.mp4','rb')
	
	audio_file.write(audio_init_file.read())
	video_file.write(video_init_file.read())
	
	audio_file.close()
	video_file.close()
	
	try:
		os.remove('aud_init.mp4')
		os.remove('vid_init.mp4')
	except Exception:
		pass
	
	#os.system('cat aud_init.mp4 > audio.mp4')
	#os.system('rm -f aud_init.mp4')
	#os.system('cat vid_init.mp4 > video.mp4')
	#os.system('rm -f vid_init.mp4')

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
			
def Silent(src, aud_q, vid_q, total_pb, percent):
	def audio_process():
		global aud_seg
		audio_init_done = ''
		#print('')
		print('Initializing audio...\n')
		
		aud_seg = 500
		ID = str(aud_seg)
		url = str(aud_src+'segment_'+ID+'.m4s')
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
			url = str(aud_src+'segment_'+ID+'.m4s')
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
		global seg_id
		global seg_id_use
		global aud_range
		aud_range = aud_seg+1
		
		aud_file = open('audio.mp4','ab')
		#seg_id = 0
		for seg_id in range(aud_seg):
			aud_size = os.stat('audio.mp4').st_size
			aud_ID = str(seg_id)
			aud_url = str(aud_src+'segment_'+aud_ID+'.m4s')
			while len(aud_ID)<len(str(aud_seg)):
				aud_ID = '0'+aud_ID
			aud_outfilename = 'aud_seg_'+aud_ID+'.m4s'

			urllib.request.urlretrieve(str(aud_url),str(aud_outfilename))

			inaudsegfile = open(str('aud_seg_'+aud_ID+'.m4s'),'rb')
			aud_file.write(inaudsegfile.read())
			inaudsegfile.close()
			seg_id_use = seg_id+1

			#if totalSize == aud_size+seg_size:
			#time.sleep(3)
			os.remove(aud_outfilename)
						
		#print('Finished downloading audio.')
		aud_file.close()
		aud_done = '.'

	def video_process():
		global vid_seg
		#print('')
		print('Initializing video...\n')
		
		video_init_done = ''
		vid_seg = 500
		ID_vid = str(vid_seg)
		url_vid = str(vid_src+'segment_'+ID_vid+'.m4s')
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
			vid_url = str(vid_src+'segment_'+ID_vid+'.m4s')
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
			    
		global iden
		global iden_use
		global vid_range
		vid_range = vid_seg+1
		vid_file = open('video.mp4','ab')
		#iden = 0
		for iden in range(vid_seg):
			ID = str(iden)
			vid_url = vid_src+'segment_'+ID+'.m4s'
			while len(ID)<len(str(vid_seg)):
				ID = '0'+ID
			vidoutfilename = 'vid_seg_'+ID+'.m4s'
			
			while True:
				try:
					urllib.request.urlretrieve(str(vid_url), vidoutfilename)
				except Exception:
					pass
				else:
					break
			invidsegfile = open(str('vid_seg_'+ID+'.m4s'),'rb')
			vid_file.write(invidsegfile.read())
			invidsegfile.close()
			os.remove(vidoutfilename)
			iden_use = iden+1

		global vid_done
		vid_file.close()
		vid_done = '.'
		#print('Finished downloading video.')
	
	aud_src = src+'/audio/'+aud_q+'/dash/'
	vid_src = src+'/video/'+vid_q+'/dash/'
	
	audio_file = open('audio.mp4','wb')
	video_file = open('video.mp4','wb')
	
	download(str(aud_src)+'init.mp4',out='aud_init.mp4',bar='')
	download((vid_src)+'init.mp4',out='vid_init.mp4',bar='')
	
	audio_init_file = open('aud_init.mp4','rb')
	video_init_file = open('vid_init.mp4','rb')
	
	audio_file.write(audio_init_file.read())
	video_file.write(video_init_file.read())
	
	audio_file.close()
	video_file.close()
	
	try:
		os.remove('aud_init.mp4')
		os.remove('vid_init.mp4')
	except Exception:
		pass
	
	#os.system('cat aud_init.mp4 > audio.mp4')
	#os.system('rm -f aud_init.mp4')
	#os.system('cat vid_init.mp4 > video.mp4')
	#os.system('rm -f vid_init.mp4')

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

			while True:
				try:
					seg_id_use
					iden_use
				except Exception:
					pass
				else:
					break
			tdone = seg_id_use+iden_use
			
			while tdone<tot:
				tdone = seg_id_use+iden_use
				percentage = int((tdone/tot)*100)
				pc_val = str(percentage)+'% ('+str(tdone)+' of '+str(tot)+')'
				percent.update(pc_val)
				total_pb.update_bar(percentage)
			break
			
