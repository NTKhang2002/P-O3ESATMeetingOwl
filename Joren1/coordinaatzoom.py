import cv2

# creating a variable with the classifiers
CLASSIFIERS = "haarcascade_frontalface_default.xml"

# Create cascade
FaceCascade = cv2.CascadeClassifier(CLASSIFIERS)
# Capture from camera, 0 because webcam
cap = cv2.VideoCapture(0)



def zoom(img,faces, face=0):
    if not faces == ():
        X = faces[face][0]
        Y = faces[face][1]
        W = faces[face][2]
        H = faces[face][3]

        Ry = img.shape[0]
        Rx = img.shape[1]

        ymin = max(min(int(((Y-3*H/2)/(3*H))*Ry),Ry),0)
        ymax = min(max(int(((Y+3*H/2)/(3*H))*Ry),0),Ry)
        xmin = max(min(int(((X-3*W/2)/(3*W))*Rx),Rx),0)
        xmax = min(max(int(((X+3*W/2)/(3*W))*Rx),0),Rx)
        print('data',[ymin, ymax, xmin,xmax])
        imgzoom = img[ymin:ymax,xmin:xmax]
        imgresized = cv2.resize(imgzoom,(img.shape[1],img.shape[0]))
        return imgresized
    else:
        return img

while True:
    status, img = cap.read()

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Detect the faces
    faces = FaceCascade.detectMultiScale(gray, 1.1, 4)
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
    print(faces)
    cv2.imshow('beeld',zoom(img,faces,0))

    toets = cv2.waitKey(1)
    if toets == 27:
        break
cap.release()



