import cv2
import time
# creating a variable with the classifiers
CLASSIFIERS = "haarcascade_frontalface_default.xml"
# Create cascade
FaceCascade = cv2.CascadeClassifier(CLASSIFIERS)
# Creates a video object that takes the image of the webcam
cap = cv2.VideoCapture(0)

def coordinaatgezicht(faces, face):
    if faces != () and len(faces) >= face + 1:
        X = faces[face][0]
        Y = faces[face][1]
        W = faces[face][2]
        H = faces[face][3]

        return X,Y,W,H

def mostcentralface(width,faces):
    if faces != ():
        centerpoint = int(width/2)
        xlijst = list()
        for face in range(len(faces)):
            xlijst.append(int(abs(centerpoint - faces[face][0])))
        return xlijst.index(min(xlijst))
    return 0



while True:
    status, img = cap.read()

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Detect the faces
    faces = FaceCascade.detectMultiScale(gray, scaleFactor=1.22, minNeighbors=8, minSize=(60,60))
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

    print(type(faces))
    print(mostcentralface(img,faces))

    cv2.imshow("beeld",img)

    toets = cv2.waitKey(1)
    if toets == 32:
        print(type(img))
        print(img)
        print("_______________")
    if toets == 27:
        break
cap.release()
