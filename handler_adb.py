import os
import platform

import cv2
import numpy as np

import utils


def check_adb():
    """
        Check if adb repository exists, if not try to download it
    """
    print("check_adb")
    if not os.path.exists("adb/"):
        print("adb not found")
        if platform.system() == "Windows":
            install_adb("https://dl.google.com/android/repository/platform-tools-latest-windows.zip")
        elif platform.system() == "Darwin":
            install_adb("https://dl.google.com/android/repository/platform-tools-latest-windows.zip")
        elif platform.system() == "Linux":
            install_adb("https://dl.google.com/android/repository/platform-tools-latest-windows.zip")
    else:
        print("adb found")


def install_adb(url):
    """
        Download ADB and unzip it in the current repository then delete the .zip
    """
    print("install_adb: " + url)
    filename = utils.download_file(url)
    utils.unzip(filename, "adb/")
    os.remove(filename)


def check_device(device=""):
    """
        Check if device is connected
    """
    print("check_device: " + device)
    if device == "nox":
        return utils.adb_execute("connect localhost:62001")
    return utils.adb_execute("get-state")


def restart_adb():
    """
        Restart ADB
    """
    print("restart_adb")
    utils.adb_execute("kill-server")
    utils.adb_execute("start-server")


def screenshot():
    """
        Take a screenshot and return it
    """
    image_bytes = utils.adb_execute("shell screencap -p").replace(b'\r\n', b'\n')
    return cv2.imdecode(np.fromstring(image_bytes, np.uint8), cv2.IMREAD_COLOR)
