from datetime import datetime

import cv2 as cv

import handler_adb as adb
import utils

adb.check()  # Installing ADB
adb.restart()  # Starting ADB
if not adb.connect():
    print("[ERROR] Failed to connect to ADB")
    exit(1)
print(adb.get_resolution())  # Get resolution
adb.stop_app("com.lilithgame.hgame.gp")  # Stop the app
adb.start_app("com.lilithgame.hgame.gp", 30)  # Start the app

# Start
while True:
    image = adb.screenshot()  # Get image directly from ADB
    cv.imshow("", image)  # Show image in window
    print(utils.fps())  # Print FPS (crappy rate yeah)
    k = cv.waitKey(25)
    if k == ord('s'):  # If 's' is pressed
        cv.imwrite(".tmp/" + str(datetime.now()).replace(":", ".") + ".jpg", image)  # Save the image in .tmp/
    elif k == ord('q'):  # If 'q' is pressed
        cv.destroyWindow("")  # Destroy the window
        break
