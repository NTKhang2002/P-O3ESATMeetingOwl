import cv2
import pyvirtualcam

def zoomboundaries(img , X, Y, W, H, Scalar):
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

def mostcentralface(width,faces,Central_bounding):
    if len(faces) != 0 :
        centerpoint = int(width/2)
        xlijst = list()
        for face in range(len(faces)):
            xlijst.append(int(abs(centerpoint - (faces[face][0]+faces[face][2]/2))))
        minx = min(xlijst)
        if minx <= Central_bounding:
            return xlijst.index(minx)
    return False

def coordinaatzoomfunctie(camera=0):
    HEIGHT = 480
    WIDTH = int(16 / 9 * HEIGHT)
    MIDDLEPOINTX = int(WIDTH / 2)
    MIDDLEPOINTY = int(HEIGHT / 2)
    tijd = 17
    schaal = 1.4
    interpolatielijst = [[MIDDLEPOINTX, MIDDLEPOINTY, MIDDLEPOINTX, MIDDLEPOINTY]] * tijd
    Camlock = False
    # 1/2 for full screen[|---------------------|] , 1/4 to use only the middle part [-----|----------|-----]
    Central_bounding = int(1 / 6 * WIDTH)

    # creating a variable with the classifiers
    CLASSIFIERS = "haarcascade_frontalface_default.xml"

    # Create cascade
    FaceCascade = cv2.CascadeClassifier(CLASSIFIERS)
    # Capture from camera, 0 because webcam
    capzoom = cv2.VideoCapture(camera,cv2.CAP_DSHOW)
    capzoom.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
    capzoom.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
    capzoom.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)

    # sets the variables xmin, xmax etc. to the standard value of the image.
    Xf, Yf, Wf, Hf = MIDDLEPOINTX, MIDDLEPOINTY, MIDDLEPOINTX, MIDDLEPOINTY
    xmin, xmax, ymin, ymax = 0, WIDTH, 0, HEIGHT
    i = 0
    with pyvirtualcam.Camera(width=WIDTH, height=HEIGHT, fps=30) as cam:
        while True:
            status, imgzoom = capzoom.read()
            gray = cv2.cvtColor(imgzoom, cv2.COLOR_BGR2GRAY)
            # Detect the faces
            faces = FaceCascade.detectMultiScale(gray, scaleFactor=1.22, minNeighbors=8, minSize=(60, 60))
            """for (x, y, w, h) in faces:
                cv2.rectangle(imgzoom, (x, y), (x + w, y + h), (255, 0, 0), 2)"""
            #bounding box that represents the part of the image it tracks faces in.
            #cv2.rectangle(imgzoom, (int(WIDTH/2) - Central_bounding,0),(int(WIDTH/2)+Central_bounding,HEIGHT),(255,255,255),2)
            face = mostcentralface(WIDTH,faces,Central_bounding)


            if face is not False:
                if len(faces) != 0  and len(faces) >= face + 1:
                    Xf, Yf, Wf, Hf = coordinaatgezicht(faces, face)

            interpolatielijst[i % tijd] = [Xf, Yf, Wf, Hf]

            if face is not False:
                Xf = gemiddeldelijst(interpolatielijst,0)
                Yf = gemiddeldelijst(interpolatielijst,1)
                Wf = gemiddeldelijst(interpolatielijst,2)
                Hf = gemiddeldelijst(interpolatielijst,3)

                if len(faces) != 0  and len(faces) >= face + 1:
                    (xmin, xmax, ymin, ymax) = zoomboundaries(imgzoom, Xf, Yf, Wf, Hf,schaal)

            if Camlock == True:
                xmin = 0
                xmax = WIDTH
                ymin = 0
                ymax = HEIGHT

            imgcropped = crop(imgzoom, xmin, xmax, ymin, ymax)
            imgresized = resizer(imgcropped, WIDTH, HEIGHT)

            cv2.imshow("zoomed", imgresized)
            # cv2.imshow("origineel", imgzoom)
            imgresized = cv2.cvtColor(imgresized, cv2.COLOR_BGR2RGB)
            imgresized = cv2.flip(imgresized, 1)
            cam.send(imgresized)
            cam.sleep_until_next_frame()
            toets = cv2.waitKey(10)
            if toets == 32:
                if Camlock == False:
                    Camlock = True
                else:
                    Camlock = False

            if toets == 27:
                break
            i += 1

        capzoom.release()

