import serial
import time
import math




def move(x,x_oud,nodeMcu,straal,helft_pixels):
    print("x: " + str(x))
    print("x_oud: " + str(x_oud))
    if x != None:
<<<<<<< HEAD

        if abs(x_oud - x) > 150:
            x_oud = x
=======
        if abs(x_oud - x) > 150:
>>>>>>> a333fa258d49aeaeadd8bb0980b65ec9faa89e01
            if x > helft_pixels:
                x = x-helft_pixels
                angle = 90 - (math.sin(x / straal))*180/3.14
            elif x < helft_pixels:
                x = helft_pixels - x
                angle = 90 + (math.sin(x / straal))*180/3.14
            elif x == helft_pixels:
                angle = 90
            print(angle)
            print(math.sin(x / straal)*180/3.14)
<<<<<<< HEAD

=======
            x_oud = x
>>>>>>> a333fa258d49aeaeadd8bb0980b65ec9faa89e01

            nodeMcu.write(str(angle).encode())
    return x_oud

def main():
    nodeMcu = serial.Serial("COM10", 9600)  # Sartup
    straal = 694
    max_aantal_pixels = 1080
    helft_pixels = max_aantal_pixels / 2
    x_oud = 5000
    while True:
        x = int(input("Geef x:"))
        x_oud = move(x,x_oud,nodeMcu,straal,helft_pixels)

if __name__ == '__main__':
    main()

#time.sleep(2) #Arduino heeft tijd nodig om connectie te maken
#move(180)
#time.sleep(1) #Tijd tussen commands nodig
#move(90)
#time.sleep(0.5)
#move(0)

