import cv2 as cv


# ToDo: facto, remove cv2

class CommonUtils:
    def __init__(self, cv2):
        self.cv2 = cv2

    def close_main_menu_popup(self):
        print("TODO")
        # Check if crap popup to close, special offers, ...

    def wait_game_to_load(self):
        game_is_loading = True
        template = cv.imread("images/common/campaign.jpg")
        while game_is_loading:
            if self.cv2.check_match(template):
                game_is_loading = False

    def wait_update(self):
        game_is_updating = True
        template = cv.imread("images/common/update.jpg")
        while game_is_updating:
            if self.cv2.check_match(template):
                game_is_updating = False
