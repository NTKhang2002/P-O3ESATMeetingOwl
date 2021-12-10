import cv2
from hand_positie import HandDetector

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

def hand_status(detector, hands):
    h = []
    status_alle_handen = []
    if hands: #als er (een) hand(en) (is) zijn
        for id in range(len(hands)):
            hand = hands[id]
            cx, cy = hand["center"]  # centerpoint: cx cy
            fingers = detector.fingersUp(hand)
            h.append(cx)
            positie = detector.voorkant_hand(hand)
            if fingers == [1,1,1,1,1] or fingers == [0,1,1,1,1]: #als alle vingers van een hand (uitgezonderd duim) zijn opgestoken
                if positie == True:
                    status_alle_handen.append(True)
                else:
                    status_alle_handen.append(False)
            else:
                status_alle_handen.append(False)
        return h, status_alle_handen #h = lijst met xcoord van alle handen, status_alle_handen = lijst met voor alle handen True of False
                                     # False voor als de hand niet opgestoken is, True voor als de hand opgestoken is
    else: #als er geen hand is
        return h, status_alle_handen #lege lijsten



def koppelen(xhanden, xgezichten):
    gekoppeld = []
    for i in range(len(xhanden)):
        min_afstand = 10000000000000000
        index = 0
        for xgezicht in xgezichten:
            afstand = abs(xhanden[i] - xgezicht)
            if afstand <= min_afstand:
                min_afstand = afstand
                juiste_gezicht = index
                index += 1
            else:
                index += 1
        ok = (xhanden[i], xgezichten[juiste_gezicht])
        gekoppeld.append(ok)
    return gekoppeld #geeft een lijst met tuples (xhanden, xgezichten)

def xhand_en_status(xhanden,status_handen):
    xcoord_en_status = []
    if len(xhanden) != 0:
        for index in range(len(xhanden)):
            xcoord_en_status.append((xhanden[index], status_handen[index]))
    else:
        xcoord_en_status.append((None,None)) #als er geen handen zijn
    return xcoord_en_status


def x_periode(lijst):
    standaard_xco = []
    een_frame = []
    for frame in lijst:
        if (None,None) in frame:
            standaard_xco =[]
            return standaard_xco
        else:
            for hand_id in range(len(frame)):
                if frame[hand_id][1] == True:
                    een_frame.append(frame[hand_id][0])
                if hand_id == len(frame)-1:
                    standaard_xco.append(een_frame)
                    een_frame = []
    return standaard_xco

def gemiddelde_xco(lijst):
    if len(lijst) == 0:
        pass
    else:
        xhanden = []
        for frame_id in range(len(lijst)):
            if lijst[frame_id] == []:
                pass
            else:
                for hand in lijst[frame_id]:
                    if frame_id == 0:
                        xhanden.append([hand,1])
                    else:
                        checker = 0 #een opgestoken hand komt in de periode te voorschijn, cheker checkt of die hand al geregistreerd staat
                        for l in xhanden:
                            if abs(l[0]-hand) <= (5 * len(lijst)): #we nemen een verhouding van 5pixels/frame
                                l[0] = (l[0]+hand)/2
                                l[1] += 1
                            else:
                                checker += 1
                        if checker == len(xhanden):
                            xhanden.append([hand,1])
        return xhanden #geeft een lijst terug met de gemiddelde xcoord van de opgestoken handen en hoe vaak de hand is gedetecteerd in die periode
                       #bv [[5.2, 10],[10.6, 5]]
                       # [5.2, 10] = [xcoord hand1, van het totaal aantel frames is deze hand 10 keer gedetecteerd]

def xco_resultaat(gemiddelde_lijst,gegevens_periode):
    if gemiddelde_lijst == None:
        print('geen handen')
        return []
    elif gemiddelde_lijst == []:
        print('geen opgestoken handen')
        return []
    else:
        xco_result = []
        aantal_frames_in_periode = len(gegevens_periode)
        for ghand in gemiddelde_lijst:
            if (ghand[1]/aantal_frames_in_periode) >= 0.9: #als de hand in meer dan 90% van de frames wordt gedetecteerd
                for handje in gegevens_periode[-1]:
                    if abs(handje[0]-ghand[0]) <= (5*len(gegevens_periode)):
                        xco_result.append(handje[0])
        if xco_result == []:
            print('steek je hand wat langer op')
            return xco_result
        return xco_result

"""
buiten de functies zijn er ook delen die in de main moeten staan
ik heb ze tussen twee comments gezet
"""

def main(detectionCon = 0.8, maxHands = 4):
    # Camera preparation
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cap.set(50,1000)
    cap.set(40,100)
    # Initializing HandDetector module
    detector = HandDetector(detectionCon=detectionCon, maxHands=maxHands)

    #dit stuk hieronder kopieren:
    gedetecteerd = []
    #tot hier (er is nog vanonder)

    while True:
        success, img = cap.read()
        hands, img = detector.findHands(img)

        #dit dtuk kopieren:
        handcoord, status = hand_status(detector, hands) # handcoord = lijst met xcoord van alle handen, status = lijst met True an False
        xco_status = xhand_en_status(handcoord,status)
        #tot hier (er is nog)

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        xgezicht = []
        if len(faces) != 0:
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 0), 2)
                xgezicht.append((x + w) / 2)
        else:
            # return face
            pass

        #vanaf hier:
        gedetecteerd.append(xco_status)
        if len(gedetecteerd) == 10:
            # gqedetecteerd is een lijst van frames, elke frame is ook een lijst
            # in de lijst van de frame zitten tuples (de tuples stellen handen voor die
            # in dat frame voorkomen): (xcoord hand, True of False) of indien er geen handen zijn gwn: (None,None)
            # er is gekozen om per 10 frames te detecteren, maar dat kan nog gewijzigd worden
            gem = gemiddelde_xco(x_periode(gedetecteerd)) #lijst van gemiddelde xcoord van opgestoken handen
            xhanden = xco_resultaat(gem,gedetecteerd)
            if len(xhanden) != 0 and len(xgezicht) != 0:
                resultaat = koppelen(xhanden,xgezicht)
                print(resultaat)
            gedetecteerd = []
        #tot hier (dat was het)

        cv2.imshow("image", img)
        if cv2.waitKey(1) == ord('q'):
            break

main()