from utils.handler_cv2 import HandlerCv2


class Common:
    def __init__(self, cv2: HandlerCv2):
        self.cv2 = cv2
        self.images_list = ["images/common/campaign.jpg", "images/common/update.jpg"]
        self.images = self.cv2.load_images(self.images_list)
        self.state = None

    def close_main_menu_popup(self):
        self.state = "game_is_starting"
        while self.state == "game_is_starting":
            data_image = self.images["images/common/load.jpg"]
            if self.cv2.check_match(data_image):
                self.cv2.tap_find(1)
            else:
                data_image = self.images["images/common/load.jpg"]
                if self.cv2.check_match(data_image):
                    self.cv2.tap_find(1)
                else:
                    self.state = 'game_ready'

    def run(self):
        self.state = "Init"
        self.wait_game_to_load()
        self.wait_maintenance()
        self.wait_update()
        self.close_main_menu_popup()

    def wait_game_to_load(self):
        data_image = self.images["images/common/load.jpg"]
        if not self.cv2.check_match(data_image):
            self.state = "game_is_loading"
        while self.state == "game_is_loading":
            if not self.cv2.check_match(data_image):
                self.state = "game_loaded"

    def wait_maintenance(self):
        data_image = self.images["images/common/maintenance.jpg"]
        if self.cv2.check_match(data_image):
            self.state = "game_is_under_maintenance"
        while self.state == "game_is_under_maintenance":
            if not self.cv2.check_match(data_image):
                self.state = "game_is_updating"

    def wait_update(self):
        data_image = self.images["images/common/update.jpg"]
        if self.cv2.check_match(data_image):
            self.state = "game_is_updating"
        while self.state == "game_is_updating":
            if not self.cv2.check_match(data_image):
                self.state = "game_updated"
