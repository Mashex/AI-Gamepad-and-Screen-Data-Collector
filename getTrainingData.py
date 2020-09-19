from getControllerData import *
from screenCollector import FrameGrabber
import os, glob
import numpy as np
import cv2
import time 
import keyboard


location = "images/"
if os.path.exists(location) == False:
	os.mkdir(location)



cap = FrameGrabber()

keys = np.array(['HX', 'HY', 'A0', 'A1', 'A2', 'A3', 'N', 'E', 'S', 'W', 'THL', 'THR', 'TL', 'TR', 'TL2', 'TR3', 'M' ,'ST', 'SL'])


def loop_translate(keys, outputs):
	new_a = map(outputs.get, keys)
	return new_a

def get_events(delay, run_event):

	"""Process all events forever."""
	jstest = JSTest()
	while run_event.is_set():
		time.sleep(delay)
		jstest.process_events()


def get_controls(delay, run_event): 
	global outputs, cap

	list_of_files = glob.glob('images/*.npz')
	latest_file = max(list_of_files, key=os.path.getctime)
	last_number = latest_file.split('.npz')[0].split('frame-')[1]
	i = int(last_number)
	print ("Process Start from frame: ", i)
	while run_event.is_set():
		time.sleep(delay)
		try:
			frame = np.array(cap.get_processed_frame())
			controllerOutput = np.array(list(loop_translate(keys, outputs)))

			np.savez(location+"frame-{}.npz".format(i), a = frame, b = controllerOutput)

			if i%500==0:
				print (i)	
			i+=1
		except KeyboardInterrupt:
			del cap


def main():

	print ("Waiting for Key Press of ` ")
	keyboard.wait('`') 
	print ("Process Started")

	run_event = threading.Event()
	run_event.set()

	d1 = 0.005
	x = threading.Thread(target=get_events, args = (d1, run_event))
				

	d2 = 0.016
	y = threading.Thread(target=get_controls, args = (d2, run_event))
	
	x.start()
	time.sleep(.5)
	y.start()

	try:
		while 1:
			time.sleep(.1)
	except KeyboardInterrupt:
		print ("attempting to close threads. Max wait =",max(d1,d2))
		run_event.clear()
		x.join()
		y.join()
		print ("threads successfully closed")

		# Ctrl + C or Ctrl + Pause(Break) to end process

if __name__ == '__main__':
    main()