
import pyttsx3
from selenium import webdriver
import speech_recognition as sr
import os
import psutil

ordinals = {
    "first": 0,
    "second": 1,
    "third": 2,
    "last": -1
}

# to avoid cookie settings every time the browser is launched
settings = "user-data-dir=C:\\Users\\Tabats\\AppData\\Local\\Google\\Chrome\\User Data\\Default"
dir_path = os.path.abspath(os.curdir)

# download the Chrome web driver associated to the browser version. In order to avoid cookie settings my default Chrome
# settings are imported
option = webdriver.ChromeOptions()
option.add_argument(settings)
driver = webdriver.Chrome(executable_path=dir_path + '\chromedriver', chrome_options=option)


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
recognizer.energy_threshold = 500


# Microphone entity. The device_index parameter needs to be changed according to the input device that you want to use
microphone = sr.Microphone(device_index=1)


# The system takes the user's input, gives feedback to the user and recognizes the command
def recognize_speech():
    with microphone as input_device:
        input_audio = recognizer.listen(input_device, phrase_time_limit=5)

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


# return the part of the page requested by the user
def point_of_the_page(command):
    page_height = driver.execute_script("return document.documentElement.scrollHeight")
    unit = page_height / 4

    words = command.split(" ")
    index = words.index("part")
    key = words[index-1]
    if key in ordinals:
        if key == "last":
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        else:
            y = unit * ordinals[key]
            driver.execute_script("window.scrollTo(0, %s);" % y)
    else:
        system_speak("Invalid section of the page, try again")


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
            if len(driver.window_handles) == 1:
                system_speak('If you want to stop the application, say exit')

            else:
                system_speak("I'm closing it")
                driver.close()
                driver.switch_to.window(driver.window_handles[-1])

    elif 'switch' in command:
        check_and_switch_tab(command)

    elif 'search on google' in command:
        element = driver.find_element_by_name('q')
        element.clear()
        element.click()

    elif 'scroll' in command:
        if 'down' not in command and 'up' not in command:
            system_speak("You need to specify in which direction to scroll the page")

        else:
            page_height = driver.execute_script("return document.documentElement.scrollHeight")

            if 'down' in command:
                scroll_height = 2
                while scroll_height < page_height:
                    driver.execute_script("window.scrollTo(0, %s)" % scroll_height)
                    scroll_height += 0.9

            if 'up' in command:
                scroll_height = page_height - 2
                while scroll_height > 0:
                    driver.execute_script("window.scrollTo(0, %s);" % scroll_height)
                    scroll_height -= 0.9

    elif 'part' in command:
        point_of_the_page(command)

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


# kill both speech and gestural modules
def kill_all():
    processes = []
    for proc in psutil.process_iter():
        if proc.name() == "python.exe":
            pinfo = proc.as_dict(attrs=['pid', 'name', 'username'])
            pinfo['vms'] = proc.memory_info().vms/ (1024 * 1024)
            processes.append(pinfo)

    processes = sorted(processes, key=lambda process: process['vms'], reverse=True)

    for element in processes:
        pid = element['pid']
        for proc in psutil.process_iter():
            if proc.pid == pid:
                proc.kill()
                break


system_speak("Hello, I'm your browser assistant.")

while True:
    system_speak("I'm ready for your command when you want.")
    if parse_command():
        kill_all()
