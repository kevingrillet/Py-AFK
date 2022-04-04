from enum import auto

from utils.cls import superdecorator, metasingleton, superintenum
from utils.handlercv2 import HandlerCv2


class Results(superintenum.SuperIntEnum):
    INIT = auto()
    IN_PROGRESS = auto()
    WIN = auto()
    LOOSE = auto()


@superdecorator.decorate_all_functions()
class Battle(metaclass=metasingleton.MetaSingleton):
    def __init__(self, hcv2: HandlerCv2):
        self.hcv2 = hcv2 if hcv2 else HandlerCv2()
        self.images = self.cv2.load_images(None)
        self.result = Results.INIT

    def enable_auto(self):
        # Check / try to enable x4, x2
        print("TODO")

    def enable_fast(self):
        # Check / try to enable x4, x2
        print("TODO")

    def run(self):
        self.result = Results.IN_PROGRESS
        self.enable_fast()
        self.enable_auto()
        self.waiting_battle_to_end()
        return self.result

    def waiting_battle_to_end(self):
        print("TODO")
        # Check if WIN / LOOSE
