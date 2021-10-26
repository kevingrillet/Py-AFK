from utils.handler_cv2 import HandlerCv2


class Common:
    def __init__(self, cv2: HandlerCv2):
        self.cv2 = cv2
        self.images_list = ["images/common/campaign.jpg", "images/common/update.jpg"]
        self.images = self.cv2.load_images(self.images_list)

    def close_main_menu_popup(self):
        print("TODO")
        # Check if crap popup to close, special offers, ...

    def run(self):
        self.wait_game_to_load()
        self.wait_update()
        self.close_main_menu_popup()

    def wait_game_to_load(self):
        game_is_loading = True
        data_image = self.images["images/common/campaign.jpg"]
        while game_is_loading:
            if self.cv2.check_match(data_image):
                game_is_loading = False

    def wait_update(self):
        game_is_updating = True
        data_image = self.images["images/common/update.jpg"]
        while game_is_updating:
            if self.cv2.check_match(data_image):
                game_is_updating = False
