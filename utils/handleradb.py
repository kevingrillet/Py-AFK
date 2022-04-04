import os
import platform
import random
import subprocess
import time

import psutil as psutil

from utils import common


class HandlerAdb:
    def __init__(self, device="", adb=""):
        self.adb = adb
        self.device = device
        self.require_new_capture = True
        self.resolution = None
        self.system = platform.system()

    def app_check(self, app="") -> bool:
        """
            Check if app is running
        :param app: name of the app
        :return: true/false
        """
        common.debug("app_check [app=" + app + "]")
        if app:
            return self.execute("shell pidof " + app) != ""
        return False

    def app_start(self, app="", sleep_timer=0):
        """
            Start app then sleep for sleep_timer
        :param app: name of the app
        :param sleep_timer:
        :return:
        """
        common.debug("app_start [app=" + app + ", sleep_timer=" + str(sleep_timer) + "]")
        if app:
            # execute("shell am start -n " + app)
            self.execute("shell monkey -p " + app + " 1")
            time.sleep(sleep_timer)

    def app_stop(self, app=""):
        """
            Start app then sleep for sleep_timer
        :param app: name of the app
        :return:
        """
        common.debug("app_stop [app=" + app + "]")
        if app:
            self.execute("shell am force-stop " + app)

    def check_installed(self):
        """
            Check if adb repository exists, if not try to download it
        """

        def install(url):
            """
                Download ADB and unzip it in the current repository then delete the .zip
            :param url: url of adb
            :return:
            """
            common.debug("install [url=" + url + "]")
            filename = common.download_file(url)
            common.unzip(filename, "../adb/")
            os.remove(filename)

        common.debug("check")
        if not os.path.exists("../adb/"):
            ret = "ADB not found, installing " + self.system + " version."
            if self.system == "Windows":
                install("https://dl.google.com/android/repository/platform-tools-latest-windows.zip")
            elif self.system == "Darwin":
                install("https://dl.google.com/android/repository/platform-tools-latest-darwin.zip")
            elif self.system == "Linux":
                install("https://dl.google.com/android/repository/platform-tools-latest-linux.zip")
        else:
            ret = "ADB found."
        self.adb = "adb\\platform-tools\\adb.exe"
        return ret

    def connect(self) -> bool:
        """
            Check if device is connected
                - ""
                - "memu"
                - "nox"

        :return: true/false
        """
        common.debug("connect [device=" + self.device + "]")
        return {
            "memu": common.bytes_to_string(self.execute("connect localhost:21503")) == "device",
            "nox": common.bytes_to_string(self.execute("connect localhost:62001")) == "device"
        }.get(self.device, common.bytes_to_string(self.execute("get-state")) == "device")

    def execute(self, command) -> bytes:
        """
            execute command, return stdout & stderr

        :param command: command to execute
        :return: stdout / stderr
        """
        pipe = subprocess.Popen(self.adb + " " + command,
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        return pipe.stdout.read()

    def find_nox_adb(self):
        """
            Look for adb in nox
        :return:
        """
        processes = filter(lambda p: psutil.Process(p).name() == "nox_adb", psutil.pids())
        for pid in processes:
            path = os.path.abspath(psutil.Process(pid).cmdline()[1])
            if path != "":
                self.adb = path
                break

    def get_resolution(self):
        """
            get resolution of device
        """
        common.debug("get_resolution ")
        self.resolution = common.bytes_to_string(self.execute("shell wm size"))

    def init(self):
        """
            Init ADB
        """
        if self.adb == "":
            if self.device == "Nox":
                self.find_nox_adb()
            else:
                self.check_installed()
        self.restart_adb()
        if not self.connect():
            print("[ERROR] Failed to connect to ADB.")
            exit(1)
        self.get_resolution()
        self.execute("shell settings put global heads_up_notifications_enabled 0")
        self.settings("disable_orientation")

    def restart_adb(self):
        """
            Restart ADB
        """
        common.debug("restart")
        self.execute("kill-server")
        self.execute("start-server")

    def screen_input(self, input_type="", coords: list[int] = None, sleep_timer=0):
        """
            Input related to screen:
                - tap       [<X>, <Y>]
                - swipe     [<X>, <Y>, <XEND>, <YEND>, <TIME>]

        :param input_type: tap/swipe
        :param coords:
        :param sleep_timer:
        :return:
        """
        if coords is None:
            coords = []
        common.debug("screen_input [input_type=" + input_type + ", coords=[" + str(coords)
                     + "], sleep_timer=" + str(sleep_timer) + "]")
        if input_type == "tap" and len(coords) == 2:
            self.execute("input tap " + " ".join(coords))
            time.sleep(sleep_timer)
        elif input_type == "swipe" and len(coords) == 5:
            self.execute("input swipe " + " ".join(coords))
            time.sleep(sleep_timer)
        self.require_new_capture = True

    def screenshot(self):
        """
            Take a screenshot and return it
        :return: image bytes
        """
        common.debug("screenshot")
        image_bytes = self.execute("shell screencap -p").replace(b'\r\n', b'\n')
        # noinspection PyTypeChecker
        return image_bytes

    def settings(self, setting=""):
        """
            Function to work on settings, possible arguments:
                - disable_orientation
        :param setting:
        :return:
        """
        common.debug("settings [tmp=" + setting + "]")
        if setting == "disable_orientation":
            self.execute(
                "content insert --uri content://settings/system --bind name:s:accelerometer_rotation --bind value:i:0")

    def start(self, app="", sleep_timer=0):
        """
            Restart the app
        :param app: app name
        :param sleep_timer:
        :return:
        """
        self.app_stop(app)
        self.app_start(app, sleep_timer)

    def swipe(self, from_position=None, to_position=None, sleep_timer=0, swipe_timer=0):
        """
            input swipt to screen (short version of screen_input)
        :param from_position:
        :param to_position:
        :param sleep_timer:
        :param swipe_timer:
        :return:
        """
        if to_position is None:
            to_position = [0, 0]
        if from_position is None:
            from_position = [0, 0]
        self.screen_input("swipe", [from_position[0], from_position[1], to_position[0], to_position[1], swipe_timer],
                          sleep_timer)

    def tap(self, x=0, y=0, sleep_timer=0):
        """
            input tab to screen (short version of screen_input)
        :param x:
        :param y:
        :param sleep_timer:
        :return:
        """
        self.screen_input("tab", [x, y], sleep_timer)

    def tap_random(self, p1=(0, 0), p2=(0, 0), sleep_timer=0):
        """
            input tab to screen (short version of screen_input)
        :param p1:
        :param p2:
        :param sleep_timer:
        :return:
        """
        self.screen_input("tab", [random.randint(p1[0], p2[0]), random.randint(p1[1], p2[1])], sleep_timer)
