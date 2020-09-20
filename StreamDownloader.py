import PySimpleGUI as sg
import json
import Sources
import os
import ffmpeg
from ffmpy import FFmpeg
import threading
import time
import shutil

jsondb = open('list.json')
data = json.load(jsondb)
keys = data.keys()
headers = []
aud_quality = {
	'128 kbps':'1_stereo_128000',
	'360 kbps':'1_stereo_360000',
	'640 kbps':'1_stereo_640000'
	}
aud_quality_man = ['128 kbps','360 kbps','640 kbps']
vid_quality = {	
	'144p (190 kbps)':'144_190464',
	'288p (381 kbps)':'288_380928',
	'360p (688 kbps)':'360_688128',
	'432p (1098 kbps)':'432_1097728',
	'576p (1405 kbps)':'576_1404928',
	'HD 720p (2288 kbps)':'720_2287616',
	'Full HD 1080p (3113 kbps)':'1080_3112960'
	}
vid_quality_man = ['144p (190 kbps)','288p (381 kbps)','360p (688 kbps)','432p (1098 kbps)','576p (1405 kbps)','HD 720p (2288 kbps)','Full HD 1080p (3113 kbps)']
for key in sorted(keys):
	headers.append(key)

layout = [  [sg.Text('Opera name:'),sg.Text('		         Audio resolution:'),sg.Text('Video resolution:')],
            [sg.Combo(headers,size=(30,1),key = 'st_name'), sg.Combo(aud_quality_man,size=(10,1),key='aud_quality'), sg.Text(' '), sg.Combo(vid_quality_man,size=(20,1),key='vid_quality')],
            [sg.Output(size=(80,20))],
            [sg.Text('Progress:'),sg.Text('0% (0 of 0)	   ',key='progress_percent'),sg.ProgressBar(100,orientation='h',size=(30,20), bar_color=('chartreuse2','white'), key='Progress')],
            [sg.Button('Start'), sg.Button('Close')] ]
            
window = sg.Window('Stream Downloader',layout)
total_pb = window['Progress']
pc = window['progress_percent']


while True:
	global event,values
	event,values = window.read()
	if event == 'Close' or event == sg.WIN_CLOSED:
		break
	elif event == 'Start':
		if os.path.exists('Download'):
			pass
		else:

			os.mkdir('Download')
		os.chdir('Download')
		name = values['st_name']
		
		try:
			os.mkdir(name)
			#shutil.rmtree('temp')
		except Exception:
			pass
		
		os.chdir(name)
		shutil.rmtree('./temp', ignore_errors=True)
		os.mkdir('temp')
		os.chdir('temp')
		audq = aud_quality.get(values['aud_quality'])
		vidq = vid_quality.get(values['vid_quality'])
		src = data.get(name)
		Sources.MyFidelio.Silent(src,audq,vidq,total_pb,pc)
		print('Procesing - merging audio and video.')
		vid_in = ffmpeg.input('./video.mp4')
		aud_in = ffmpeg.input('./audio.mp4')
		ff = FFmpeg(
		inputs={'video.mp4': None, 'audio.mp4': None},
		outputs={'../'+name+'.mp4': '-c:v copy -c:a aac -loglevel quiet'}
		)

		ff.run()
		os.chdir('..')
		shutil.rmtree('temp')
		os.chdir('../..')
		print('Finished downloading '+name+''', You can now go ahead and download more or close the program.
		Enjoy!
		Thanks for using my software.''')
