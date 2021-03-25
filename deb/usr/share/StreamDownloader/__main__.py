import os
import Sources
path = os.path.abspath(__file__)
#__import__(path+'/MyFidelio')
import MyFidelio
import PySimpleGUI as sg

mftab = MyFidelio.layout
settab = Sources.settings.final
group = [[sg.Tab('MyFidelio',mftab)
,sg.Tab('Settings',settab)
]]

layout = [[sg.TabGroup(group,enable_events=True,key='_GROUP_')]]

#print(layout)

window = sg.Window('StreamDownloader',layout,finalize=True,icon=MyFidelio.ico)
window['defdir'].Update(Sources.settings.defdir)
window['deftheme'].Update(Sources.settings.deftheme)
names = {'res0':'','res1':'','res2':'','res3':'','res4':'','res5':'','res6':'','res7':'','res8':'','res9':''}


total_pb = window['Progress']
pc = window['progress_percent']
p = 0
while True:
	event,values = window.read()
	
	select = window["_GROUP_"].get()
	
	closed = event == sg.WIN_CLOSED
	
	if closed or event == 'Close':
		break
	elif event == 'Start' and select == 'MyFidelio':
		MyFidelio.start('',window,total_pb,pc)
		
	elif event == 'Search' and select == 'MyFidelio':
		column = MyFidelio.Search(values['searchVal'])
		
		for i in range(10):
			try:
				window['res'+str(i)].Update(column[i],visible=True)
				names['res'+str(i)] = column[i]
			except Exception:
				window['res'+str(i)].Update(visible=False)
			
	elif event == 'Next >>' and select == 'MyFidelio':
		try:
			column[int(p*10)-1]
			
		except Exception:
			p = 0
			
		for i in range(10):
			try:
				window['res'+str(i)].Update(column[int(int(p*10))+i],visible=True)
				names['res'+str(i)] = column[int(int(p*10))+i]
				
			except Exception:
				window['res'+str(i)].Update(visible=False)
			
		p += 1
		
	elif event == 'res0' or event == 'res1' or event == 'res2' or event == 'res3' or event == 'res4' or event == 'res5' or event == 'res6' or event == 'res7' or event == 'res8' or event == 'res9':
		name = names[event]
		MyFidelio.start(name,window,total_pb,pc)
	elif event == 'Browse themes':
		Sources.themes.browse()
		window['deftheme'].Update(Sources.themes.theme)
		
	elif event == 'Apply settings':
		Sources.settings.apply(defdir=values['defdir'],deftheme=values['deftheme'])
		
	try:
		bwin = Sources.themes.bwin
		beve = Sorces.themes.beve
		if beve == sg.WIN_CLOSED:
			bwin.close()
			event,values = window.read()
	
	except Exception:
		pass
