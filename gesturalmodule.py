import cv2
import time
from cvzone.HandTrackingModule import HandDetector
from pynput.keyboard import Key, Controller
from keyboard import Keyboard

# capturing the webcam
video_capture = cv2.VideoCapture(0, cv2.CAP_DSHOW) # works only for Windows

# setting a higher resolution, default resolution is 640x480
video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# Hand detector from cvzone library which uses OpenCV and Mediapipe libraries
# detectionCon is 0.5 by default but it's important to be sure about the detection
# in order to avoid to randomly press any key on the virtual keyboard
hand_detector = HandDetector(detectionCon=0.8)
keyboard = Keyboard().create_keyboard()
Keyboard.create_keyboard(keyboard)
controller = Controller()


def draw_interaction(img, pos, size, text, color):
    x, y = pos
    w, h = size
    cv2.rectangle(img, pos, (x + w, y + h), color, cv2.FILLED)
    cv2.putText(img, text, (x + 20, y + 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 3)


def draw_keyboard(img, keyboard):

    for key in keyboard:
        draw_interaction(img, key.pos, key.size, key.text, (20, 20, 20))

    return img


def parse_command(text):

    if text == "Space":
        return Key.space
    elif text == "<--":
        return Key.backspace
    else:
        return text


lastClick = time.time()

while True:
    _, img = video_capture.read()

    # hands detection in the image
    hands, img = hand_detector.findHands(img)

    if hands:
        # getting all info about one hand
        hand = hands[0]
        lmList = hand["lmList"] # list of 21 landmark points
        bbox = hand["bbox"] # bounding box info x, y, w, h
        center = hand["center"] # center of the hand cx, cy
        handType = hand["type"] # left or right hand

        fingers = hand_detector.fingersUp(hand)
        img = draw_keyboard(img, keyboard.keyboard)

        if lmList:
            for key in keyboard.keyboard:
                x, y = key.pos
                w, h = key.size

                if x < lmList[8][0] < x + w and y < lmList[8][1] < y + h:
                    draw_interaction(img, key.pos, key.size, key.text, (50, 50, 50))
                    distance, _ = hand_detector.findDistance(lmList[8][0:2], lmList[12][0:2])

                    if distance < 30 and time.time() - lastClick > 0.75:
                        if key.text == "Shift":
                            if Keyboard.is_up(keyboard):
                                keyboard = Keyboard(False)
                            else:
                                keyboard = Keyboard()

                            Keyboard.create_keyboard(keyboard)
                            img = draw_keyboard(img, keyboard.keyboard)
                        else:
                            command = parse_command(key.text)
                            controller.press(command)
                            controller.release(command)
                            draw_interaction(img, key.pos, key.size, key.text, (0, 71, 171))

                        lastClick = time.time()

        #cv2.rectangle(img, (50, 550), (700, 450), (50, 50, 50), cv2.FILLED)
        #cv2.putText(img, final_text, (60, 500), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 3)

    cv2.imshow("Webcam", img)
    cv2.waitKey(1)


