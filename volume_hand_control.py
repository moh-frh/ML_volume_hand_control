import math
import time
from ctypes import POINTER, cast

import cv2
import numpy as np
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

import HandTrackingModule as htm

################################################################################################
wCam, hCam = 640, 480
################################################################################################

cap = cv2.VideoCapture(0)

cap.set(3, wCam)
cap.set(4, hCam)
# pTime = 0

detector = htm.handDetector(detectionCon=0.7)






devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# volume.GetMute()
# volume.GetMasterVolumeLevel()

# range between -96.0 and 0.0
volumeRange = volume.GetVolumeRange()

minVolume = volumeRange[0] 
maxVolume = volumeRange[1] 





while True:
    success, img = cap.read()

    img = detector.findHands(img)

    lmList = detector.findPosition(img)

    if len(lmList) > 0:
        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]

        length =  math.hypot(x2 - x1, y2 - y1)

        # hand range --> 10, 150
        # volume range -96, 0

        vol = np.interp(length, [10, 150], [-96, 0])

        volume.SetMasterVolumeLevel(vol, None)

        cx, yx = (x1 + x2) //2, (y1 + y2) //2

        cv2.circle(img, (x1, y1), 5, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 5, (255, 0, 255), cv2.FILLED)

        cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 3)

        cv2.circle(img, (cx, yx), 5, (255, 0, 255), cv2.FILLED)

    # cTime = time.time()
    # fps = 1 / (cTime - pTime)
    # pTime = cTime

    # cv2.putText(img, f'FPS : {int(fps)}', (40, 70), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 0, 0), 3)

    cv2.imshow("Img", img)
    cv2.waitKey(1)

