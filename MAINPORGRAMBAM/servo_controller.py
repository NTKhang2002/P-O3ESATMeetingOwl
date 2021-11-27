import serial
import time
import math




def move(x,x_oud,nodeMcu,straal,helft_pixels):
    if x != None:
        if abs(x_oud - x) > 75:
            if x > helft_pixels:
                x = x-helft_pixels
                angle = 90 - (math.sin(x / straal))*180/3.14
            elif x < helft_pixels:
                x = helft_pixels - x
                angle = 90 + (math.sin(x / straal))*180/3.14
            elif x == helft_pixels:
                angle = 90
            x_oud = x
            nodeMcu.write(str(angle).encode())
    return x_oud

