import cv2
import numpy as np
import os
from time import time
from window_capture import WindowCapture, WindowCapture2
import win32gui, win32ui, win32con


USE_SCREENSHOT = True

def black_white_filter(image, threshold):
    """Turns an image to only fully black and fully white pixels.
    """
    # convert the image to grayscale
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # apply threshold
    image = cv2.threshold(image, threshold, 255, cv2.THRESH_BINARY)[1]

    return image



def find_characters(screenshot, image_to_find, threshold=0.5):
    """Finds the location of the image inside the screenshot"""

    if threshold > 1:
        threshold = threshold / 100

    # # crop to the center of the image, since the frame hides some of the image:
    # image_to_find = image_to_find[200:400, 200:400]

    # find the location of the image inside the screenshot
    # for method in [cv2.TM_CCOEFF, cv2.TM_CCOEFF_NORMED, cv2.TM_CCORR, cv2.TM_CCORR_NORMED, cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]

    res = cv2.matchTemplate(screenshot, image_to_find, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= threshold)

    # print(loc)

    # draw a rectangle around the image
    for pt in zip(*loc[::-1]):
        cv2.rectangle(screenshot, pt, (pt[0] + image_to_find.shape[1], pt[1] + image_to_find.shape[0]), (0, 0, 255), 1)

    return screenshot


def rotate_image(img):
    """Rotates an image 90 degrees clockwise"""
    return np.rot90(img)


def gaussian_blur(img, kernel_size):
    """Blurs an image with a gaussian kernel"""
    return cv2.GaussianBlur(img, (kernel_size, kernel_size), 0)


# def slider():
#     cv2.namedWindow('image')
#     threshold = 100 
#     img = cv2.imread('C:/Users/awlego/Documents/Repositories/brawl_bot/images/characters/Card_art_-_B-a-a-d_Billy_Gruff_tiny.png')
#     cv2.createTrackbar('threshold', 'image', 0, 255, black_white_filter)
#     while(1):
#         img = cv2.imread('C:/Users/awlego/Documents/Repositories/brawl_bot/images/characters/Card_art_-_B-a-a-d_Billy_Gruff_tiny.png')
#         threshold = cv2.getTrackbarPos('threshold', 'image')
#         img = black_white_filter(img, threshold)
#         cv2.imshow('image', img)
#         k = cv2.waitKey(1) & 0xFF
#         if k == 27:
#             break
#     cv2.destroyAllWindows()


def noise_alpha(img):
    """Adds noise to the RGB channels if the alpha is 0"""
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if img[i, j, 3] == 0:
                img[i, j, 0] = np.random.randint(0, 255)
                img[i, j, 1] = np.random.randint(0, 255)
                img[i, j, 2] = np.random.randint(0, 255)
    return img



def print_cursor_location():
    """Prints the pixel location of the cursor"""
    print(win32gui.GetCursorPos())


def main():
    cv2.namedWindow('Computer Vision')
    wincap = WindowCapture2('Storybook Brawl')

    if USE_SCREENSHOT:
        screenshot = cv2.imread("C:/Users/awlego/Documents/Repositories/brawl_bot/images/example_boards/billy_test.png")
        screenshot = cv2.resize(screenshot, (3072, 1728)) # Resize image to my scaled display
        # screenshot = black_white_filter(screenshot, 100)

    cv2.namedWindow('Sliders')
    cv2.createTrackbar('threshold', 'Sliders', 0, 255, lambda x: x)
    cv2.createTrackbar('find_characters_threshold', 'Sliders', 100, 100, lambda x: x)
    cv2.createTrackbar('find_image_scale', 'Sliders', 100, 200, lambda x: x)

    example_image = cv2.imread("C:/Users/awlego/Documents/Repositories/brawl_bot/images/good_frame_partial.png",  cv2.IMREAD_UNCHANGED)
    example_image = noise_alpha(example_image)

    loop_time = time()
    while(True):

        # get an updated image of the game
        # TOOD: update to take in videos, streams, etc.
        if not USE_SCREENSHOT:
            screenshot = wincap.get_screenshot()
            screenshot = cv2.resize(screenshot, (3072, 1728)) # Resize image to my scaled display

        threshold = cv2.getTrackbarPos('threshold', 'Sliders')
        find_characters_threshold = cv2.getTrackbarPos('find_characters_threshold', 'Sliders')

        img = cv2.imread('C:/Users/awlego/Documents/Repositories/brawl_bot/images/example_boards/billy_test.png', cv2.IMREAD_UNCHANGED)
        img = cv2.resize(img, (3072, 1728)) # Resize image to my scaled display
        # img = black_white_filter(img, threshold)

        example_image = cv2.imread("C:/Users/awlego/Documents/Repositories/brawl_bot/images/good_frame_partial.png",  cv2.IMREAD_UNCHANGED)
        example_image = noise_alpha(example_image)
        example_image_scale = cv2.getTrackbarPos('find_image_scale', 'Sliders')
        example_image = cv2.resize(example_image, (int(example_image.shape[1] * example_image_scale / 100), int(example_image.shape[0] * example_image_scale / 100)))
        # example_image = black_white_filter(example_image, threshold)
        cv2.imshow('Example image', example_image)

        img = find_characters(img, example_image, find_characters_threshold)
        cv2.imshow('Storybook Brawl Tracker', img)

        print_cursor_location()


        # debug the loop rate
        print('FPS {}'.format(1 / (time() - loop_time)))
        loop_time = time()



        # press 'q' with the output window focused to exit.
        # waits 1 ms every loop to process key presses
        if cv2.waitKey(1) == ord('q'):
            cv2.destroyAllWindows()
            break

    print('Done.')


if __name__ == '__main__':
    main()