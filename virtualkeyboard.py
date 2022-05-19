import cv2
import time
from pynput.keyboard import Key, Controller
from keyboard import Keyboard

keyboard = Keyboard().create_keyboard()
controller = Controller()
lastClick = time.time()


class VirtualKeyboard:
    def __init__(self, img, hand_detector):
        self.img = img
        self.hand_detector = hand_detector

    def run(self, hand):

        global lastClick, keyboard

        lmList = hand["lmList"]
        fingers = self.hand_detector.fingersUp(hand)
        self.img = draw_keyboard(self.img, keyboard.get_keyboard())

        for key in keyboard.get_keyboard():
            x, y = key.pos
            w, h = key.size

            if x < lmList[8][0] < x + w and y < lmList[8][1] < y + h:
                draw_interaction(self.img, key.pos, key.size, key.text, (50, 50, 50))
                distance, _ = self.hand_detector.findDistance(lmList[8][0:2], lmList[12][0:2])

                if distance < 15 and time.time() - lastClick > 0.75 and fingers[1] == 1 and fingers[2] == 1:
                    if key.text == "Shift":
                        if keyboard.is_up():
                            new_keyboard = Keyboard(False).create_keyboard()
                        else:
                            new_keyboard = Keyboard().create_keyboard()

                        keyboard = new_keyboard
                        self.img = draw_keyboard(self.img, keyboard.get_keyboard())
                    else:
                        command = parse_command(key.text)
                        controller.press(command)
                        controller.release(command)
                        draw_interaction(self.img, key.pos, key.size, key.text, (0, 71, 171))

                    lastClick = time.time()


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