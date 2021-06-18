import os
import platform
import subprocess
import time
from datetime import datetime

import cv2 as cv
import numpy as np

import utils


def check():
    """
        Check if adb repository exists, if not try to download it
    """
    utils.debug("check")
    if not os.path.exists("adb/"):
        ret = "ADB not found, installing " + platform.system() + " version."
        if platform.system() == "Windows":
            install("https://dl.google.com/android/repository/platform-tools-latest-windows.zip")
        elif platform.system() == "Darwin":
            install("https://dl.google.com/android/repository/platform-tools-latest-windows.zip")
        elif platform.system() == "Linux":
            install("https://dl.google.com/android/repository/platform-tools-latest-windows.zip")
    else:
        ret = "ADB found."
    return ret


def connect(device="") -> bool:
    """
        Check if device is connected
            - ""
            - "nox"
    """
    utils.debug("connect [device=" + device + "]")
    if device == "nox":
        return utils.bytes_to_string(execute("connect localhost:62001")) == "device"
    return utils.bytes_to_string(execute("get-state")) == "device"


def dev():
    while True:
        image = screenshot()  # Get image directly from ADB
        cv.imshow("dev", image)  # Show image in window
        print(utils.fps())  # Print FPS (crappy rate yeah)
        k = cv.waitKey(25)  # Get key pressed every 25ms
        if k == ord('s'):  # If 's' is pressed
            cv.imwrite("tmp/" + str(datetime.now()).replace(":", ".") + ".jpg", image)  # Save the image in tmp/
        elif k == ord('q'):  # If 'q' is pressed
            cv.destroyWindow("dev")  # Destroy the window
            break


def execute(command):
    """
        execute command, return stdout & stderr
    """
    pipe = subprocess.Popen("adb\\platform-tools\\adb.exe " + command,
                            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    return pipe.stdout.read()


def get_resolution() -> str:
    """
        return resolution of device
    """
    utils.debug("get_resolution ")
    return utils.bytes_to_string(execute("shell wm size"))


def screen_input(input_type="", coords=None, sleep_timer=0):
    """
        Input related to screen:
            - tap       [<X>, <Y>]
            - swipe     [<X>, <Y>, <XEND>, <YEND>, <TIME>]
    """
    utils.debug("screen_input [input_type=" + input_type + ", coords=[" + str(coords)
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
    utils.debug("install [url=" + url + "]")
    filename = utils.download_file(url)
    utils.unzip(filename, "adb/")
    os.remove(filename)


def restart():
    """
        Restart ADB
    """
    utils.debug("restart")
    execute("kill-server")
    execute("start-server")


def screenshot():
    """
        Take a screenshot and return it
    """
    utils.debug("screenshot")
    image_bytes = execute("shell screencap -p").replace(b'\r\n', b'\n')
    # noinspection PyTypeChecker
    return cv.imdecode(np.fromstring(image_bytes, np.uint8), cv.IMREAD_COLOR)


def settings(tmp=""):
    """
        Function to work on settings, possible arguments:
            - disable_orientation
    """
    utils.debug("settings [tmp=" + tmp + "]")
    if tmp == "disable_orientation":
        execute("content insert --uri content://settings/system --bind name:s:accelerometer_rotation --bind value:i:0")


def start_app(app="", sleep_timer=0):
    """
        Start app then sleep for sleep_timer
    """
    utils.debug("start_app [app=" + app + ", sleep_timer=" + str(sleep_timer) + "]")
    if app:
        # execute("shell am start -n " + app)
        execute("shell monkey -p " + app + " 1")
        time.sleep(sleep_timer)


def stop_app(app=""):
    """
        Start app then sleep for sleep_timer
    """
    utils.debug("stop_app [app=" + app + "]")
    if app:
        execute("shell am force-stop " + app)
