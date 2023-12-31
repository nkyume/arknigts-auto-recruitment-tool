import pygetwindow as gw
from PIL import ImageGrab
from easyocr import Reader
import os


def extract(available_tags, window_name):

    try:
        window = gw.getWindowsWithTitle(window_name)[0]
    except IndexError:
        print("Error, can't find arknights window")
        return []
    else:
        pass

    x, y = window.topleft
    height, width = window.height, window.width

    top_x = x + width * 0.28
    top_y = y + height * 0.5
    bot_x = x + width * 0.66
    bot_y = y + height * 0.7

    screenshot = ImageGrab.grab(bbox=(top_x, top_y, bot_x, bot_y), all_screens=True)
    screenshot.save("tags.png")

    reader = Reader(["en"])
    result = reader.readtext("tags.png")
    tags = []
    if not result:
        print("Error. Make sure the arknights window is active.")
        return []
    for tag in result:
        if tag:
            tag = tag[1].replace(",","").replace(".","").strip()
        elif not tag or not tag in available_tags:
            print("Error. Make sure the arknights window is active.")
            return []
        tags.append(tag)

    os.remove("tags.png")

    return tags