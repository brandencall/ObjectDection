import cv2 as cv
import numpy as np
from time import time
from webwindowcapture import WindowCapture
from vision import Vision

# Bookmark for FPS
loop_time = time()

wincap = WindowCapture('T-Rex Game – Google Dino Run - Google Chrome')
vision_player = Vision('DinoRunPlayer.png')


while(True):

    screenshot = wincap.get_screenshot()

    vision_player.find(screenshot, 0.52, 'rectangles')

    # finding the FPS of our loop
    print('FPS {}'.format(1 / (time() - loop_time)))
    # Bookmark for FPS
    loop_time = time()

    if(cv.waitKey(1) == ord('q')):
        cv.destroyAllWindows()
        break


print('Done')
