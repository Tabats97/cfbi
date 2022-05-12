import cv2
import time
from cvzone.HandTrackingModule import HandDetector
from pynput.keyboard import Key, Controller
from keyboard import Keyboard


keyboard = Keyboard()
Keyboard.create_keyboard(keyboard)
controller = Controller()


class VirtualKeyboard:
    def __init__(self, img, hand_detector):
        self.img = img
        self.hand_detector = hand_detector

    def run(self):
        self.img = draw_keyboard(self.img, keyboard.keyboard)
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