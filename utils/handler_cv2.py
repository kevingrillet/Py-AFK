from datetime import datetime

import cv2 as cv
import numpy as np

from utils import global_utils
from utils.handler_adb import HandlerAdb


class HandlerCv2:
    def __init__(self, adb: HandlerAdb):
        self.adb = adb
        self.find_start = None
        self.find_end = None
        self.imread = cv.IMREAD_COLOR
        self.method = cv.TM_CCOEFF_NORMED
        self.target_image = None
        self.threshold = 0.9

    def check_match(self, data_image):
        self.get_image()
        return self.match(data_image)

    def check_match_multiple(self, find_image):
        self.get_image()
        return self.match_multiple(find_image)

    def dev(self):
        """
            Run dev mode, showing the capture
        """
        global_utils.debug("dev > s to save, q to quit")
        while True:
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
        color = (255, 0, 0)
        thickness = 2
        self.target_image = cv.rectangle(self.target_image, self.find_start, self.find_end, color, thickness)
        self.show_image()

    def get_image(self):
        self.target_image = cv.imdecode(np.fromstring(self.adb.screenshot(), np.uint8), cv.IMREAD_COLOR)
        self.show_image()

    def load_images(self, images_list: list[str] = None) -> dict:
        if images_list is None:
            images_list = []
        res = {}
        for image in images_list:
            img = cv.imread(image, self.imread)
            res[image] = (img, img.shape[:2])
        return res

    def match_template(self, find_image):
        return cv.matchTemplate(self.target_image, find_image, self.method)

    def match(self, data_image) -> bool:
        find_image, h, w = data_image
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(self.match_template(find_image))
        if max_val < self.threshold:
            self.find_start = None
            self.find_end = None
            return False
        self.find_start = max_loc[0]
        self.find_end = (int(max_loc[0] + w), int(max_loc[1] + h))
        return True

    def match_multiple(self, data_image) -> bool:
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
                self.find_start.append(max_loc[0])
                self.find_end.append((int(max_loc[0] + w), int(max_loc[1] + h)))
        if len(self.find_start) == 0:
            self.find_start = None
            self.find_end = None
            return False
        return True

    def show_image(self):
        cv.imshow("show_image", self.target_image)
        cv.waitKey(1)
        cv.destroyWindow("show_image")
