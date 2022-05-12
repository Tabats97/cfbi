import pyttsx3
from selenium import webdriver
import speech_recognition as sr
import os

from selenium.webdriver.common.keys import Keys

ordinals = {
    "first": 0,
    "second": 1,
    "third": 2,
    "last": -1
}

settings = "user-data-dir=C:\\Users\\gabri\\AppData\\Local\\Google\\Chrome\\User Data\\Default"
dir_path = os.path.abspath(os.curdir)

# download the Chrome web driver associated to the browser version. In order to avoid cookie settings my default Chrome
# settings are imported
option = webdriver.ChromeOptions()
option.add_argument(settings)
driver = webdriver.Chrome(executable_path=dir_path + '\chromedriver.exe', chrome_options=option)


# initialization of the engine
engine = pyttsx3.init()

# getting the male and female voices of the engine
voices = engine.getProperty('voices')

# it's possible to choose a male [0] or a female voice [1]
engine.setProperty('voice', voices[1].id)

# Recognizer entity
recognizer = sr.Recognizer()

# set these parameters to adjust microphone input sensibility (they depend on the specific device)
recognizer.dynamic_energy_threshold = False
recognizer.energy_threshold = 800

# Microphone entity. The device_index parameter needs to be changed according to the input device that you want to use
microphone = sr.Microphone(device_index=1)


# The system takes the user's input, gives feedback to the user and recognizes the command
def recognize_speech():
    with microphone as input_device:
        input_audio = recognizer.listen(input_device, phrase_time_limit=5)

    # this will contain system response
    system_response = ""

    # System response in order to give feedback to the user
    system_speak("I'm processing your message")
    try:
        system_response = recognizer.recognize_google(input_audio)
    except:
        system_response = "An error occurred, please try again"

    return system_response


# Function to allow the system to provide feedback to the user
def system_speak(sentence):
    engine.say(sentence)
    engine.runAndWait()


# Check if the user tab that he/she is looking for exists, before performing the corresponding action
def check_and_switch_tab(command):
    key = command.split(" ")[-2]
    if key in ordinals and ordinals[key] >= len(driver.window_handles):
        system_speak("Invalid tab, try again")
        return False

    if key in ordinals:
        driver.switch_to.window(driver.window_handles[ordinals[key]])

    return True


# User's input is parsed in order to execute the correct action
def parse_command():
    command = recognize_speech().lower()
    print(command)

    if 'open' in command:
        target = command.split(" ")[1]
        if 'new tab' in command:
            driver.execute_script("window.open('');")
            tab_list = driver.window_handles
            driver.switch_to.window(tab_list[-1])

        driver.get('https://' + target + '.com')

    elif 'close' in command:

        if check_and_switch_tab(command):
            system_speak("I'm closing it")
            driver.close()
            driver.switch_to.window(driver.window_handles[-1])

    elif 'switch' in command:
        check_and_switch_tab(command)

    elif 'search on google' in command:
        element = driver.find_element_by_name('q')
        element.clear()
        element.click()

    elif 'scroll the page' in command:
        scroll_height = 0.1
        while scroll_height < 9.9:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight/%s);" % scroll_height)
            scroll_height += 0.01

    elif 'go back' in command:
        driver.back()

    elif 'go forward' in command:
        driver.forward()

    elif 'exit' in command:
        system_speak('Goodbye')
        driver.quit()
        return True

    else:
        system_speak("Sorry I didn't get your command, try again")

    return False


system_speak("Hello, I'm your browser assistant! How may I help you?")

while True:
    if parse_command():
        break
