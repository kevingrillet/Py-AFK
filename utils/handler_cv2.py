from datetime import datetime

import cv2 as cv
import numpy as np

from utils import global_utils


class HandlerCv2:
    def __init__(self, adb):
        self.adb = adb
        self.find = None
        self.method = cv.TM_CCOEFF_NORMED
        self.target_image = None
        self.threshold = 0.9

    def check_match(self, find_image):
        self.get_image()
        return self.match(find_image)

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

    def get_image(self):
        self.target_image = cv.imdecode(np.fromstring(self.adb.screenshot(), np.uint8), cv.IMREAD_COLOR)

    def match_template(self, find_image):
        return cv.matchTemplate(self.target_image, find_image, self.method)

    def match(self, find_image) -> bool:
        h, w = find_image.shape[:2]
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(self.match_template(find_image))
        if max_val < self.threshold:
            self.find = None
            return False
        self.find = (int(max_loc[0] + (w / 2)), int(max_loc[1] + (h / 2)))
        return True

    def match_multiple(self, find_image) -> bool:
        # https://stackoverflow.com/a/58514954
        self.find = []
        h, w = find_image.shape[:2]
        res = self.match_template(find_image)
        max_val = 1
        while max_val > self.threshold:
            min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
            if max_val < self.threshold:
                res[max_loc[1]-h//2:max_loc[1]+h//2+1, max_loc[0]-w//2:max_loc[0]+w//2+1] = 0
            self.find.append((int(max_loc[0] + (w / 2)), int(max_loc[1] + (h / 2))))
        if len(self.find) == 0:
            self.find = None
            return False
        return True
