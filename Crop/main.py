import cv2

cap = cv2.VideoCapture('a.avi')
out = cv2.VideoWriter('output.avi', 0x21, 15.0, (853,524))

while cap.isOpened():

    ret, frame = cap.read()
    if ret == True:
        crop_img = frame[60:584,13:866]

        cv2.imshow('frame',crop_img)

        out.write(crop_img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break
# When everything done, release the capture
cap.release()
out.release()
cv2.destroyAllWindows()