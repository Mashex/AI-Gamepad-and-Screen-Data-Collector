import numpy as np
import cv2

for i in range(1,550):
	data = np.load(f"images//frame-{i+1}.npz")

	cv2.imshow('image', data['a'])
	cv2.waitKey(0)  
	controls = data['b']
	print (controls)
