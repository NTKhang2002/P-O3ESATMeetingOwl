import cv2

HEIGHT = 480
WIDTH = int(16/9 * HEIGHT)
face = 0
tijd = 5
interpolatielijst = list()
nextcord = [None, None, None, None]
prevcord = [None, None, None, None]
Xf, Yf, Wf, Hf = None, None, None, None


# creating a variable with the classifiers
CLASSIFIERS = "haarcascade_frontalface_default.xml"

# Create cascade
FaceCascade = cv2.CascadeClassifier(CLASSIFIERS)
# Capture from camera, 0 because webcam
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
cap.set(cv2.CAP_PROP_FRAME_WIDTH,  WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)


#sets the variables xmin, xmax etc. to the standard value of the image.

xmin, xmax, ymin, ymax = 0, WIDTH, 0, HEIGHT


def zoomboundaries(img,X, Y, W, H):
    """X = faces[face][0]
    Y = faces[face][1]
    W = faces[face][2]
    H = faces[face][3]"""
    H = 209
    W = 209

    Ry = img.shape[0]
    Rx = img.shape[1]
    V = Rx / Ry

    xfc = X + W / 2
    yfc = Y + H / 2

    ymin = max(min(int(yfc - H), int(Ry - 2 * H)), 0)
    ymax = max(min(int(yfc + H), Ry), int(2 * H))
    xmin = max(min(int(xfc - V * H), int(Rx - V * 2 * H)), 0)
    xmax = max(min(int(xfc + V * H), Rx), int(V * 2 * H))
    return xmin,xmax,ymin,ymax

def crop(img,xmin,xmax,ymin,ymax):
    imgcropped = img[ymin:ymax, xmin:xmax]
    return imgcropped

def resizer(img, Width, Height):
    imgresized = cv2.resize(img,(Width,Height))
    return imgresized

def coordinaatgezicht(faces, face):
    if faces != () and len(faces) >= face + 1:
        X = faces[face][0]
        Y = faces[face][1]
        W = faces[face][2]
        H = faces[face][3]

        return X,Y,W,H
    return None,None,None,None


def interpolatiepad(prevcord, nextcord, tijd):
    X1, Y1, W1, H1 = prevcord[0], prevcord[1], prevcord[2], prevcord[3]
    X2, Y2, W2, H2 = nextcord[0], nextcord[1], nextcord[2], nextcord[3]
    k = tijd
    interpolatielijst = list()
    for i in range(tijd):
        i += 1
        interpolatielijst.append([int((k - i) / tijd * X1 + i / tijd * X2), int((k - i) / tijd * Y1 + i / tijd * Y2),
                                  int((k - i) / tijd * W1 + i / tijd * W2), int((k - i) / tijd * H1 + i / tijd * H2)])
    return interpolatielijst



i = 0
while True:
    status, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Detect the faces
    faces = FaceCascade.detectMultiScale(gray, scaleFactor=1.22, minNeighbors=8, minSize=(60, 60))
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

    if list(coordinaatgezicht(faces,face)) != [None,None,None,None]:
        nextcord = list(coordinaatgezicht(faces,face))

    if i % tijd == 0:
        if prevcord != [None, None, None, None]:
            interpolatielijst = interpolatiepad(prevcord,nextcord,tijd)
        prevcord = nextcord


    if i % tijd != 0 and interpolatielijst != list():
        Xf, Yf, Wf, Hf = int(interpolatielijst[i%tijd][0]), int(interpolatielijst[i%tijd][1]), \
                         int(interpolatielijst[i%tijd][2]), int(interpolatielijst[i%tijd][3])
        print(Xf, Yf, Wf, Hf)
    else: Xf, Yf, Wf, Hf = [nextcord[0], nextcord[1], nextcord[2], nextcord[3]]


    if faces != () and len(faces) >= face + 1 and Xf != None:

        (xmin, xmax, ymin, ymax) = zoomboundaries(img, Xf,Yf,Wf,Hf)

    imgcropped = crop(img,xmin,xmax,ymin,ymax)
    imgresized = resizer(imgcropped,WIDTH,HEIGHT)

    cv2.imshow("zoomed",imgresized)
    cv2.imshow("origineel",img)
    toets = cv2.waitKey(10)
    if toets == 32:
        xmin = 0
        xmax = WIDTH
        ymin = 0
        ymax = HEIGHT

    if toets == 27:
        break
    i+=1

cap.release()