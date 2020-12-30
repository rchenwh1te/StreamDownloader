import PySimpleGUI as sg
import os
import ffmpeg
from ffmpy import FFmpeg
import threading
import time
import shutil
import sys
import sqlite3
import Sources
import time

path = os.path.abspath(os.path.join(__file__,os.pardir))
path = os.path.abspath(os.path.join(path,os.pardir))
#print(path)
dbdir = os.path.dirname(os.path.abspath(__file__))

ico = b'''iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAQAAAC1+jfqAAAABGdBTUEAALGPC
/xhBQAAACBjSFJNAAB6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAAAAmJL
R0QAAKqNIzIAAAAHdElNRQfkCxgOAgCb1PLdAAAA40lEQVQoz6XQvUoDARAE4O/yo4hViIW
VPoDYCSlELCy0sbK0FBF8A7HyLaxtFDvJMwh2msZKbEIEUUIQOczPZS2iyQXsnGJhd2ZnluW
/KE51iapNFe+yv8SJXU2pTweTYWlMFqy6NK+vbFlBQSbyUcfehNDSVld3a0uStz8TQldHCKn
QNEfhRxAewZ1X0MKC2bzDjTCw40no6gr3yiNyxoaattCwpC8MhNT67/aentRQZtuJEK6dWxv
HOzI0lLmyryP01KY/+awic+HUoRVFHQ8ak+NGtSiTWFT1peTFR/5J/8M3IJ5LdWJ9WE8AAAA
ldEVYdGRhdGU6Y3JlYXRlADIwMjAtMTEtMjRUMTM6NTY6NDMrMDA6MDBXOkR2AAAAJXRFWHR
kYXRlOm1vZGlmeQAyMDIwLTExLTI0VDEzOjU2OjQzKzAwOjAwJmf8ygAAACB0RVh0c29mdHd
hcmUAaHR0cHM6Ly9pbWFnZW1hZ2ljay5vcme8zx2dAAAAGHRFWHRUaHVtYjo6RG9jdW1lbnQ
6OlBhZ2VzADY5my6MAAAAF3RFWHRUaHVtYjo6SW1hZ2U6OkhlaWdodAAyMjHvybUAAAAWdEV
YdFRodW1iOjpJbWFnZTo6V2lkdGgAMjLJQAk4AAAAGXRFWHRUaHVtYjo6TWltZXR5cGUAaW1
hZ2UvaWNvlzA4zgAAABd0RVh0VGh1bWI6Ok1UaW1lADE2MDYyMjYyMDPpMWI6AAAAE3RFWHR
UaHVtYjo6U2l6ZQAxMjQ4NkJCbGg3fQAAACB0RVh0VGh1bWI6OlVSSQBmaWxlOi8vbWVkaWE
vaWNvbi5pY29HhGrQAAAAAElFTkSuQmCC'''

search_ico = b'''
iVBORw0KGgoAAAANSUhEUgAAABYAAAAWCAYAAADEtGw7AAAABmJLR0QA/wD/AP+gvaeTAAADWElE
QVQ4ja3VT0gjVwAG8G8y2kwgbcnin6YnYSE9KNuCB1FUot5UvAQR9lA8tIGFeAgVerLsRUhY4iEH
zSHYYE4GJCiWpEk8iBEkXmrj3rK5hKyUmhkwThKZJF8PGslWp7vb9oO5zDx+M+97M2+A90cE0PEB
496JoHP+id/vnx0aGprs7u7+QhAEQ6lU+vP8/Dy9vLy8e3l5+fZjb9Th8XieK4ryO3WiquqbYDDo
AmD8YDQcDv/YbDYrJKlpGhOJBL1eL1dXV7m7u8tKpdLy6/F43AdAeq/q8Xiet9B0Ok2bzUYA7xxW
q5XRaLSFN7a2tn6Afp0AgCeyLP9GksfHx5QkiaIo0uVy8eDggIeHh1xZWaHJZKIgCIxEIiTJWq12
MTIy8lRX9fv937amb7PZKIoik8nkg36z2SzNZjMtFgtlWSZJRqPRl7pwJpMJkWQikSAALi0tkSSb
zWb19PR06+joKFCv1xWSXFtbIwAGAgGSZD6f/xVA52OumMvl4iTp9XoJgKlUiiSZyWRCuH2Hhf39
/dU7iADodDpJkoqinAH47O+oAYAgiqIAAI1GAwDQ2Xn7ADc3NzUADQCs1WqV9muapgEABEEw4JEF
7ABQL5VKl319fejv7wcApFIpjI+PY3h4eGFvb69UrVbV2dnZFwCQTCYBAAMDAwCAcrn8B4Dqox2H
QqEXJFmpVGi1WmkymZjNZh8s3sXFBXt6eihJEovFIkkyFou90lk6oKur60tVVd/crTINBgPNZjN9
Ph/z+TwLhQI3NzfZ29tLAHS73dQ0rdXx64WFha918WAw6CJZJ8nt7W1aLJYHH4gkSXS73QRAu93O
6+vre9zhcDzTs42JRMJHskGSsiwzEAjQ6XRycXGRPp+PxWKRmqbRbrff46qq8m78P+JSOBxertVq
b/U2obuNiJOTkwTA0dFRlsvle3x6etqmhwuDg4NPd3Z2Xubz+biiKGdXV1fZQqFwEIvFXimK8rqF
T01NEQDHxsbu8ZOTk03dvtvSCeBTAJ8D+AQA5ufnv2nHJyYmaDQamU6nSZK5XO4X3P4cPj4Oh+NZ
O95CSWrr6+vf/Su0lZmZmQFZls/aqtcikchPrZn9p8zNzX2VyWR+zuVysY2Nje//F7QtAh7p9C/9
rL8WVoiW3gAAAABJRU5ErkJggg==
'''

sg.theme('SystemDefaultForReal')
dbpath = path+'/media/database.db'
#file_list = os.listdir(path)
#print(file_list)
#print(dbpath)
#f = open(dbpath,'rb')
#print(f.read())
db = sqlite3.connect(dbpath)
sql = db.cursor()

sql.execute('SELECT * FROM myfidelio')

result = sql.fetchall()
data = [list(i) for i in result]

keys = []
things = []

for i in data:
        keys.append(i[0])
        things.append(i[1])

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

resultsFrame = [ [sg.Button('',key='res0',visible=False)],
                 [sg.Button('',key='res1',visible=False)],
                 [sg.Button('',key='res2',visible=False)],
                 [sg.Button('',key='res3',visible=False)],
                 [sg.Button('',key='res4',visible=False)],
                 [sg.Button('',key='res5',visible=False)],
                 [sg.Button('',key='res6',visible=False)],
                 [sg.Button('',key='res7',visible=False)],
                 [sg.Button('',key='res8',visible=False)],
                 [sg.Button('',key='res9',visible=False)],
                 [sg.Button('Next >>',visible=True)]]


sFrame = [[sg.In(size=(20,5),key='searchVal'),sg.Button(key='Search',image_data=search_ico)]]
sCol = [[sg.Frame('Search',sFrame)],[sg.Frame('Search results',resultsFrame,key='resframe',size=(80,10))],]
column0 = [[sg.Text('Opera name:')],[sg.Combo(keys,size=(30,1),key='st_name')]]
column1 = [[sg.Text('Audio resolution:')],[sg.Combo(aud_quality_man,size=(10,1),key='aud_quality')]]
column2 = [[sg.Text('Video resolution:')],[sg.Combo(vid_quality_man,size=(20,1),key='vid_quality')]]

headerCol = [
            [sg.Column(column0),sg.Column(column1),sg.Column(column2)],
            [sg.Text('Select download location:'),sg.In(key='save_path'),sg.FolderBrowse()]]
mainCol = [[sg.Column(headerCol)],
           [sg.Output(size=(80,20))]
           ]

footer1 = [[sg.Text('Progress:'),sg.Text('0% (0 of 0)',key='progress_percent')]]
footer2 = [[sg.ProgressBar(100,orientation='h',size=(30,20) , key='Progress'),sg.T('Elapsed: '),sg.T('--:--:--      ',key='elapsed'),sg.T('Remaining:'),sg.T(' --:--:--      ',key='estimated')]]
#bar_color=('chartreuse2','white')

layout = [  [sg.Column(mainCol),sg.Column(sCol,justification='right')],
            [sg.Column(footer1),sg.Column(footer2)],
            [sg.Button('Start'), sg.Button('Close')] ]

#window = sg.Window('Stream Downloader',layout,icon=ico)

#window.Finalize()

def start(name,window,total_pb,pc):
        if name == '':
                while True:
                        global event,values
                        event,values = window.read()
                        if event == 'Close' or event == sg.WIN_CLOSED:
                                try:
                                        sys.exit()
                                except SystemExit:
                                        os._exit(0)
                                break
                        elif event == 'Start':
                                window['Start'].Update(disabled=True)
                                path = values['save_path']
                                if path == '':
                                        if os.path.exists('Download'):
                                                pass
                                        else:

                                                os.mkdir('Download')
                                        path = './Download'
                                else:
                                        os.chdir(path)
                                
                                name = values['st_name']
                                
                                try:
                                        os.mkdir(name)
                                        
                                except Exception:
                                        pass
                                
                                os.chdir(name)
                                shutil.rmtree('./temp', ignore_errors=True)
                                os.mkdir('temp')
                                os.chdir('temp')
                                audq = aud_quality.get(values['aud_quality'])
                                vidq = vid_quality.get(values['vid_quality'])

                                sql.execute('SELECT * FROM myfidelio WHERE name="'+name+'"')
                                source = sql.fetchall()
                                source = [list(i) for i in source]
                                
                                src,aud_seg,vid_seg = source[0][1],source[0][2],source[0][3]
                                
                                stime = time.time()
                                print(stime)

                                down = threading.Thread(target=Sources.MyFidelio.Silent,args=(aud_seg,vid_seg,src,audq,vidq,total_pb,pc,name,window,stime,values,))
                                down.start()
                                #threading.Thread(target=Sources.Merge.merge,args=(down,name,window),daemon=True).start()
                                
        else:
                event,values = window.read()

                window['Start'].Update(disabled=True)
                path = values['save_path']
                if path == '':
                        if os.path.exists('Download'):
                                pass
                        else:

                                os.mkdir('Download')
                        path = './Download'
                else:
                        os.chdir(path)
                
                
                try:
                        os.mkdir(name)
                        
                except Exception:
                        pass
                
                os.chdir(name)
                shutil.rmtree('./temp', ignore_errors=True)
                os.mkdir('temp')
                os.chdir('temp')
                audq = aud_quality.get(aud_quality_man[-1])
                vidq = vid_quality.get(vid_quality_man[-1])

                sql.execute('SELECT * FROM myfidelio WHERE name="'+name+'"')
                source = sql.fetchall()
                source = [list(i) for i in source]
                
                src = source[0][1]
                aud_seg = source[0][2]
                vid_seg = source[0][3]
                stime = time.time()
                print(stime)
                
                down = threading.Thread(target=Sources.MyFidelio.Silent,args=(aud_seg,vid_seg,src,audq,vidq,total_pb,pc,name,window,stime,values),daemon=True)
                down.start()
                #threading.Thread(target=Sources.Merge.merge,args=(down,name,window),daemon=True).start()
                        
                        
def Search(val):
        sql.execute("SELECT * FROM myfidelio WHERE name LIKE '%"+val+"%';")
        result = sql.fetchall()
        resultlist = []
        for i in result:
                n,_,_,_ = i
                resultlist.append(n)
                
        if resultlist != None:
                resCol = []
                for i in resultlist:
                        resCol.append([sg.Button(i)])
        else:
                resultlist = ['No results found.']
                
        return resultlist
