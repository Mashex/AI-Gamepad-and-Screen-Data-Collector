from getControllerData import *
from screenCollector import FrameGrabber
import os
import numpy as np
import cv2
import time 

location = "images/"
if os.path.exists(location) == False:
	os.mkdir(location)



d = FrameGrabber()

keys = np.array(['HX', 'HY', 'A0', 'A1', 'A2', 'A3', 'N', 'E', 'S', 'W', 'THL', 'THR', 'TL', 'TR', 'TL2', 'TR3', 'M' ,'ST', 'SL'])

def loop_translate(keys, outputs):
	new_a = map(outputs.get, keys)
	return new_a

def get_events():
	try:
		"""Process all events forever."""
		jstest = JSTest()
		while 1:
			jstest.process_events()
	except KeyboardInterrupt:
		exit()

def get_controls():
	global outputs
	try:
		i = 0
		while 1:
			#time.sleep(0.016)
			frame = np.array(d.get_processed_frame())
			controllerOutput = np.array(list(loop_translate(keys, outputs)))

			np.savez(location+"frame-{}.npz".format(i), a = frame, b = controllerOutput)

			print (i, controllerOutput)	
			i+=1
	except KeyboardInterrupt:
		exit()



x = threading.Thread(target=get_events)
x.start()			

y = threading.Thread(target=get_controls)
y.start()
#get_controls()
