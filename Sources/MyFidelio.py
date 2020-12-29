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
from . import Merge
		
def Silent(audio_seg, video_seg, src, aud_q, vid_q, total_pb, percent,name,window):
	def audio_process(aud_seg):
		aud_file = open('audio.mp4','ab')
		aud_seg = int(aud_seg)
		global seg_id_use
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

			os.remove(aud_outfilename)
						
		aud_file.close()
		aud_done = '.'

	def video_process(vid_seg):
		vid_seg = int(vid_seg)
		vid_range = vid_seg+1
		vid_file = open('video.mp4','ab')
		global iden_use
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
	
	print('')
	print('Initializing, this may take a while.')
	
	print(audio_seg)

	threading.Thread(target=audio_process,args=(int(audio_seg),)).start()
	threading.Thread(target=video_process,args=(int(video_seg),)).start()

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
			vseg = int(audio_seg) #+1
			aseg = int(video_seg) #+1
		except Exception:
			pass
		else:
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
					print('Starting download')
					tdone = seg_id_use+iden_use
					
					while tdone<tot:
						tdone = seg_id_use+iden_use
						percentage = int((tdone/tot)*100)
						pc_val = str(percentage)+'% ('+str(tdone)+' of '+str(tot)+')'
						percent.update(pc_val)
						total_pb.update_bar(percentage)
					break
			break
	Merge.merge(name,window)
