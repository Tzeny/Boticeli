import cv2
import numpy as np

car_cascade = [cv2.CascadeClassifier('test.xml'), cv2.CascadeClassifier('cas2.xml'), cv2.CascadeClassifier('cas1.xml'), cv2.CascadeClassifier('cas3.xml'), cv2.CascadeClassifier('cas4.xml')]
colors = [(0,255,0),(255,0,0),(0,0,255),(0,0,0),(255,255,255)]

cap = cv2.VideoCapture('inter3.avi')

points = [(0,0)]

wid = 1280
hei = 698

points = np.array([(50,225),(900,160),(1280,250),(1280,360),(244,650)])



def checkX(origX):
    if origX < 0:
        return 0
    elif origX > wid:
        return wid
    else:
        return origX

def checkY(origY):
    if origY < 0:
        return 0
    elif origY > hei:
        return hei
    else:
        return origY

while cap.isOpened():

    ret, frame = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    cars = car_cascade[0].detectMultiScale(gray, 1.1, 3)

    for i in range(0, len(points)):
        cv2.line(frame,(points[i][0],points[i][1]),(points[(i+1)%len(points)][0],points[(i+1)%len(points)][1]),(255,0,0),10)

    for (x, y, w, h) in cars:
        center = (x+w/2,y+h/2)

        area = w * h;

        if area<5000:
            continue

        if cv2.pointPolygonTest(points, center, False) >= 0:
            cv2.rectangle(frame, (x, y), (x + w, y + h), colors[0], 2)
            cv2.circle(frame, center, 10, (255,0,0))

        # const = 100;
        #
        # a = checkY(y-const)
        # b = checkY(y+h+const)
        # c = checkX(x-const)
        # d = checkX(x+const)

        #print str(a)+";"+str(b)+";"+str(c)+";"+str(d)

        # img = gray[a:b, c:d]
        #
        # cv2.imshow('frame2',img)
        # cv2.moveWindow('frame2',1500,500)
        #
        # cars2 = car_cascade[1].detectMultiScale(img, 1.3, 1)
        # for (x2, y2, w2, h2) in cars2:
        #     cv2.rectangle(frame, (x2, y2), (x2 + w2, y2 + h2), colors[1], 2)

    cv2.imshow('frame',frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()