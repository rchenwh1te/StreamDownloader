import PySimpleGUI as sg 

def browse():
	layout = [[sg.Text('List of InBuilt Themes')], 
			[sg.Text('Please Choose a Theme to see Demo window')], 
			[sg.Listbox(values = sg.theme_list(), 
						size =(20, 12), 
						key ='-LIST-', 
						enable_events = True)], 
			[sg.Button('Exit')]] 

	themeWindow = sg.Window('Theme List', layout) 
	global theme
	while True: 
		tevent, tvalues = themeWindow.read() 
		
		if tevent in (None, 'Exit'): 
			break
		
		theme = tvalues['-LIST-'][0]
			
		sg.theme(theme) 
		sg.popup_get_text('This is {}'.format(theme)) 
		
	# Close 
	themeWindow.close() 

