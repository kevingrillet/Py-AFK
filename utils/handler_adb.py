import os
import platform
import subprocess
import time

from utils import global_utils


class HandlerAdb:
    def __init__(self, device="", adb=""):
        self.adb = adb
        self.device = device
        self.resolution = None
        self.system = platform.system()

    def check_installed(self):
        """
            Check if adb repository exists, if not try to download it
        """

        def install(url):
            """
                Download ADB and unzip it in the current repository then delete the .zip
            """
            global_utils.debug("install [url=" + url + "]")
            filename = global_utils.download_file(url)
            global_utils.unzip(filename, "../adb/")
            os.remove(filename)

        global_utils.debug("check")
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
        """
        global_utils.debug("connect [device=" + self.device + "]")
        return {
            "memu": global_utils.bytes_to_string(self.execute("connect localhost:21503")) == "device",
            "nox": global_utils.bytes_to_string(self.execute("connect localhost:62001")) == "device"
        }.get(self.device, global_utils.bytes_to_string(self.execute("get-state")) == "device")

    def execute(self, command) -> bytes:
        """
            execute command, return stdout & stderr
        """
        pipe = subprocess.Popen(self.adb + " " + command,
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        return pipe.stdout.read()

    def get_resolution(self):
        """
            return resolution of device
        """
        global_utils.debug("get_resolution ")
        self.resolution = global_utils.bytes_to_string(self.execute("shell wm size"))

    def init(self):
        """
            Init ADB
        """
        if self.adb == "":
            self.check_installed()
        self.restart()
        if not self.connect():
            print("[ERROR] Failed to connect to ADB.")
            exit(1)
        self.get_resolution()
        print(self.resolution)  # Get resolution
        self.settings("disable_orientation")

    def restart(self):
        """
            Restart ADB
        """
        global_utils.debug("restart")
        self.execute("kill-server")
        self.execute("start-server")

    def screen_input(self, input_type="", coords=None, sleep_timer=0):
        """
            Input related to screen:
                - tap       [<X>, <Y>]
                - swipe     [<X>, <Y>, <XEND>, <YEND>, <TIME>]
        """
        global_utils.debug("screen_input [input_type=" + input_type + ", coords=[" + str(coords)
                           + "], sleep_timer=" + str(sleep_timer) + "]")
        if input_type == "tap" and coords.len == 2:
            self.execute("input tap " + " ".join(coords))
            time.sleep(sleep_timer)
        elif input_type == "swipe" and coords.len == 5:
            self.execute("input swipe " + " ".join(coords))
            time.sleep(sleep_timer)

    def screenshot(self):
        """
            Take a screenshot and return it
        """
        global_utils.debug("screenshot")
        image_bytes = self.execute("shell screencap -p").replace(b'\r\n', b'\n')
        # noinspection PyTypeChecker
        return image_bytes

    def settings(self, tmp=""):
        """
            Function to work on settings, possible arguments:
                - disable_orientation
        """
        global_utils.debug("settings [tmp=" + tmp + "]")
        if tmp == "disable_orientation":
            self.execute(
                "content insert --uri content://settings/system --bind name:s:accelerometer_rotation --bind value:i:0")

    def start(self, app="", sleep_timer=0):
        """
            Restart the app
        """
        self.stop_app(app)
        self.start_app(app, sleep_timer)

    def start_app(self, app="", sleep_timer=0):
        """
            Start app then sleep for sleep_timer
        """
        global_utils.debug("start_app [app=" + app + ", sleep_timer=" + str(sleep_timer) + "]")
        if app:
            # execute("shell am start -n " + app)
            self.execute("shell monkey -p " + app + " 1")
            time.sleep(sleep_timer)

    def stop_app(self, app=""):
        """
            Start app then sleep for sleep_timer
        """
        global_utils.debug("stop_app [app=" + app + "]")
        if app:
            self.execute("shell am force-stop " + app)
