import logging
import time
from datetime import datetime
from zipfile import ZipFile

import requests

from game import constant
from utils.constant import DebugLevel


def bytes_to_string(msg=None) -> str:
    """
        Convert utf-8 bytes into string
    """
    return msg.replace(b'\r\n', b'').decode("utf-8")


def debug(msg: str = '', debug_level: int = DebugLevel.ALWAYS):
    """
    print debug if enough level
    :param msg:
    :param debug_level:
    """
    msg = '[DEBUG] ' + str(datetime.now().strftime('%d/%m/%Y %H:%M:%S')) + ' - ' + msg
    if debug_level <= constant.DEBUG_LEVEL:
        # print(msg)
        logging.debug(msg)


def download_file(url: str) -> str:
    """
        download file from url, return file name from url
    :param url: URL to download
    :return: Path to file
    """
    r = requests.get(url, allow_redirects=True)
    filename = get_filename_from_url(url)
    open(filename, 'wb').write(r.content)
    return filename


def fps() -> float:
    """
    :return: fps
    """
    new_frame = time.time()
    timer = 1 / (new_frame - fps.frame)
    fps.frame = new_frame
    return timer


# https://stackoverflow.com/questions/279561/what-is-the-python-equivalent-of-static-variables-inside-a-function
fps.frame = time.time()


def get_filename_from_url(url: str) -> str:
    """
        return file name from url, last split after "/"
    :param url:
    :return:
    """
    if not url:
        return ""
    url_split = url.split("/")
    return url_split[len(url_split) - 1]


def info(msg: str = ''):
    """
    print info
    :param msg:
    """
    msg = '[INFO ] ' + str(datetime.now().strftime('%d/%m/%Y %H:%M:%S')) + ' - ' + msg
    # print(msg)
    logging.info(msg)


def log(msg: str = ''):
    """
    print log
    :param msg:
    """
    # print(msg)
    logging.info(''.join([i if ord(i) < 128 else ' ' for i in msg]))


def sleep(secs: float = 0, msg: str = ''):
    """
    sleep for x secs
    :param msg:
    :param secs:
    """
    if msg:
        info(msg)
    time.sleep(secs)


def unzip(filename, path: str = None):
    """
        unzip the file in the current repository
    :param filename:
    :param path:
    :return:
    """
    zp = ZipFile(filename)
    zp.extractall(path)
    zp.close()


def warn(msg: str = ''):
    """
    print warn
    :param msg:
    """
    msg = '[WARN ] ' + str(datetime.now().strftime('%d/%m/%Y %H:%M:%S')) + ' - ' + msg
    # print(msg)
    logging.warning(msg)
