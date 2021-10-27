from enum import auto

from utils.cls.MetaSingleton import MetaSingleton
from utils.cls.SuperIntEnum import SuperIntEnum
from utils.handler_cv2 import HandlerCv2


class Results(SuperIntEnum):
    INIT = auto()
    IN_PROGRESS = auto()
    WIN = auto()
    LOOSE = auto()


class Battle(metaclass=MetaSingleton):
    def __init__(self, cv2: HandlerCv2):
        self.cv2 = cv2
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
