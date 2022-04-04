from utils.cls import superdecorator
from utils.handlercv2 import HandlerCv2


@superdecorator.decorate_all_functions()
class Ending:
    def __init__(self, hcv2: HandlerCv2):
        self.hcv2 = hcv2 if hcv2 else HandlerCv2()

    def marchants(self):
        print("TODO")

    def quests(self):
        def dailies():
            print("TODO")

        def weeklies():
            print("TODO")

        def campaign():
            print("TODO")

        dailies()
        weeklies()
        campaign()

    def mail(self):
        print("TODO")

    def run(self):
        self.marchants()
        self.quests()
        self.mail()
