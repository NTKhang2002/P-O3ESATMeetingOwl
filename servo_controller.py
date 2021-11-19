import serial
import time
<<<<<<< HEAD
nodeMcu = serial.Serial("COM10", 9600) #Sartup en kijk goed na welke poort
=======
import math

nodeMcu = serial.Serial("COM10", 9600) #Sartup
straal=2
max_aantal_pixels = 580
helft_pixels = max_aantal_pixels/2

def move(x):
    time.sleep(2)
    if x > helft_pixels:
        x = x-helft_pixels
        angle = 90 - (math.sin(x / straal))
    elif x < helft_pixels:
        x = helft_pixels - x
        angle = 90 + (math.sin(x / straal))
    elif x == helft_pixels:
        angle = 90

>>>>>>> c60db7a9 (commit)

    nodeMcu.write(str(angle).encode())

#time.sleep(2) #Arduino heeft tijd nodig om connectie te maken
#move(180)
#time.sleep(1) #Tijd tussen commands nodig
#move(90)
#time.sleep(0.5)
#move(0)

