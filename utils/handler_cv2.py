import random
from datetime import datetime

import cv2 as cv
import numpy as np

from utils import global_utils
from utils.handler_adb import HandlerAdb


# ToDo:
#   - Take capture only when needed (after tap, swipe, sleep, ...) -> SPEED


class HandlerCv2:
    def __init__(self, adb: HandlerAdb):
        self.adb = adb
        self.find_start = None
        self.find_end = None
        self.imread = cv.IMREAD_COLOR
        self.method = cv.TM_CCOEFF_NORMED
        self.show_debug_image = False
        self.target_image = None
        self.target_image_debug = None
        self.threshold = 0.9

    def check_match(self, data_image):
        """
            Take capture & check if image match
            return true / false
            Coords can be accessed with find_start / find_end or directly tap with tap_find
        """
        self.get_image()
        return self.match(data_image)

    def check_match_multiple(self, find_image):
        """
            Take capture & check if image match
            return true / false
            Coords can be accessed with find_start / find_end
        """
        self.get_image()
        return self.match_multiple(find_image)

    def dev(self):
        """
            Run dev mode, showing the capture
        """
        global_utils.debug("dev > s to save, q to quit")
        while True:
            self.adb.require_new_capture = True
            self.get_image()  # Get image directly from ADB
            cv.imshow("dev", self.target_image)  # Show image in window
            print(global_utils.fps())  # Print FPS (crappy rate yeah)
            k = cv.waitKey(25)  # Get key pressed every 25ms
            if k == ord('s'):  # If 's' is pressed
                # Save the image in .temp/
                cv.imwrite(".temp/" + str(datetime.now()).replace(":", ".") + ".jpg", self.target_image)
            elif k == ord('q'):  # If 'q' is pressed
                cv.destroyWindow("dev")  # Destroy the window
                break

    def draw_debug(self):
        """
            Draw rect on find & show
        """
        self.target_image_debug = cv.rectangle(self.target_image_debug, self.find_start, self.find_end, (0, 255, 0), 5)
        self.show_image(self.target_image_debug)

    def get_image(self):
        """
            take capture & show
        """
        if self.adb.require_new_capture:
            self.adb.require_new_capture = False
            self.target_image = cv.imdecode(np.fromstring(self.adb.screenshot(), np.uint8), cv.IMREAD_COLOR)
            self.target_image_debug = self.target_image
            self.show_image()

    def load_images(self, images_list: list[str] = None) -> dict:
        """
            Load images and return dictionnary
                dict[path]={image, h, w}
        """
        if images_list is None:
            images_list = []
        res = {}
        for image in images_list:
            # global_utils.debug("load_images > " + image, -1)
            img = cv.imread(image, self.imread)
            if img is not None:
                h, w = img.shape[:2]
                res[image] = (img, h, w)
        return res

    def match_template(self, find_image):
        """
            return true if image match
        """
        return cv.matchTemplate(self.target_image, find_image, self.method)

    def match(self, data_image) -> bool:
        """
            return true if image match & set find_start & find_end
        """
        find_image, h, w = data_image
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(self.match_template(find_image))
        if max_val < self.threshold:
            self.find_start = None
            self.find_end = None
            return False
        self.find_start = max_loc
        self.find_end = (int(max_loc[0] + w), int(max_loc[1] + h))
        self.draw_debug()
        return True

    def match_multiple(self, data_image) -> bool:
        """
            return true if image match & set array of find_start & find_end for every match
        """
        # https://stackoverflow.com/a/58514954
        self.find_start = []
        self.find_end = []
        find_image, h, w = data_image
        res = self.match_template(find_image)
        max_val = 1
        while max_val > self.threshold:
            min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
            if max_val > self.threshold:
                res[max_loc[1] - h // 2:max_loc[1] + h // 2 + 1, max_loc[0] - w // 2:max_loc[0] + w // 2 + 1] = 0
                self.find_start.append(max_loc)
                self.find_end.append((int(max_loc[0] + w), int(max_loc[1] + h)))
        if len(self.find_start) == 0:
            self.find_start = None
            self.find_end = None
            return False
        return True

    def random_find(self) -> (int, int):
        """
            return random coords (x,y) between find_start & find_end
        """
        x1, y1 = self.find_start
        x2, y2 = self.find_end
        return random.randint(x1, x2), random.randint(y1, y2)

    def show_image(self, image=None):
        """
            show image if show_debug_image is set to True
        """
        if not self.show_debug_image:
            return
        if image is None:
            image = self.target_image
        cv.namedWindow("show_image", cv.WINDOW_NORMAL)
        cv.resizeWindow("show_image", 540, 960)
        cv.imshow("show_image", image)
        cv.waitKey(0)
        cv.destroyWindow("show_image")

    def tap_find(self, sleep_timer=0):
        """
            tap at random_find position
        """
        x, y = self.random_find()
        self.adb.tap(x, y, sleep_timer)
