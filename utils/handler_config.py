import configparser


class HandlerConfig:
    def __init__(self, path=""):
        self.path = path

    def get(self) -> configparser:
        if not self.path:
            return None
        config = configparser.ConfigParser()
        config.read(self.path)
        return config

    def init(self):
        if not self.get():
            print("[ERROR] No config found.")
