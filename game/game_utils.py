from utils import handler_adb as adb, handler_cv2 as hcv
import cv2 as cv


def close_main_menu_popup():
    print("TODO")


def wait_game_to_load():
    game_is_loading = True
    template = cv.imread("images/.jpg")
    while game_is_loading:
        min_val, max_val, min_loc, max_loc = hcv.match_template(adb.screenshot(), template)
        print(min_val + " " + max_val + " " + min_loc + " " + max_loc)


def wait_update():
    game_is_updating = True
    template = cv.imread("images/.jpg")
    while game_is_updating:
        min_val, max_val, min_loc, max_loc = hcv.match_template(adb.screenshot(), template)
        print(min_val + " " + max_val + " " + min_loc + " " + max_loc)
