import serial
import time
nodeMcu = serial.Serial("COM10", 9600) #Sartup en kijk goed na welke poort
#Bij opstart gaat servo automatisch naar 90!

def move(angle):
    nodeMcu.write(str(angle).encode())

time.sleep(2.5) #Arduino heeft tijd nodig om connectie te maken
move(90)
time.sleep(2.5)
move(0)
#time.sleep(2.5) #Tijd tussen commands nodig
#move(120)
#time.sleep(2.5)
#move(180)

