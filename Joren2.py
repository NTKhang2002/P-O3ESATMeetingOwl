from time import sleep

interpolatielijst = [[11,12,13,14],[21,22,23,24],[31,32],[4],[5]]
tijd = 5


def interpolatiepad(prevcord,nextcord,tijd):
    X1,Y1,W1,H1 = prevcord[0], prevcord[1], prevcord[2], prevcord[3]
    X2,Y2,W2,H2 = nextcord[0], nextcord[1], nextcord[2], nextcord[3]
    k = tijd
    interpolatielijst = list()
    for i in range(tijd):
        i += 1
        interpolatielijst.append([int((k-i)/tijd * X1 + i/tijd * X2),int((k-i)/tijd * Y1 + i/tijd * Y2),
                                  int((k-i)/tijd * W1 + i/tijd * W2),int((k-i)/tijd * H1 + i/tijd * H2)])


    return interpolatielijst
def coordinaatgezicht(faces, face):
    if faces != () and len(faces) >= face + 1:
        X = faces[face][0]
        Y = faces[face][1]
        W = faces[face][2]
        H = faces[face][3]

        return X,Y,W,H
    else:
        return None,None,None,None

cord1 = [5, 5, 2, 2]
cord2 = [10,10,4,4]
print(interpolatiepad(cord1,cord2,5))

"""i = 0
while True:
    if i % tijd != 0 and interpolatielijst != None:
        Xf, Yf, Wf, Hf = int(interpolatielijst[i - (i // tijd) - 1][0]), int(interpolatielijst[i - (i // tijd) - 1][1]), \
                         int(interpolatielijst[i - (i // tijd) - 1][2]), int(interpolatielijst[i - (i // tijd) - 1][3])
        print(Xf, Yf, Wf, Hf)

    i += 1"""

i = 0
while True:
    print((i % tijd))
    i+=1
    sleep(0.5)



