import PySimpleGUI as sg
import sqlite3
import os

#path = os.path.abspath(os.path.join(os.path.abspath(__file__),os.pardir))
#path = os.path.abspath(os.path.join(path,os.pardir))
#####path = os.path.abspath(os.path.join(path,os.pardir))
#print(path)
conn = sqlite3.connect('/usr/share/StreamDownloader/media/database.db')
sql = conn.cursor()

sql.execute('''SELECT count(name) FROM sqlite_master WHERE type='table' AND name='settings' ''')

if sql.fetchone()[0] == 1:
	sql.execute('''SELECT * FROM settings''')
	settings = sql.fetchall()
	settings = [list(i) for i in settings]
	for i in settings:
		defdir,deftheme = i
		
else:
	sql.execute('''CREATE TABLE settings(defdir TEXT,deftheme TEXT)''')
	sql.execute('''INSERT INTO settings(defdir,deftheme) values ('./Download','SystemDefaultForReal')''')
	conn.commit()
	sql.execute('''SELECT * FROM settings''')
	settings = list(sql.fetchall())
	for i in settings:
		defdir,deftheme = i

conn.close()

sg.theme(deftheme)

settab_textcol = [[sg.Text('Default download location:')],
[sg.Text('Theme:')]]
settab_incol = [[sg.In(key='defdir'),sg.FolderBrowse()],
[sg.In(key='deftheme'),sg.Button('Browse themes')]]
final = [[sg.Column(settab_textcol),sg.Column(settab_incol)],[sg.B('Apply settings')]]


def apply(#path=path,
defdir='./Download',deftheme='SystemDefaultForReal'):
	conn = sqlite3.connect('/usr/share/StreamDownloader/media/database.db')
	sql = conn.cursor()
	sql.execute('DROP TABLE settings')
	sql.execute('''CREATE TABLE settings(defdir TEXT,deftheme TEXT)''')
	sql.execute('INSERT INTO settings(defdir,deftheme) values ("{}","{}")'.format(defdir,deftheme))
	conn.commit()
	conn.close()
