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
        W = 209 #faces[face][2]
        H = 209 #faces[face][3]

        xfc = (X + W)/2
        yfc = (Y + H)/2


        imgzoom = img[max(Y - int(3*(H)/2),0):min(Y + int(3*H/2),img.shape[0]),
                  max(X - int(3*W/2),0):min(X + int(3*W/2),img.shape[1])]
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
        pt2x = int(x+w+5)
        pt2y = int(y+h+5)
        cv2.rectangle(img, (x+w, y+h), (pt2x, pt2y), (255, 0, 0), 2)
        cv2.rectangle(img, (x , y), (x+w, y+h), (0, 0, 255), 2)
    print(faces)
    cv2.imshow('zoom',zoom(img,faces,0))
    cv2.imshow('beeld',img)
    toets = cv2.waitKey(20)
    if toets == 27:
        break
cap.release()


