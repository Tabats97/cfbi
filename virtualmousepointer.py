import time

import autopy
import cv2
import numpy as np

# values to map mouse box interface with the screen and to smooth mouse movement
wScr, hScr = autopy.screen.size()
frameR = 150
smooth_value = 5
plocX, plocY = 0, 0
lastclick = time.time()


class VirtualMouse:
    def __init__(self, img, hand_detector):
        self.img = img
        self.hand_detector = hand_detector
        self.plocX, self.plocY = plocX, plocY

    def run(self, hand):
        global plocX, plocY, lastclick

        # getting hand detected information
        fingers = self.hand_detector.fingersUp(hand)
        lmList = hand["lmList"]
        x1, y1 = lmList[8][:2]

        # Move mouse if only index is up
        if fingers[1] == 1:

            # Convert coordinates, applying mapping and smoothing movement
            cv2.rectangle(self.img, (frameR, frameR), (1280-frameR, 720-frameR), (255,0,255), 2)
            x = np.interp(x1, (frameR, 1280 - frameR), (0, wScr))
            y = np.interp(y1, (frameR, 720 - frameR), (0, hScr))
            clocX = self.plocX + (x - self.plocX) / smooth_value
            clocY = self.plocY + (y - self.plocY) / smooth_value

            try:
                autopy.mouse.move(wScr - clocX, clocY)
                plocX, plocY = clocX, clocY
            except:
                pass

        # Click mouse if index and middle are up and d < t, where t = 20
        if time.time() - lastclick > 0.75 and fingers[1] == 1 and fingers[2] == 1:
            distance, _ = self.hand_detector.findDistance(lmList[8][:2], lmList[12][:2])
            if distance < 20:
                autopy.mouse.click()
                lastclick = time.time()
