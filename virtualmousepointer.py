import autopy
import cv2
import numpy as np

wScr, hScr = autopy.screen.size()
frameR = 150
smooth_value = 3
plocX, plocY = 0, 0


class VirtualMouse:
    def __init__(self, img, hand_detector):
        self.img = img
        self.hand_detector = hand_detector
        self.plocX, self.plocY = plocX, plocY

    def run(self, hand):
        global plocX, plocY
        fingers = self.hand_detector.fingersUp(hand)
        lmList = hand["lmList"]
        x1, y1 = lmList[8][:2]

        # Move mouse if only index is up
        if fingers[1] == 1:

            # Convert coordinates
            cv2.rectangle(self.img, (frameR, frameR), (1280-frameR, 720-frameR), (255,0,255), 2)
            x = np.interp(x1, (frameR, 1280 - frameR), (0, wScr))
            y = np.interp(y1, (frameR, 720 - frameR), (0, hScr))
            clocX = self.plocX + (x - self.plocX) / smooth_value
            clocY = self.plocY + (y - self.plocY) / smooth_value

            try:
                autopy.mouse.move(clocX, clocY)
                plocX, plocY = clocX, clocY
            except:
                pass

        # Click mouse if index and middle are up
        if fingers[1] == 1 and fingers[2] == 1:
            distance, _ = self.hand_detector.findDistance(lmList[8][0:2], lmList[12][0:2])
            #if distance < 30:
                #autopy.mouse.click()