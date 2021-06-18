import os
import platform
import subprocess
import time

import cv2
import numpy as np

import utils


def check():
    """
        Check if adb repository exists, if not try to download it
    """
    print("check")
    if not os.path.exists("adb/"):
        print("adb not found")
        if platform.system() == "Windows":
            install("https://dl.google.com/android/repository/platform-tools-latest-windows.zip")
        elif platform.system() == "Darwin":
            install("https://dl.google.com/android/repository/platform-tools-latest-windows.zip")
        elif platform.system() == "Linux":
            install("https://dl.google.com/android/repository/platform-tools-latest-windows.zip")
    else:
        print("adb found")


def connect(device=""):
    """
        Check if device is connected
    """
    print("connect [device=" + device + "]")
    if device == "nox":
        return execute("connect localhost:62001")
    return execute("get-state")


def execute(command):
    """
        execute command, return stdout & stderr
    """
    pipe = subprocess.Popen("adb\\platform-tools\\adb.exe " + command,
                            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    return pipe.stdout.read()


def screen_input(input_type="", coords=None, sleep_timer=0):
    """
        Input related to screen:
            - tap       [<X>, <Y>]
            - swipe     [<X>, <Y>, <XEND>, <YEND>, <TIME>]
    """
    print("screen_input [input_type=" + input_type + ", coords=[" + str(coords)
          + "], sleep_timer=" + str(sleep_timer) + "]")
    if input_type == "tap" and coords.len == 2:
        execute("input tap " + " ".join(coords))
        time.sleep(sleep_timer)
    elif input_type == "swipe" and coords.len == 5:
        execute("input swipe " + " ".join(coords))
        time.sleep(sleep_timer)


def install(url):
    """
        Download ADB and unzip it in the current repository then delete the .zip
    """
    print("install [url=" + url + "]")
    filename = utils.download_file(url)
    utils.unzip(filename, "adb/")
    os.remove(filename)


def restart():
    """
        Restart ADB
    """
    print("restart")
    execute("kill-server")
    execute("start-server")


def screenshot():
    """
        Take a screenshot and return it
    """
    print("screenshot")
    image_bytes = execute("shell screencap -p").replace(b'\r\n', b'\n')
    # It's working so I'll let it that way, but I prefer to have no warning
    # noinspection PyTypeChecker
    return cv2.imdecode(np.fromstring(image_bytes, np.uint8), cv2.IMREAD_COLOR)


def settings(tmp=""):
    """
        Function to work on settings, possible arguments:
            - disable_orientation
    """
    print("settings [tmp=" + tmp + "]")
    if tmp == "disable_orientation":
        execute("content insert --uri content://settings/system --bind name:s:accelerometer_rotation --bind value:i:0")


def start_app(app="", sleep_timer=0):
    """
        Start app then sleep for sleep_timer
    """
    print("start_app [app=" + app + ", sleep_timer=" + str(sleep_timer) + "]")
    if app:
        # execute("shell am start -n " + app)
        execute("shell monkey -p " + app + " 1")
        time.sleep(sleep_timer)


def stop_app(app=""):
    """
        Start app then sleep for sleep_timer
    """
    print("stop_app [app=" + app + "]")
    if app:
        execute("shell am force-stop " + app)
