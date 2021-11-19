import cv2

HEIGHT = 720
WIDTH = int(16 / 9 * HEIGHT)
MIDDLEPOINTX = int(WIDTH/2)
MIDDLEPOINTY = int(HEIGHT/2)
tijd = 15
schaal = 1.3
interpolatielijst = [0]*tijd
# 1/2 for full screen[|---------------------|] , 1/4 to use only the middle part [-----|----------|-----]
Central_bounding = int(1/2 * WIDTH)

# creating a variable with the classifiers
CLASSIFIERS = "haarcascade_frontalface_default.xml"

# Create cascade
FaceCascade = cv2.CascadeClassifier(CLASSIFIERS)
# Capture from camera, 0 because webcam
cap = cv2.VideoCapture(1)
cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
cap.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)

# sets the variables xmin, xmax etc. to the standard value of the image.
Xf, Yf, Wf, Hf = MIDDLEPOINTX, MIDDLEPOINTY, MIDDLEPOINTX, MIDDLEPOINTY
xmin, xmax, ymin, ymax = 0, WIDTH, 0, HEIGHT


def zoomboundaries(img , X, Y, W, H,Scalar):
    Ry = img.shape[0]
    Rx = img.shape[1]
    V = Rx / Ry

    xfc = X + W / 2
    yfc = Y + H / 2

    ymin = max(min(int(yfc - Scalar*H), int(Ry - 2 * Scalar*H)), 0)
    ymax = max(min(int(yfc + Scalar*H), Ry), int(2 * Scalar*H))
    xmin = max(min(int(xfc - V * Scalar * H), int(Rx - V * 2 * Scalar * H)), 0)
    xmax = max(min(int(xfc + V * Scalar * H), Rx), int(V * 2 * Scalar * H))
    return xmin, xmax, ymin, ymax

def crop(img, xmin, xmax, ymin, ymax):
    imgcropped = img[ymin:ymax, xmin:xmax]
    return imgcropped

def resizer(img, Width, Height):
    imgresized = cv2.resize(img, (Width, Height))
    return imgresized

def coordinaatgezicht(faces, face):
    X = faces[face][0]
    Y = faces[face][1]
    W = faces[face][2]
    H = faces[face][3]

    return X, Y, W, H

def gemiddeldelijst(lijst, positie):
    som = 0
    n = len(lijst)
    for i in range(n):
        som += lijst[i][positie]
    return int(som/n)

def mostcentralface(width,faces):
    if faces != ():
        centerpoint = int(width/2)
        xlijst = list()
        for face in range(len(faces)):
            xlijst.append(int(abs(centerpoint - (faces[face][0]+faces[face][2]/2))))
        minx = min(xlijst)
        if minx <= Central_bounding:
            return xlijst.index(minx)
    return False

i = 0
while True:
    status, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Detect the faces
    faces = FaceCascade.detectMultiScale(gray, scaleFactor=1.22, minNeighbors=8, minSize=(60, 60))
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
    #bounding box that represents the part of the image it tracks faces in.
    cv2.rectangle(img, (int(WIDTH/2) - Central_bounding,0),(int(WIDTH/2)+Central_bounding,HEIGHT),(255,255,255),2)
    face = mostcentralface(WIDTH,faces)


    if face is not False:
        if faces != () and len(faces) >= face + 1:
            Xf, Yf, Wf, Hf = coordinaatgezicht(faces, face)

    interpolatielijst[i % tijd] = [Xf, Yf, Wf, Hf]

    if face is not False:
        if i > tijd:
            Xf = gemiddeldelijst(interpolatielijst,0)
            Yf = gemiddeldelijst(interpolatielijst,1)
            Wf = gemiddeldelijst(interpolatielijst,2)
            Hf = gemiddeldelijst(interpolatielijst,3)

        if faces != () and len(faces) >= face + 1:
            (xmin, xmax, ymin, ymax) = zoomboundaries(img, Xf, Yf, Wf, Hf,schaal)

    imgcropped = crop(img, xmin, xmax, ymin, ymax)
    imgresized = resizer(imgcropped, WIDTH, HEIGHT)

    cv2.imshow("zoomed", imgresized)
    cv2.imshow("origineel", img)
    toets = cv2.waitKey(10)
    if toets == 32:
        xmin = 0
        xmax = WIDTH
        ymin = 0
        ymax = HEIGHT

    if toets == 27:
        break
    i += 1

cap.release()