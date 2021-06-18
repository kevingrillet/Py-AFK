import cv2 as cv

import handler_adb

handler_adb.check_adb()
handler_adb.restart_adb()
handler_adb.check_device()
handler_adb.start_app("com.lilithgame.hgame.gp", 30)

image = handler_adb.screenshot()
cv.imshow("", image)
cv.waitKey(0)
cv.destroyWindow("")
