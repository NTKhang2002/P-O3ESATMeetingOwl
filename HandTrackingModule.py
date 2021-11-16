import cv2
import mediapipe as mp
import time


class handDetector():
    #initialisatie
    def __init__(self,mode = False,maxHands = 2, detectionCon = 0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.detectionCon,self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    #detectie
    def findHands (self, img, draw = True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # convert it to rgb because object 'hands' only uses rgb-images
        self.results = self.hands.process(imgRGB)  # there is a method in object 'hands'
        # that will process the frame for us and give us the result
        # print(results.multi_hand_landmarks)
        if self.results.multi_hand_landmarks:  # ~if results.multi_hand_landmarks == True
            for handLms in self.results.multi_hand_landmarks:  # extract info of each hand
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)  # drawing points
        return img
    def findPosition(self,img,handNo = 0, draw =True):
        lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]

            for id, lm in enumerate( myHand.landmark):  # enumerate geeft een tupel van een voorwerp in een lijst met zijn index
                # ('index','voorwerp')
                # print(id,lm) #geeft index en positie (x,y,z in decimale getallen) van de herkenningspunten
                hight, width, channel = img.shape
                cx, cy = int(lm.x * width), int(lm.y * hight)
                #print(id, cx, cy)
                lmList.append([id,cx,cy])
                #if id == 0:
                if draw:
                    cv2.circle(img, (cx, cy), 3, (255, 0, 255), cv2.FILLED)  # puntje kleuren
        return lmList






def main():
    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(0)
    detector = handDetector()
    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        lmList = detector.findPosition(img)
        if len(lmList) != 0:
            print(lmList[4])
        cTime = time.time()  # current time
        fps = 1 / (cTime - pTime)  # frame per second
        pTime = cTime
        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
        # (beeld,tekst,positie,tekststijl,grootte,kleur,dikte)


        cv2.imshow("image", img)
        cv2.waitKey(1)


if __name__ == "__main__": #if we are running this script
    main()
