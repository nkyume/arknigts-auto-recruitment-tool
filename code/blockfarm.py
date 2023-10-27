import pyautogui as pa
from random import randint
from time import sleep

sanity = int(input("Sanity: "))
pa.PAUSE = 2.5
pa.FAILSAFE = True
print(int(sanity/6))
for _ in range(int(sanity/6)):
    offsetx, offsety = randint(-20,20),randint(-20,20)
    pa.moveTo(1655+offsetx,967+offsety,duration=1)
    sleep(randint(1,2))
    pa.click()
    sleep(randint(1,2))
    pa.moveTo(1587+offsetx,748+offsety,duration=1)
    sleep(randint(1,2))
    pa.click()
    sleep(100+randint(-5,5))
    pa.click()
    sleep(1)

    