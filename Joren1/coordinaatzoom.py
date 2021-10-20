import cv2

# creating a variable with the classifiers
CLASSIFIERS = "haarcascade_frontalface_default.xml"

# Create cascade
FaceCascade = cv2.CascadeClassifier(CLASSIFIERS)
# Capture from camera, 0 because webcam
cap = cv2.VideoCapture(0)



def zoom(img,faces, face=0):
    if not faces == () and len(faces) >= face + 1:
        X = faces[face][0]
        Y = faces[face][1]
        W = 210 #faces[face][2]
        H = 210 #faces[face][3]

        Ry = img.shape[0]
        Rx = img.shape[1]
        xfc = (X + W) / 2
        yfc = (Y + H) / 2
        ymin = max(min(int(((Y-3*H/2)/(3*H))*Ry)-1,Ry-1),0)
        ymax = min(max(int(((Y+3*H/2)/(3*H))*Ry),0),Ry)
        xmin = max(min(int(((X-3*W/2)/(3*W))*Rx)-1,Rx-1),0)
        xmax = min(max(int(((X+3*W/2)/(3*W))*Rx),0),Rx)
        # edge solution
        if ymin == 0:
            ymax = 2*H
        if ymax == Ry:
            ymin = Ry-2*H
        if xmin == 0:
            xmax = 2 * W
        if ymax == Rx:
            ymin = Rx - 2 * W


        print('data', [ymin, ymax, xmin, xmax])
        print(img.shape)
        imgzoom = img[ymin:ymax, xmin:xmax]
        imgresized = cv2.resize(imgzoom, (img.shape[1], img.shape[0]))
        return (imgresized, ymin, ymax, xmin, xmax)
    else:
        return (img,-1,-1,-1,-1)

while True:
    status, img = cap.read()

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Detect the faces
    faces = FaceCascade.detectMultiScale(gray, 1.1, 4)
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

    print(faces)
    cv2.imshow('beeld',zoom(img,faces,0)[0])
    cv2.imshow('origineel',img)
    toets = cv2.waitKey(1)
    if toets == 27:
        break
cap.release()



