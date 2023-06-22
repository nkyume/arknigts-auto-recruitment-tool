import pygetwindow as gw
from PIL import ImageGrab
import easyocr
import sys


def extract(avalible_tags):

    try:
        window = gw.getWindowsWithTitle("BlueStacks App Player")[0]
    except IndexError:
        sys.exit("Can't find arknights window")
    else:
        pass

    x, y = window.topleft
    height, width = window.height, window.width

    top_x = x + width * 0.28
    top_y = y + height * 0.5
    bot_x = x + width * 0.66
    bot_y = y + height * 0.7

    screenshot = ImageGrab.grab(bbox=(top_x, top_y, bot_x, bot_y))

    screenshot.save("tags.jpg")

    reader = easyocr.Reader(["en"])
    result = reader.readtext("tags.jpg")

    tags = []
    for tag in result:
        if not tag[1] in avalible_tags or not tag:
            print(tag[1])
            print(avalible_tags)
            sys.exit("Something went wrong, make sure that arknights window is active")

        tags.append(tag[1])

    return tags
