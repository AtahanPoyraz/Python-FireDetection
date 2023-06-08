import cv2
import numpy as np
import datetime as dt

STATUS = False

cam = cv2.VideoCapture(0)
now = dt.datetime.now()
night = dt.datetime(now.year, now.month, now.day, 20, 0, 0)

while cam.isOpened():
    ret, frame = cam.read()
    frame = cv2.resize(frame, (1000, 600))
    blur = cv2.GaussianBlur(frame, (21, 21), 0)
    tespit = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
    lower = [18, 50, 50]
    upper = [35, 255, 255]
    lower = np.array(lower, dtype="uint8")
    upper = np.array(upper, dtype="uint8")
    mask = cv2.inRange(tespit, lower, upper)
    output = cv2.bitwise_and(frame, tespit, mask=mask)

    number = cv2.countNonZero(mask)
    #print(number)
    if now <= night:
        if 800 < number < 2200:
            STATUS = True
        else:
            STATUS = False

    if now >= night:
        if number < 3000:
            STATUS = True
        else:
            STATUS = False
            
    if ret:
        cv2.imshow("CAM", output)
    else:
        break
    
    if cv2.waitKey(10) == 27:
        break
    
    if STATUS:
        print("FIRE DETECTED!")
    
cam.release()
cv2.destroyAllWindows()
