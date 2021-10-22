import cv2


# creating a variable with the classifiers
CLASSIFIERS = "haarcascade_frontalface_default.xml"

# Create cascade
FaceCascade = cv2.CascadeClassifier(CLASSIFIERS)
# Capture from camera, 0 because webcam
cap = cv2.VideoCapture(1)



def zoom(img,faces, face=0):
    if not faces == () and len(faces) >= face + 1:
        X = faces[face][0]
        Y = faces[face][1]
        W = faces[face][2]
        H = faces[face][3]

        Ry = img.shape[0]
        Rx = img.shape[1]
        V = Rx/Ry

        xfc = X + W/2
        yfc = Y + H/2

        ymin = max(min(int(yfc-H)-1,int(Ry-2*H)),0)
        ymax = max(min(int(yfc+H),Ry),int(2*H))
        xmin = max(min(int(xfc-V*H)-1,int(Rx-V*2*H)),0)
        xmax = max(min(int(xfc+V*H),Rx),int(V*2*H))


        cv2.rectangle(img,(int(xfc),int(yfc)),(int(xfc+5),int(yfc+5)),(255,255,255),2)
        print(faces)
        print('data', ["ymin =",ymin, "ymax=",ymax,"xmin=", xmin,"xmax=", xmax, "xfc=",xfc,"yfc=", yfc])
        print(img.shape)
        imgzoom = img[ymin:ymax, xmin:xmax]

        imgresized = cv2.resize(imgzoom, (img.shape[1], img.shape[0]))
        cv2.rectangle(img,(int(xmin),int(ymin)),(int(xmax),int(ymax)),(0,255,0),2)
        return imgresized
    else:
        return img

while True:
    status, img = cap.read()

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Detect the faces
    faces = FaceCascade.detectMultiScale(gray, scaleFactor=1.22, minNeighbors=8, minSize=(60,60))
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)


    cv2.imshow('beeld',zoom(img,faces,0))
    cv2.imshow('origineel',img)
    toets = cv2.waitKey(1)
    if toets == 27:
        break
cap.release()



