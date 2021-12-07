import serial
import time
import math




def move(x,x_oud,nodeMcu,straal,helft_pixels):
    if x != None and isinstance(x, str) == False:
        if abs(x_oud - x) > 75:
            x_oud = x
            if x > helft_pixels:
                x = x-helft_pixels
                angle = 90 - (math.sin(x / straal))*180/3.14
            elif x < helft_pixels:
                x = helft_pixels - x
                angle = 90 + (math.sin(x / straal))*180/3.14
            elif x == helft_pixels:
                angle = 90
            nodeMcu.write(str(angle).encode())
    return x_oud

