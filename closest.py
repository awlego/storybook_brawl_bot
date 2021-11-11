import cv2
import numpy as np
import os
from time import time
from window_capture import WindowCapture, WindowCapture2
import win32gui, win32ui, win32con
from tqdm import tqdm


USE_SCREENSHOT = True

def center_crop_img(img, percentage_cut):
    """Crops the image, zooming in on the center"""
    height, width, channels = img.shape
    height_cut = int(height * percentage_cut)
    width_cut = int(width * percentage_cut)
    return img[int(height_cut/2):int(height-height_cut/2), int(width_cut/2):int(width-width_cut/2)]


def top_two_thirds_crop(img):
    """Crops the image to the top two thirds"""
    height, width, channels = img.shape
    return img[0:int(height/3), :]


def filtered(img):

    def edge_detection(img):
        img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        img = cv2.GaussianBlur(img, (5, 5), 0)
        img = cv2.Canny(img, 100, 200)
        return img

    return edge_detection(img)


def closest_match(img, img_set):
    """Finds the image in the img_set that is closest to the img"""
    closest_img = None
    closest_distance = None
    for img_name, img_i in tqdm(img_set.items()):
        img_i = center_crop_img(img_i, 0.15)
        print(img_i.shape)
        img_i = top_two_thirds_crop(img_i)
        print(img_i.shape)
        img_i = img_i[:,:,:3]
        img_i = cv2.resize(img_i, (img.shape[1], img.shape[0]))

        print(img.shape)
        filtered_img = top_two_thirds_crop(img)
        print(filtered_img.shape)
        filtered_img = filtered(filtered_img)
        print(filtered_img.shape)
        img_i = filtered(img_i)
        img_i = top_two_thirds_crop(img_i)
        distance = cv2.norm(filtered_img, img_i, cv2.NORM_L2)
        if img_name == "SBB_CHARACTER_MONSTAR.png":
            print(img_name, distance)
            cv2.imshow("demo", img_i)
            cv2.imshow("demo2", filtered_img)

        # cv2.waitKey(0)


        if closest_distance is None or distance < closest_distance:
            closest_img = img_i
            closest_distance = distance
    print(closest_distance)
    return closest_img


def get_character_list(img_folder):
    """Returns a list of images in the folder"""
    images = {}
    for filename in os.listdir(img_folder):
        if filename.startswith("SBB_CHARACTER"):
            images[filename] = cv2.imread(os.path.join(img_folder, filename), cv2.IMREAD_UNCHANGED)
    return images


def print_cursor_location():
    """Prints the pixel location of the cursor"""
    print(win32gui.GetCursorPos())


from brawl_background_locations import position_1, position_2, position_3, position_4, position_5, position_6, position_7

# def get_char(img, position):

def debug_crop():
    img_i = cv2.imread("C:/Users/awlego/Documents/Repositories/brawl_bot/images/exported_assets/Texture2D/SBB_CHARACTER_MONSTAR.png")
    # img_i = img_i[:,:,:3]
    print(img_i.shape)
    img_i = center_crop_img(img_i, 0.1)
    print(img_i.shape)
    cv2.imshow("monstar", img_i)


def main():
    cv2.namedWindow('Computer Vision')
    wincap = WindowCapture2('Storybook Brawl')

    if USE_SCREENSHOT:
        img = cv2.imread("C:/Users/awlego/Documents/Repositories/brawl_bot/images/example_boards/billy_test.png")
        img = cv2.resize(img, (3072, 1728)) # Resize image to my scaled display

    pos1 = position_1()
    cutout = pos1.get(img)
    match = closest_match(cutout, get_character_list("C:/Users/awlego/Documents/Repositories/brawl_bot/images/exported_assets/Texture2D"))

    cv2.imshow("img", img)
    cv2.imshow("cutout", cutout)
    cv2.imshow("match", match)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()