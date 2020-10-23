from ffmpy import FFmpeg
import os
import shutil
import threading

def merge(down,name,window):
	while True:
		if down.is_alive():
			pass
		else:
			print('Procesing - merging audio and video.')

			ff = FFmpeg(
			inputs={'video.mp4': None, 'audio.mp4': None},
			outputs={'../../'+name+'.mp4': '-c:v copy -c:a aac -y -loglevel quiet'}
			)

			ff.run()
			os.chdir('../..')
			shutil.rmtree(name)
			print('Finished downloading '+name+', You can now go ahead and download more or close the program.')
			print('')
			print('')
			print('Enjoy!')
			print('')
			print('Thanks for using my software.')
			window.FindElement('Start').Update(disabled=False)
			break
