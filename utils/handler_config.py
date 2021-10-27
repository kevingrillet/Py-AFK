import configparser

from utils.cls.MetaSingleton import MetaSingleton


class HandlerConfig(metaclass=MetaSingleton):
    def __init__(self, path=""):
        self.path = path

    def get(self) -> configparser:
        """
            return config
        """
        if not self.path:
            return None
        config = configparser.ConfigParser()
        config.read(self.path)
        return config

    def init(self):
        """
            check if config exists
        """
        if not self.get():
            print("[ERROR] No config found.")
