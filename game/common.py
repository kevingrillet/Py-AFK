import time
from enum import auto

from utils.cls.SuperIntEnum import SuperIntEnum
from utils.handler_cv2 import HandlerCv2


class StartingStep(SuperIntEnum):
    INIT = auto()
    LOADING = auto()
    UNDER_MAINTENANCE = auto()
    POPUP = auto()
    UPDATING = auto()
    STARTED = auto()
    DONE = auto()


class Common:
    def __init__(self, cv2: HandlerCv2):
        self.cv2 = cv2
        self.images_list = ["./images/common/board_tales.jpg", "./images/common/campaign.jpg",
                            "./images/common/cross.jpg", "./images/common/load.jpg",
                            "./images/common/maintenance.jpg", "./images/common/special_gift.jpg",
                            "./images/common/update.jpg"]
        self.images = self.cv2.load_images(self.images_list)
        self.step = StartingStep.INIT

    def check_game_to_load(self) -> bool:
        """
            Check if afk arena title is visible (during start)
        """
        data_image = self.images["./images/common/load.jpg"]
        if self.cv2.check_match(data_image):
            self.step = StartingStep.LOADING
            return True
        elif self.step == StartingStep.LOADING:
            self.step = self.step.next()
        return False

    def check_maintenance(self) -> bool:
        """
            Check if maintenance popup is visible
            ToDo:
                - Add image
                - Restart the app after X secs
        """
        data_image = self.images["./images/common/maintenance.jpg"]
        if self.cv2.check_match(data_image):
            self.step = StartingStep.UNDER_MAINTENANCE
            return True
        elif self.step == StartingStep.UNDER_MAINTENANCE:
            self.step = self.step.first()
        return False

    def check_popup(self) -> bool:
        """
            Check if there is any visible popup (after game menu is loaded)
                - New hero
                - Special gift
                - Boarf Tales
        """
        data_image = self.images["./images/common/cross.jpg"]
        if self.cv2.check_match(data_image):
            self.step = StartingStep.POPUP
            self.cv2.tap_find(1)
            return True
        else:
            data_image = self.images["./images/common/special_gift.jpg"]
            if self.cv2.check_match(data_image):
                self.step = StartingStep.POPUP
                self.cv2.adb.tap(10, 10, 1)
                return True
            else:
                data_image = self.images["./images/common/board_tales.jpg"]
                if self.cv2.check_match(data_image):
                    self.step = StartingStep.POPUP
                    self.cv2.adb.tap(10, 10, 1)
                    return True
                elif self.step == StartingStep.POPUP:
                    self.step = self.step.next()
        return False

    def check_started(self) -> bool:
        """
            Check if the Campaign buton is visible 3 times with 1 sec of sleep between each
            If it fails, return false & set step to first
        """
        data_image = self.images["./images/common/campaign.jpg"]
        for i in range(3):
            self.cv2.adb.require_new_capture = True
            if not self.cv2.check_match(data_image):
                self.step = self.step.first()
                return False
            time.sleep(1)
        self.step = StartingStep.DONE
        return True

    def check_update(self) -> bool:
        """
            Check if update logo is visible in game
        """
        data_image = self.images["./images/common/update.jpg"]
        if self.cv2.check_match(data_image):
            self.step = StartingStep.UPDATING
            self.enable_fast_update()
            return True
        elif self.step == StartingStep.UPDATING:
            self.step = self.step.next()
        return False

    def enable_fast_update(self):
        """
            If game is updating, try to enable fast update then close the window
        """
        self.cv2.tap_find(1)
        data_image = self.images["./images/common/update.jpg"]
        if self.cv2.check_match(data_image):
            self.cv2.tap_find(1)
        self.cv2.adb.tap(10, 10, 1)

    def run(self):
        """
            Need to be launch after adb command to start the game
            It will try to do everything until game is loaded and in main menu
        """
        self.step = StartingStep.INIT
        while self.step != StartingStep.DONE:
            if self.step <= StartingStep.LOADING and self.check_game_to_load():
                continue
            # if self.step <= StartingStep.UNDER_MAINTENANCE and self.check_maintenance():
            #     continue
            if self.step <= StartingStep.POPUP and self.check_popup():
                continue
            if self.step <= StartingStep.UPDATING and self.check_update():
                continue
            if self.step <= StartingStep.STARTED and self.check_started():
                continue
