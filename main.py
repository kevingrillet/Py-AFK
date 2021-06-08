import cv2 as cv

import handler_adb

handler_adb.check_adb()
handler_adb.restart_adb()
handler_adb.check_device()

image = handler_adb.screenshot()
cv.imshow("", image)
cv.waitKey(0)
cv.destroyWindow("")
