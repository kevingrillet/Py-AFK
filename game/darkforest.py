from utils.cls import superdecorator
from utils.handlercv2 import HandlerCv2


@superdecorator.decorate_all_functions()
class DarkForest:
    def __init__(self, hcv2: HandlerCv2):
        self.hcv2 = hcv2 if hcv2 else HandlerCv2()

    def arena_of_heroes(self):
        print("TODO")
        # Arena of heroes
        # Challenge
        # Challenge last opponent until max

        # Legend's challenger tournament
        # Same

        # Legends championship
        # Always pick left? or right? user choice :)

    def bounty_board(self):
        print("TODO")
        # with sub function
        # Collect > Dispatch
        # Team bounty
        # Collect > Dispatch

    def kings_tower(self):
        print("TODO")
        # Open king's tower
        # Check if low level (directly in main King's Tower)
        # Depending on day, launch successively all King's Towers
        # Fuction to do it
        # Open tower
        # Tap challenge
        # If still OK it will open new window
        # Check Battle button, then click it, wait until win/loose, do it again until max attempt

    def run(self):
        self.kings_tower()
        self.arena_of_heroes()
        self.bounty_board()
