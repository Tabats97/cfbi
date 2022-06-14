
import cv2
import time
from cvzone.HandTrackingModule import HandDetector
from pynput.keyboard import Controller
from virtualkeyboard import VirtualKeyboard
from virtualmousepointer import VirtualMouse

# capturing the webcam
video_capture = cv2.VideoCapture(0, cv2.CAP_DSHOW) # works only for Windows

# setting a higher resolution, default resolution is 640x480
video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# Hand detector from cvzone library which uses OpenCV and Mediapipe libraries
# detectionCon is 0.5 by default but it's important to be sure about the detection
# in order to avoid to have a reliable system for the detection task
hand_detector = HandDetector(detectionCon=0.9, maxHands=1)
controller = Controller()

gestural_modality = "Mouse"
lastClick = time.time()

while True:
    _, img = video_capture.read()

    # hands detection in the image
    hands, img = hand_detector.findHands(img)

    if hands:
        # getting all info about one hand
        hand = hands[0]
        lmList = hand["lmList"] # list of 21 landmark points

        if lmList:
            # distance between tip of the thumb and of the little finger
            distance, _ = hand_detector.findDistance(lmList[4][0:2], lmList[20][0:2])
            # t = 190, the previous distance is used to switch between modalities
            if distance > 190 and gestural_modality == "Mouse" and time.time() - lastClick > 0.75:
                VirtualKeyboard(img, hand_detector).run(hand)
                gestural_modality = "Keyboard"
                lastClick = time.time()

            elif distance > 190 and gestural_modality == "Keyboard" and time.time() - lastClick > 0.75:
                VirtualMouse(img, hand_detector).run(hand)
                gestural_modality = "Mouse"
                lastClick = time.time()

            elif gestural_modality == "Mouse":
                VirtualMouse(img, hand_detector).run(hand)

            else:
                VirtualKeyboard(img, hand_detector).run(hand)

    cv2.imshow("Covid Free Browser Interaction", img)
    cv2.waitKey(1)
