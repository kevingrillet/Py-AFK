from utils.handler_cv2 import HandlerCv2


class Campaign:
    def __init__(self, cv2: HandlerCv2):
        self.cv2 = cv2
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
        self.cv2.adb.tap_random((500, 1475), (600, 1550), 1)
        # Tap Collect
        self.cv2.adb.tap_random((500, 1475), (600, 1550), 1)
        # Check special crap
        data_image = self.images[""]
        if self.cv2.match(data_image):
            self.cv2.tap_find(1)
        # Check level up
        data_image = self.images[""]
        if self.cv2.match(data_image):
            self.cv2.tap_find(1)

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
