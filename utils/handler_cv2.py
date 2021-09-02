import cv2 as cv


def match_template(img, template, method=cv.TM_CCOEFF_NORMED):
    res = cv.matchTemplate(img, template, method)
    return cv.minMaxLoc(res)
