import serial
import time
nodeMcu = serial.Serial("COM10", 9600) #Sartup

def move(angle):
    nodeMcu.write(str(angle).encode())

time.sleep(2) #Arduino heeft tijd nodig om connectie te maken
move(180)
time.sleep(1) #Tijd tussen commands nodig
move(90)
time.sleep(0.5)
move(0)

