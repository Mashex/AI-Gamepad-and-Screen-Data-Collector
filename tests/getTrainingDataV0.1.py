from inputControls import JoyControls
from screenCollector import FrameGrabber
import os
import numpy as np
import cv2
location = "images/"
if os.path.exists(location) == False:
    os.mkdir(location)

d = FrameGrabber()
controls = JoyControls()

i = 0
#start = time.time()
try:
    while cv2.waitKey(7) % 0x100 != 10:
        i+=1
        frame = np.array(d.get_processed_frame())
        controllerOutput = controls.getInputs()

        #frameReshape = frame.reshape(-1)

        if controllerOutput.shape[0] == 22:
            #arr = frameReshape.append(controllerOutput)

            #print (arr.shape, frame.shape, controllerOutput.shape)
            #(91583,) (131, 233, 3) (14,)
            #Frame shape: (131, 233, 3) = 91569
            print (controllerOutput)
            np.savez(location+"frame-{}.npz".format(i), a = frame, b = controllerOutput)

        #print (controllerOutput)
        #print (frame.shape, controllerOutput.shape, data.shape)
        #exit()
except KeyboardInterrupt:
    print("Press Ctrl-C to terminate while statement")
    del d
    del controls
