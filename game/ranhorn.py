from utils.cls import superdecorator
from utils.handlercv2 import HandlerCv2


@superdecorator.decorate_all_functions()
class Ranhorn:
    def __init__(self, hcv2: HandlerCv2):
        self.hcv2 = hcv2 if hcv2 else HandlerCv2()

    def guild(self):
        def guild_hunting():
            print("TODO")
            # Wrizz then Soren

        def the_twisted_realm():
            print("TODO")

        # Check chest, open, ...
        guild_hunting()
        the_twisted_realm()

    def resonating_crystal(self):
        print("TODO")
        # If new slot take it, click 1 time level up, try to level up, everything under setting ofc

    def run(self):
        self.guild()
        self.the_oak_inn()
        self.temple_of_ascension()
        self.resonating_crystal()
        self.the_noble_tavern()
        self.store()

    def store(self):
        print("TODO")
        # Buy wanted items

    def temple_of_ascension(self):
        print("TODO")
        # If red dot do auto ugrade

    def the_noble_tavern(self):
        print("TODO")
        # Invoke free heart hero

    def the_oak_inn(self):
        print("TODO")
        # Enter the Tavern, if high level directly loot the 3 in the hall
        # If low level, tap right & enter the friends / guild towers to do the same
