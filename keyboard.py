
lower_keys = [["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "'", "ì", "<--"],
              ["q", "w", "e", "r", "t", "y", "u", "i", "o", "p", "[", "]"],
              ["a", "s", "d", "f", "g", "h", "j", "k", "l", "@", "#"],
              ["<", "z", "x", "c", "v", "b", "n", "m", ",", ".", "-"],
              ["Shift", "Space"]]

upper_keys = [["!", "\"", "*", "$", "%", "&", "/", "(", ")", "=", "?", "^", "<--"],
              ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P", "{", "}"],
              ["A", "S", "D", "F", "G", "H", "J", "K", "L", "@", "#"],
              [">", "Z", "X", "C", "V", "B", "N", "M", ",", ".", "_"],
              ["Shift", "Space"]]


class Key:
    def __init__(self, pos, text, size=[70, 70]):
        self.pos = pos
        self.text = text
        self.size = size


class Keyboard:
    def __init__(self, up=True):
        self.keyboard = []
        self.up = up
        if self.up:
            self.keys = upper_keys
        else:
            self.keys = lower_keys

    def is_up(self):
        return self.up

    def get_keyboard(self):
        return self.keyboard

    def create_keyboard(self):
        for i in range(len(self.keys)):
            for j, key in enumerate(self.keys[i]):
                if key == "<--" or key == "Shift":
                    self.keyboard.append(Key([90 * j + 50, 105 * i + 50], key, [120, 70]))
                elif key == "Space":
                    self.keyboard.append(Key([250 * j + 50, 105 * i + 50], key, [250, 70]))
                else:
                    self.keyboard.append(Key([90 * j + 50, 105 * i + 50], key))

        return self
