

import cv2
import numpy as np
import os
from time import time
from window_capture import WindowCapture, WindowCapture2
import win32gui, win32ui, win32con


def main():

    cv2.namedWindow('Computer Vision')

    img = cv2.imread("C:/Users/awlego/Documents/Repositories/brawl_bot/images/characters/B-a-a-d Billy Gruff.png")

    cv2.namedWindow('Sliders')
    cv2.createTrackbar('threshold', 'Sliders', 0, 255, lambda x: x)
    cv2.createTrackbar('find_characters_threshold', 'Sliders', 0, 100, lambda x: x)

    cv2.imshow('Storybook Brawl Tracker', img)

    while True:
        # press 'q' with the output window focused to exit.
        # waits 1 ms every loop to process key presses
        if cv2.waitKey(1) == ord('q'):
            cv2.destroyAllWindows()

    print('Done.')


if __name__ == '__main__':
    main()