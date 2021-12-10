# Utils : mouse jiggler
# A mouse jiggler is a tool which, when plugged into a target computer, prevents it from falling asleep by moving the mouse to simulate human input. 
# https://www.youtube.com/watch?v=aZ8u56I3J3I

import mouse
import time
import random

m1 = 1
m2 = 15
j = 10
base = time.monotonic()

def getRandomTime():
    return (random.randint(m1, m2))

timeInterval = getRandomTime()

while True:
    if (time.monotonic() - base) > timeInterval:
        print('Boop')
        mouse.move(j,j,absolute=False,duration=0.2)
        mouse.move(-abs(j),-abs(j),absolute=False,duration=0.2)
        base = time.monotonic()
        timeInterval = getRandomTime()
        print(f'going again in {timeInterval}')
