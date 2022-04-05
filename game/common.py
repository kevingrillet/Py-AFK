import time
from enum import auto

from utils.cls import superdecorator, superintenum
from utils.handlercv2 import HandlerCv2


class StartingStep(superintenum.SuperIntEnum):
    INIT = auto()
    LOADING = auto()
    UNDER_MAINTENANCE = auto()
    POPUP = auto()
    UPDATING = auto()
    STARTED = auto()
    DONE = auto()


@superdecorator.decorate_all_functions()
class Common:
    step = StartingStep.INIT

    def __init__(self, hcv2: HandlerCv2):
        self.hcv2 = hcv2 if hcv2 else HandlerCv2()
        self.images = self.hcv2.load_images(["common/board_tales", "common/campaign",
                                             "common/cross", "common/load",
                                             "common/maintenance", "common/special_gift",
                                             "common/update"])

    def check_game_to_load(self) -> bool:
        """
            Check if afk arena title is visible (during start)
        """
        if self.hcv2.check_match(self.images["common/load"]):
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
        if self.hcv2.check_match(self.images["common/maintenance"]):
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
        if self.hcv2.check_match(self.images["common/cross"]):
            self.step = StartingStep.POPUP
            self.hcv2.tap_find(1)
            return True
        else:
            if self.hcv2.check_match(self.images["common/special_gift"]):
                self.step = StartingStep.POPUP
                self.hcv2.hadb.tap(10, 10, 1)
                return True
            else:
                if self.hcv2.check_match(self.images["common/board_tales"]):
                    self.step = StartingStep.POPUP
                    self.hcv2.hadb.tap(10, 10, 1)
                    return True
                elif self.step == StartingStep.POPUP:
                    self.step = self.step.next()
        return False

    def check_started(self) -> bool:
        """
            Check if the Campaign buton is visible 3 times with 1 sec of sleep between each
            If it fails, return false & set step to first
        """
        for i in range(3):
            if not self.hcv2.check_match(self.images["common/campaign"], True):
                self.step = self.step.first()
                return False
            time.sleep(1)
        self.step = StartingStep.DONE
        return True

    def check_update(self) -> bool:
        """
            Check if update logo is visible in game
        """
        if self.hcv2.check_match(self.images["common/update"]):
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
        self.hcv2.tap_find(1)
        if self.hcv2.check_match(self.images["common/update"]):
            self.hcv2.tap_find(1)
        self.hcv2.hadb.tap(10, 10, 1)

    def run(self):
        """
            Need to be launch after adb command to start the game
            It will try to do everything until game is loaded and in main menu
        """
        self.step = StartingStep.INIT
        while self.step != StartingStep.DONE:
            self.hcv2.require_new_capture = True
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
