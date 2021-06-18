import handler_adb as adb
import cv2 as cv


def close_main_menu_popup():
    print("TODO")


def wait_game_to_load():
    game_is_loading = True
    template = cv.imread("images/.jpg")
    method = cv.TM_CCOEFF_NORMED
    while game_is_loading:
        img = adb.screenshot()
        res = cv.matchTemplate(img, template, method)
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
        cv.imshow("wait_game_to_load", res)
        print(min_val + " " + max_val + " " + min_loc + " " + max_loc)


def wait_update():
    game_is_updating = True
    template = cv.imread("images/.jpg")
    method = cv.TM_CCOEFF_NORMED
    while game_is_updating:
        img = adb.screenshot()
        res = cv.matchTemplate(img, template, method)
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
        cv.imshow("wait_update", res)
        print(min_val + " " + max_val + " " + min_loc + " " + max_loc)
