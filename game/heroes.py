from utils.cls import superdecorator
from utils.handlercv2 import HandlerCv2


@superdecorator.decorate_all_functions()
class Heroes:
    def __init__(self, hcv2: HandlerCv2):
        self.hcv2 = hcv2 if hcv2 else HandlerCv2()

    def enhance_gear(self):
        print("How?")

    def run(self):
        self.enhance_gear()
