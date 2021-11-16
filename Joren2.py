def interpolatiepad(prevcord,nextcord,tijd):
    X1,Y1,W1,H1 = prevcord[0], prevcord[1], prevcord[2], prevcord[3]
    X2,Y2,W2,H2 = nextcord[0], nextcord[1], nextcord[2], nextcord[3]
    i = 1
    k = tijd
    interpolatielijst = list()
    for i in range(tijd):
        i += 1
        interpolatielijst.append([(k-i)/tijd * X1 + i/tijd * X2,(k-i)/tijd * Y1 + i/tijd * Y2,
                                  (k-i)/tijd * W1 + i/tijd * W2,(k-i)/tijd * H1 + i/tijd * H2])


    return interpolatielijst




cord1 = [5, 5,2, 2]
cord2 = [10, 10, 4, 4]
print(interpolatiepad(cord1,cord2,4))