import numpy as np
import cv2

for i in range(2000,4000):
	data = np.load(f"images//frame-{i+1}.npz")
	img = cv2.cvtColor(data['a'], cv2.COLOR_BGR2RGB)
	cv2.imshow('image', img )
	cv2.waitKey(0)  
	controls = data['b']
	print (controls)




















