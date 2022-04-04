from utils.cls import superdecorator
from utils.handlercv2 import HandlerCv2


@superdecorator.decorate_all_functions()
class Campaign:
    def __init__(self, hcv2: HandlerCv2):
        self.hcv2 = hcv2 if hcv2 else HandlerCv2()
        self.images = self.cv2.load_images(None)

    def battle(self):
        print("TODO")
        # Find button Begin
        # Check if BOSS
        # Boss
        # Find button Begin for battle
        # Find button Begin Battle
        # Continue until last battle
        # Get loot

    def collect_loot(self):
        print("TODO")
        # Tap on Chest
        self.hcv2.hadb.tap_random((500, 1475), (600, 1550), 1)
        # Tap Collect
        self.hcv2.hadb.tap_random((500, 1475), (600, 1550), 1)
        # Check special crap
        data_image = self.images[""]
        if self.hcv2.match(data_image):
            self.hcv2.tap_find(1)
        # Check level up
        data_image = self.images[""]
        if self.hcv2.match(data_image):
            self.hcv2.tap_find(1)

    def fast_rewards(self):
        print("TODO")
        # Check if free reward up (condition?)
        # Tap Fast Rewards
        # Tap Free
        # Loop & tap Use until max

    def gift_companion_points(self):
        print("TODO")
        # Check red dot friends
        # Tap on send & Recieve if red dot
        # Check short-term red dot
        # Manage
        # Rent out

    def run(self):
        self.collect_loot()
        self.battle()
        self.fast_rewards()
        self.gift_companion_points()
        self.collect_loot()
