import cv2

#print("Before URL")
cap = cv2.VideoCapture('rtsp://admin:123456@192.168.1.216/H264?ch=1&subtype=0')
#print("After URL")

while True:

    #print('About to start the Read command')
    ret, frame = cap.read()
    #print('About to show frame of Video.')
    cv2.imshow("Capturing",frame)
    #print('Running..')

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

###

#import cv2, time

#cap = cv2.VideoCapture("rtsp://admin:admin@192.168.1.30:554/11")

#time.sleep(2)

#while (True):

    #ret, frame = cap.read()
    #print
    #ret
    #if ret == 1:
        #cv2.imshow('frame', frame)
    #else:
        #print
        #"no video"
    #if cv2.waitKey(1) & 0xFF == ord('q'):
        #break

#cap.release()
#cv2.destroyAllWindows()
