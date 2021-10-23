import time
from zipfile import ZipFile

import requests

from utils import constant


def bytes_to_string(msg=None) -> str:
    """
        Convert utf-8 bytes into string
    """
    return msg.replace(b'\r\n', b'').decode("utf-8")


def debug(msg="", level=0):
    """
        print debug if enough level
    """
    if constant.DEBUG > level and msg != "":
        print("[DEBUG] " + msg)


def download_file(url) -> str:
    """
        download file from url, return file name from url
    """
    r = requests.get(url, allow_redirects=True)
    filename = get_filename_from_url(url)
    open(filename, 'wb').write(r.content)
    return filename


def fps() -> float:
    """
        return fps
    """
    new_frame = time.time()
    timer = 1 / (new_frame - fps.frame)
    fps.frame = new_frame
    return timer


# https://stackoverflow.com/questions/279561/what-is-the-python-equivalent-of-static-variables-inside-a-function
fps.frame = time.time()


def get_filename_from_url(url) -> str:
    """
        return file name from url, last split after "/"
    """
    if not url:
        return ""
    url_split = url.split("/")
    return url_split[len(url_split) - 1]


def unzip(filename, path=None):
    """
        unzip the file in the current repository
    """
    zp = ZipFile(filename)
    zp.extractall(path)
    zp.close()
