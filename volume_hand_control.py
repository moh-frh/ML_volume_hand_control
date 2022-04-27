import time

import cv2
import numpy as np

import HandTrackingModule as htm

################################################################################################
wCam, hCam = 640, 480
################################################################################################

cap = cv2.VideoCapture(0)

cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0

detector = htm.handDetector(detectionCon=0.7)

while True:
    success, img = cap.read()

    img = detector.findHands(img)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, f'FPS : {int(fps)}', (40, 70), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 0, 0), 3)

    cv2.imshow("Img", img)
    cv2.waitKey(1)

# import cv2

# cam = cv2.VideoCapture(0)

# while True:
#     check, frame = cam.read()

#     cv2.imshow('video', frame)

#     key = cv2.waitKey(1)
#     if key == 27:
#         break

# cam.release()
# cv2.destroyAllWindows()
