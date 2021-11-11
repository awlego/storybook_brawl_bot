import cv2


class BackgroundSubtractor:
    def __init__(self):
        pass

    def find_background(self, frame):
        backSub = cv2.createBackgroundSubtractorMOG2()

        fgMask = backSub.apply(frame)
        
        # cv2.rectangle(frame, (10, 2), (100,20), (255,255,255), -1)
        # # cv2.putText(frame, str(capture.get(cv2.CAP_PROP_POS_FRAMES)), (15, 15),
        # #         cv2.FONT_HERSHEY_SIMPLEX, 0.5 , (0,0,0))
        
        
        cv2.imshow('Frame', frame)
        cv2.imshow('FG Mask', fgMask)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def subtract(self, frame, background):
        return cv2.subtract(frame, background)


def test():
    bg_subtractor = BackgroundSubtractor()
    frame = cv2.imread('C:/Users/awlego/Documents/Repositories/brawl_bot/images/characters/Card_art_-_B-a-a-d_Billy_Gruff.png', cv2.IMREAD_COLOR)
    # cv2.imshow('frame', frame)
    # cv2.waitKey(0)

    bg_subtractor.find_background(frame)


    foreground = bg_subtractor.subtract(frame, bg_subtractor.find_background(frame))
    cv2.imshow('foreground', foreground)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    test()