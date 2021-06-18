import os
import platform
import subprocess
import time

import cv2
import numpy as np

import utils


def adb_execute(command):
    """
        execute command, return stdout & stderr
    """
    pipe = subprocess.Popen("adb\\platform-tools\\adb.exe " + command,
                            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    return pipe.stdout.read()


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
    print("install_adb [url=" + url + "]")
    filename = utils.download_file(url)
    utils.unzip(filename, "adb/")
    os.remove(filename)


def check_device(device=""):
    """
        Check if device is connected
    """
    print("check_device [device=" + device + "]")
    if device == "nox":
        return adb_execute("connect localhost:62001")
    return adb_execute("get-state")


def restart_adb():
    """
        Restart ADB
    """
    print("restart_adb")
    adb_execute("kill-server")
    adb_execute("start-server")


def screenshot():
    """
        Take a screenshot and return it
    """
    print("screenshot")
    image_bytes = adb_execute("shell screencap -p").replace(b'\r\n', b'\n')
    return cv2.imdecode(np.fromstring(image_bytes, np.uint8), cv2.IMREAD_COLOR)


def start_app(app="", sleep_timer=0):
    """
        Start app then sleep for sleep_timer
    """
    print("start_app [app=" + app + ", sleep_timer=" + str(sleep_timer) + "]")
    if app:
        # adb_execute("shell am start -n " + app)
        adb_execute("shell monkey -p " + app + " 1")
        time.sleep(sleep_timer)


def stop_app(app=""):
    """
        Start app then sleep for sleep_timer
    """
    print("stop_app [app=" + app + "]")
    if app:
        adb_execute("shell am force-stop " + app)
