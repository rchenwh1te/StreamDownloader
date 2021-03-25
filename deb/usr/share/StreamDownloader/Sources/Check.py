import wget
from wget import *
import os
import sys
import requests
import urllib
import threading
import shutil
import sqlite3

conn = sqlite3.connect('database.db')
sql = conn.cursor()

sql.execute('SELECT * FROM MyFidelio')
result = sql.fetchall()

		
def Silent(name,src, aud_q, vid_q):
	aud_src = src+'/audio/'+aud_q+'/dash/'
	vid_src = src+'/video/'+vid_q+'/dash/'
	
	def audio_process():
		connection = sqlite3.connect('database.db')
		sqlw = connection.cursor()
		global aud_seg
		audio_init_done = ''
		
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
			#print(aud_seg)
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
						
					i += 1
			else:
				valid.append(aud_seg)
			if aud_seg < 0:
				sqlw.execute('UPDATE MyFidelio SET audio = "'+str(0)+'" WHERE name = "'+opname+'";')
				break    
		global seg_id
		global seg_id_use
		global aud_range
		aud_range = aud_seg+1
		
		print('audio'+str(aud_seg))
		sqlw.execute('UPDATE MyFidelio SET audio = "'+str(aud_seg)+'" WHERE name = "'+opname+'";')
		connection.commit()
		aud_done = '.'

	def video_process():
		conne = sqlite3.connect('database.db')
		sqli = conne.cursor()
		global vid_seg
		
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
			#print(vid_seg)
			try:
				urllib.request.urlopen(vid_url)
			except urllib.error.HTTPError as vid_exception:
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
			if vid_seg < 0:
				sqli.execute('UPDATE MyFidelio SET video = '+str(0)+' WHERE name="'+opname+'"')
				break
		global iden
		global iden_use
		global vid_range
		vid_range = vid_seg+1
		
		print('video'+str(vid_seg))
		sqli.execute('UPDATE MyFidelio SET video = '+str(vid_seg)+' WHERE name="'+opname+'"')
		conne.commit()

		global vid_done
		vid_done = '.'
	
	global opname
	opname = name
	aud_thread = threading.Thread(target=audio_process)
	aud_thread.start()
	vid_thread = threading.Thread(target=video_process)
	vid_thread.start()
	
	aud_thread.join();vid_thread.join()

for i in range(len(result)):
	#print(result[i])
	print(result[i][0]+':')
	
	if result[i][2] == '1':
		Silent(result[i][0],result[i][1],'1_stereo_128000','144_190464')
