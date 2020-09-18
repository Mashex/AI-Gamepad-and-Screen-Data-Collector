import pygame
import time

import numpy as np

class JoyControls:
    def __init__(self):

        pygame.init()

        # Set the width and height of the screen (width, height).
        screen = pygame.display.set_mode((1, 1))

        #pygame.display.set_caption("My Game")

        # Loop until the user clicks the close button.
        done = False

        # Used to manage how fast the screen updates.
        clock = pygame.time.Clock()

        # Initialize the joysticks.
        pygame.joystick.init()



        i=0

        self.joystick = pygame.joystick.Joystick(i)
        self.joystick.init()

        self.name = self.joystick.get_name()
        self.axes = self.joystick.get_numaxes()
        self.buttons = self.joystick.get_numbuttons()
        self.hats = self.joystick.get_numhats()

        
    def getInputs(self):

            self.inputs = np.zeros(shape = (22,))

            # while not done:
            #     start = time.time()
            for event in pygame.event.get(): # User did something.
                if event.type == pygame.QUIT: # If user clicked close.
                    done = True # Flag that we are done so we exit this loop.
                # elif event.type == pygame.JOYBUTTONDOWN:
                #     print("Joystick button pressed.")
                # elif event.type == pygame.JOYBUTTONUP:
                #     print("Joystick button released.")

            for i in range(self.axes):
                self.axis = self.joystick.get_axis(i)
                self.inputs[i] = self.axis
                
            i = i+1
            for j in range(self.buttons):
                self.button = self.joystick.get_button(j)
                self.inputs[i+j] = self.button

            # for k in range(self.hats):
            #     self.hat = self.joystick.get_hat(k)

            #     print (self.hat)


            #     self.inputs[i+j+k] = self.hat

            #     print (i+j+k+1)

                #print("Hat {} value: {}".format(i, str(hat)))

            return (self.inputs)


            # Limit to 60 frames per second.
            #clock.tick(60)
            #print (time.time() - start)

    def __del__(self):
        pygame.quit()
        print("Pygame stopped")



controls = JoyControls()
print (controls.getInputs())