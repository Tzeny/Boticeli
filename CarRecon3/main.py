import cv2
import numpy as np

#used to use multiple cascades
car_cascade = [cv2.CascadeClassifier('test.xml')]
colors = [(0,255,0)]

#open video
cap = cv2.VideoCapture('inter3.avi')

#dimensions of video
wid = 1280
hei = 698

#defines our intersection
points = np.array([(50,225),(900,160),(1280,250),(1280,360),(244,650)])

id = 0

v_points = {}

#check if x is within the image
def checkX(origX):
    if origX < 0:
        return 0
    elif origX > wid:
        return wid
    else:
        return origX

#check if y is within the image
def checkY(origY):
    if origY < 0:
        return 0
    elif origY > hei:
        return hei
    else:
        return origY

def distance((a1,b1),(a2,b2)):
    return np.sqrt(np.power(a1-a2,2)+np.power(b1-b2,2))

#main loop
while cap.isOpened():

    #image aquisition and cascade detection
    ret, frame = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    cars = car_cascade[0].detectMultiScale(gray, 1.1, 3)

    current_points = list()

    #detect cascades and display them
    for i in range(0, len(points)):
        cv2.line(frame,(points[i][0],points[i][1]),(points[(i+1)%len(points)][0],points[(i+1)%len(points)][1]),(255,0,0),10)

    for (x, y, w, h) in cars:
        center = (x+w/2,y+h/2)

        area = w * h;

        if area<5000:
            continue

        if cv2.pointPolygonTest(points, center, False) >= 0:
            current_points.append(center)
            cv2.rectangle(frame, (x, y), (x + w, y + h), colors[0], 2)
            cv2.circle(frame, center, 10, (255,0,0))

    #go through list of identified cascades
    for (x,y) in current_points:
        found = False
        min = 99999
        min_id = 0;
        min_point = (x,y)

        for i,(m,n) in v_points.iteritems():
            dist = distance((x,y),(m,n))
            print "Dist from "+str(i)+"to current position: "+str(x)+","+str(y)
            if dist < 300 and dist < min:
                min = dist
                found = True
                min_id = i
                min_point = (x,y)

        if found:
            print "Moving point "+str(min_id)+"to coords"+str(min_point[0])+","+str(min_point[1])
            v_points[min_id] = min_point
        else:
            v_points[id] = min_point
            id = id +1

    for i,(x,y) in v_points.iteritems():
        cv2.circle(frame, (x,y), 25, (255,255,255))
        cv2.putText(frame, str(i), (x,y), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 1, (255, 255, 255), 2)

    cv2.imshow('frame',frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()