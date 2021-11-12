import cv2


from cvzone.HandTrackingModule import HandDetector
#1)
cap = cv2.VideoCapture(0)
#2)
detector = HandDetector(detectionCon=0.8, maxHands=2)
#1)
while True:
    success, img = cap.read()
    #2)
    hands, img = detector.findHands(img) #with draw
    # hands = detector.findHands(img,draw = False)  No drawing
    if hands:
        hand1 = hands[0]
        lmList1 = hand1["lmList"]  # lijst van 21 handpunten
        bbox1 = hand1["bbox"]  # bounding box x,y,w,h
        centerPoint1 = hand1["center"]  # centrum van de hand cx,cy
        handType1 = hand1["type"]  # handtype links of rechts
        print(centerPoint1)

        fingers1 = detector.fingersUp(hand1)
        length, info, img = detector.findDistance(lmList1[8], lmList1[12], img)

        if len(hands) == 2:
            hand2 = hands[1]
            lmList2 = hand2["lmList"]  # lijst van 21 handpunten
            bbox2 = hand2["bbox"]  # bounding box x,y,w,h
            centerPoint2 = hand2["center"]  # centrum van de hand cx,cy
            handType2 = hand2["type"]  # handtype links of rechts
            fingers2 = detector.fingersUp(hand2)
            length, info, img = detector.findDistance(lmList1[8], lmList2[8], img)

    cv2.imshow("image", img)
    cv2.waitKey(1)

#1) dit was om de camera aan te zetten
