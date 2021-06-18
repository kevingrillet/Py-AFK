import cv2 as cv

import handler_adb as adb

adb.check()
adb.restart()
adb.connect()
adb.stop_app("com.lilithgame.hgame.gp")
adb.start_app("com.lilithgame.hgame.gp", 30)

image = adb.screenshot()
cv.imshow("", image)
cv.waitKey(0)
cv.destroyWindow("")
