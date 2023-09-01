import speech_recognition as sr
import requests
import time
from selenium import webdriver
from selenium.common import NoSuchWindowException

chrome_driver = None


def listen_and_execute():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("\nSay something...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        recognized_text = recognizer.recognize_google(audio).lower()
        print("You said", recognized_text)
        execute_action(recognized_text)

    except sr.UnknownValueError:
        print("Could not understand.")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
    except requests.exceptions.HTTPError as e:
        print("HTTP Error: {0}".format(e))


def execute_action(action):
    global chrome_driver

    if "open" in action:
        url = action.replace("open", "").strip()
        final_url = "https://www." + url
        if not chrome_driver:
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument('--start-maximized')
            chrome_driver = webdriver.Chrome(options=chrome_options)
        try:
            chrome_driver.execute_script(f"window.open('{final_url}', '_blank');")
        except NoSuchWindowException:
            pass

    if "search" in action:
        query = action.replace("search", "").strip()
        search(query)

    if "stop" or "exit" in action:  # Fixed the space before "stop"
        exit()

    elif "close" in action:
        close_tabs()

    else:
        print("Could not execute.")


def search(query):
    global chrome_driver
    search_url = "https://www.google.com/search?q=" + query
    if not chrome_driver:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--start-maximized')
        chrome_driver = webdriver.Chrome(options=chrome_options)
    try:
        chrome_driver.execute_script(f"window.open('{search_url}', '_blank');")
    except NoSuchWindowException:
        pass


def close_tabs():
    if chrome_driver:
        chrome_driver.quit()


if __name__ == "__main__":
    while True:
        listen_and_execute()
