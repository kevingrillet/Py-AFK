from utils import common
from utils.cls import superdecorator
from utils.handlercv2 import HandlerCv2


# ToDo:
# - Use images instead of pixel color
# - Use random positions instead of fix one


@superdecorator.decorate_all_functions()
class Campaign:
    def __init__(self, hcv2: HandlerCv2):
        self.hcv2 = hcv2 if hcv2 else HandlerCv2()
        self.images = self.cv2.load_images(None)

    def battle(self):
        remaining_fight = 3
        if self.hcv2.check_match(self.images[""]):  # Find button Begin
            self.hcv2.tap_find(1)  # Begin
            if self.hcv2.check_match(self.images[""]):  # Check if BOSS
                self.hcv2.tap_find(1)  # Begin
                nb_win = 0
                nb_loose = 0
                while (remaining_fight > 0) and (not self.hcv2.check_match(self.images[""])):
                    if not self.hcv2.check_match(self.images[""]):  # Find button Begin for battle
                        raise NameError('Image found []')
                    self.hcv2.tap_find(1)

                    nb_try = 0
                    while not self.hcv2.check_match(self.images[""], True):
                        nb_try += 1
                        if nb_try > 10:
                            raise NameError('Battle did not start []')
                        common.sleep(1)

                    if self.hcv2.check_match(self.images[""]):  # Look for Skip
                        self.hcv2.tap_find(1)  # Skip
                    else:
                        if self.hcv2.check_match(self.images[""]):  # Check if auto is not pressed
                            self.hcv2.tap_find(1)  # auto
                        if not self.hcv2.check_match(self.images[""]):  # Check if x4 pressed
                            if self.hcv2.check_match(self.images[""]):  # Check for x4 not pressed
                                self.hcv2.tap_find(1)  # x4
                            elif self.hcv2.check_match(self.images[""]):  # Check for x2 not pressed:
                                self.hcv2.tap_find(1)  # x2

                    while not self.hcv2.check_match(self.images[""], True):  # Wait until battle is over
                        common.sleep(1)

                    victory = None
                    if self.hcv2.check_match(self.images[""]):  # Victory
                        victory = True
                    elif self.hcv2.check_match(self.images[""]):  # Victory with reward
                        victory = True
                    elif self.hcv2.check_match(self.images[""]):  # Failed & Failed in Challenger Tournament
                        victory = False

                    if victory:
                        nb_win += 1
                        if self.hcv2.check_match(self.images[""]):  # Check for next stage
                            self.hcv2.tap_find(6)
                            if self.hcv2.check_match(self.images[""]):  # Check if BOSS
                                self.hcv2.tap_find(1)  # Begin
                        else:
                            if self.hcv2.check_match(
                                    self.images[""]):  # Check for Continue button, does not exist for low level player
                                self.hcv2.tap_find(1)  # Continue
                            elif self.hcv2.check_match(self.images[""]):  # Find button Begin
                                self.hcv2.tap_find(1)  # Begin
                                if self.hcv2.check_match(self.images[""]):  # Check if BOSS
                                    self.hcv2.tap_find(1)  # Begin
                    elif not victory:
                        nb_loose += 1
                        if self.hcv2.check_match(
                                self.images[""]):  # Check for Try again button, does not exist for low level player
                            self.hcv2.tap_find(1)  # Try again
                        elif self.hcv2.check_match(self.images[""]):  # Find button Begin
                            self.hcv2.tap_find(1)  # Begin
                            if self.hcv2.check_match(self.images[""]):  # Check if BOSS
                                self.hcv2.tap_find(1)  # Begin
                    elif victory is None:
                        raise NameError('Battle failed to have victory / loose status :/')
                    remaining_fight -= 1

    def collect_loot(self):
        self.hcv2.hadb.tap(500, 1475, 1)  # Tap on Chest
        self.hcv2.hadb.tap(500, 1475, 1)  # Tap Collect
        if self.hcv2.check_match(self.images[""]):  # Check special crap
            self.hcv2.tap_find(1)
        if self.hcv2.check_match(self.images[""]):  # Check level up
            self.hcv2.tap_find(1)

    def fast_rewards(self):
        if self.hcv2.check_match(self.images[""]):  # Check if free reward up
            self.hcv2.tap_find(1)  # Tap Fast Rewards
            self.hcv2.hadb.tap(710, 1260)  # Tap Free
            self.hcv2.hadb.tap(560, 1800, 1)
            self.hcv2.hadb.tap(400, 1250)

    def gift_companion_points(self):
        if self.hcv2.check_match(self.images[""]):  # Check red dot friends
            self.hcv2.tap_find(1)
            self.hcv2.hadb.tap(930, 1600)  # Tap on send & Recieve if red dot
            if self.hcv2.check_match(self.images[""]):  # Check short-term red dot
                self.hcv2.tap_find(1)
                self.hcv2.hadb.tap(990, 190)  # Manage
                self.hcv2.hadb.tap(630, 1590)  # Apply
                self.hcv2.hadb.tap(750, 1410, 1)  # Auto Lend
                self.hcv2.hadb.tap(70, 1810, 0)  # Return
            self.hcv2.hadb.tap(70, 1810, 0)  # Return

    def run(self):
        self.collect_loot()
        self.battle()
        self.fast_rewards()
        self.gift_companion_points()
        self.collect_loot()
