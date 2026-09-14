import time
import webbrowser
from urllib.parse import quote

import pyautogui


def open_application(app_name):
    app_name = str(app_name).strip()

    if not app_name:
        return "No application name provided."

    pyautogui.press("win")
    time.sleep(0.5)

    pyautogui.write(app_name, interval=0.05)
    time.sleep(0.5)

    pyautogui.press("enter")
    time.sleep(1.0)

    return f"Opened {app_name}."


def search_browser(query):
    query = str(query).strip()

    if not query:
        return "I need something to search for."

    search_url = "https://www.google.com/search?q=" + quote(query)

    webbrowser.open(search_url)

    return f"Searching for {query}."


def type_text(text):
    if text is None:
        return "There is nothing to type."

    text = str(text)

    if not text:
        return "There is nothing to type."

    lines = text.split("\n")

    for index, line in enumerate(lines):

        if line:
            pyautogui.write(
                line,
                interval=0.02
            )

        if index < len(lines) - 1:
            pyautogui.press("enter")

    return "Done."