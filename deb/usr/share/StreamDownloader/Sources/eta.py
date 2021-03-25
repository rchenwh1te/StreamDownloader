import time
import datetime

previous = int()

def calculate(s,p,pr,ll,timee,window,tot=100):
	ts = time.mktime(time.strptime(timee, "%H:%M:%S"))
	sp = list(timee.split(':'))
	e = time.time()
	e -= s
	
	if pr != p:
		try:
			tpp = e/p
		except Exception as ex:
			#print(ex)
			tpp = 0
		left = tot-p
		ela = tpp*left
		pr = p

		val = time.strftime('%H:%M:%S',time.gmtime(ela))
		est = val
	else:
		time.sleep(1)
		#temp = ts + 1.0
		#print(ts,temp)
		#est = time.strftime('%H:%M:%S',time.gmtime(temp))
		secs = int(sp[2])
		mins = int(sp[1])
		hrs = int(sp[0])
		secs -= 1
		if secs == 0 and mins > 0:
			mins -= 1
		elif secs == 0 and hrs > 0:
			mins = 59
		if mins == 0 and hrs > 0:
			hrs -=1
		if secs == -1:
			secs = 59
		if mins == -1:
			mins = 59
		
		hr = str(abs(hrs))
		mi = str(abs(mins))
		se = str(abs(secs))
		
		while len(hr) < 2:
			hr = '0'+hr
		while len(mi) < 2:
			mi = '0'+mi
		while len(se) < 2:
			se = '0'+se	
		
		est = f'{hr}:{mi}:{se}'
		ela = 0
			
	window['estimated'].update(est)	
	return est,pr,ela
