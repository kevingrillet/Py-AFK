from utils.handler_cv2 import HandlerCv2


class Campaign:
    def __init__(self, cv2: HandlerCv2):
        self.cv2 = cv2

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
        # Tap Collect
        # Check level up & special crap

    def fast_rewards(self):
        print("TODO")
        # Check if free reward up (condition?)
        # Tap Fast Rewards
        # Tap Free
        # Loop & tap Use until max

    def gift_companion_points(self):
        print("TODO")

    def run(self):
        self.collect_loot()
        self.battle()
        self.fast_rewards()
        self.gift_companion_points()
        self.collect_loot()
