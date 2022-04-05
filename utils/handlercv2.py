import os
import random
from datetime import datetime
from pathlib import Path

import numpy as np
from cv2 import cv2

from utils import common
from utils.common import debug, fps
from utils.handleradb import HandlerAdb


class HandlerCv2:
    find_start = None
    find_max_val = None
    find_end = None
    image_read_flag = cv2.IMREAD_COLOR
    method = cv2.TM_CCOEFF_NORMED
    require_new_capture = True
    target_image = None
    target_image_debug = None
    threshold = 0.9

    def __init__(self, hadb: HandlerAdb = None, show_debug_image: bool = False, scale: float = 1):
        self.scale = scale
        self.show_debug_image = show_debug_image
        self.hadb = hadb if hadb else HandlerAdb()

    def check_color(self, crl: (int, int, int) = None, cru: (int, int, int) = None,
                    rect: (int, int, int, int) = None) -> bool:
        """
        Take capture & check if image match
        :param crl: color_range_lower (B,G,R)
        :param cru: color_range_upper (B,G,R)
        :param rect: rect
        """
        self.get_image()
        for x in range(rect[0], rect[2]):
            for y in range(rect[1], rect[3]):
                c = self.target_image[y, x]
                if crl[0] < c[0] < cru[0] and crl[1] < c[1] < cru[1] and crl[2] < c[2] < cru[2]:
                    return True
        return False

    def check_match(self, data_image, force: bool = False) -> bool:
        """
        Take capture & check if image match
        coordinates can be accessed with find_start / find_end or directly tap with tap_find
        :param data_image: Image to find
        :param force: force capture
        :return: true / false
        """

        self.get_image(force)
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
        debug('dev > s to save, q to quit')
        while True:
            self.get_image(True)
            cv2.namedWindow('dev', cv2.WINDOW_NORMAL)
            cv2.resizeWindow('dev', 1600, 900)
            cv2.imshow('dev', self.target_image)  # Show image in window
            debug(str(fps()))  # Print FPS (crappy rate yeah)
            k = cv2.waitKey(25)  # Get key pressed every 25ms
            if k == ord('s'):  # If 's' is pressed
                # Save the image in .temp/
                Path('.temp/').mkdir(parents=True, exist_ok=True)
                cv2.imwrite('.temp/' + str(datetime.now()).replace(':', '.') + '.jpg', self.target_image)
            elif k == ord('q'):  # If 'q' is pressed
                cv2.destroyWindow('dev')  # Destroy the window
                break

    def draw_debug(self):
        """
        Draw rect on find & show
        """
        self.target_image_debug = cv2.rectangle(self.target_image_debug, self.find_start, self.find_end, (0, 255, 0), 5)
        self.show_image()

    def get_image(self, force: bool = False):
        """
        take capture & show
        :param force: force capture, else use require_new_capture
        """
        if self.require_new_capture or force:
            self.require_new_capture = False
            self.target_image = cv2.imdecode(np.fromstring(self.hadb.screenshot(), np.uint8), cv2.IMREAD_COLOR)
            self.target_image_debug = self.target_image
            self.show_image()

    def load_images(self, images_list: list[str] = None) -> dict:
        """
        Load images and return dictionary
        :param images_list: [path_to_image, ...]
        :return: dict[path]={image, h, w}
        """
        if images_list is None:
            images_list = []
        res = {}
        for image in images_list:
            # common.debug('load_images > ' + image, -1)
            if os.path.isfile('./images/' + image + '.jpg'):
                img = cv2.imread('./images/' + image + '.jpg', self.image_read_flag)
            else:
                common.warn('Image not found [' + image + ']')
                img = cv2.imread('./images/default.jpg', self.image_read_flag)
            if self.scale != 1:
                img = cv2.resize(img, (int(img.shape[1] * self.scale), int(img.shape[0] * self.scale)),
                                 interpolation=cv2.INTER_AREA)
            if img is not None:
                h, w = img.shape[:2]
                res[image] = (img, h, w)
        return res

    def log(self) -> str:
        """
        Return logs
        :return:
        """
        ret = ('{0:20} {1}'.format('\nfind:', str(self.find_max_val >= self.threshold)))
        ret += ('{0:20} {1}'.format('\nfind_max_val:', str(self.find_max_val)))
        if self.find_start:
            ret += ('{0:20} {1}'.format('\nfind_start:', str(self.find_start)))
        if self.find_end:
            ret += ('{0:20} {1}'.format('\nfind_end:', str(self.find_end)))
        return ret

    def match_template(self, find_image) -> bool:
        """
        return true if image match
        :param find_image: Image to find
        :return: true / false
        """
        return cv2.matchTemplate(self.target_image, find_image, self.method)

    def match(self, data_image) -> bool:
        """
        return true if image match & set find_start & find_end
        :param data_image: Image to find
        :return: true / false
        """
        find_image, h, w = data_image
        min_val, self.find_max_val, min_loc, max_loc = cv2.minMaxLoc(self.match_template(find_image))
        if self.find_max_val < self.threshold:
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
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
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
        :return:
        """
        x1, y1 = self.find_start
        if self.scale != 1:
            x1 = int(x1 / self.scale)
            y1 = int(y1 / self.scale)
        x2, y2 = self.find_end
        if self.scale != 1:
            x2 = int(x2 / self.scale)
            y2 = int(y2 / self.scale)
        return random.randint(x1, x2), random.randint(y1, y2)

    def save_image(self, image=None, folder: str = '.temp'):
        """
        Save image in param or target_image
        :param image:
        :param folder: path to save image
        """
        Path(folder + '/').mkdir(parents=True, exist_ok=True)
        cv2.imwrite(folder + '/' + str(datetime.now()).replace(':', '.') + '.jpg',
                    image if image else self.target_image)

    def show_image(self, image=None):
        """
        show image if show_debug_image is set to True
        :param image: Image to show
        """
        if not self.show_debug_image:
            return
        image = image if image else self.target_image_debug
        cv2.namedWindow('show_image', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('show_image', 1600, 900)
        cv2.imshow('show_image', image)
        k = cv2.waitKey(0)
        if k == ord('s'):
            Path('.temp/').mkdir(parents=True, exist_ok=True)
            cv2.imwrite('.temp/' + str(datetime.now()).replace(':', '.') + '.jpg', self.target_image)
        cv2.destroyWindow('show_image')

    def tap_find(self, sleep_timer: int = 0):
        """
            tap at random_find position
        """
        self.require_new_capture = True
        x, y = self.random_find()
        if self.scale != 1:
            x = int(x / self.scale)
            y = int(y / self.scale)
        self.hadb.tap(x, y, sleep_timer)
