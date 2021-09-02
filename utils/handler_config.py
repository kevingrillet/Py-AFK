import configparser


def get(path="") -> configparser:
    if not path:
        return None
    config = configparser.ConfigParser()
    config.read(path)
    return config
