import serial
import time
import math

nodeMcu = serial.Serial("COM10", 9600) #Sartup
straal=2
max_aantal_pixels = 640
helft_pixels = max_aantal_pixels/2
x_oud = 5000


def move(x,x_oud):
    if x != None:
        if abs(x_oud - x) > 75:
            x = x_oud
            if x > helft_pixels:
                x = x-helft_pixels
                angle = 90 - (math.sin(x / straal))
            elif x < helft_pixels:
                x = helft_pixels - x
                angle = 90 + (math.sin(x / straal))
            elif x == helft_pixels:
                angle = 90


            nodeMcu.write(str(angle).encode())
    return x_oud

#time.sleep(2) #Arduino heeft tijd nodig om connectie te maken
#move(180)
#time.sleep(1) #Tijd tussen commands nodig
#move(90)
#time.sleep(0.5)
#move(0)

