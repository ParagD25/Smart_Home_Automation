import cv2,requests
import time
import os
import handTrack as htm


wCam, hCam = 640, 480
 
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
 
folderPath = "Images"
myList = os.listdir(folderPath)
print(myList)
overlayList = []
for imPath in myList:
    image = cv2.imread(f'{folderPath}/{imPath}')
    # print(f'{folderPath}/{imPath}')
    overlayList.append(image)
 
print(len(overlayList))
pTime = 0
 
detector = htm.handDetector(detectionCon=0.75)
 
tipIds = [4, 8, 12, 16, 20]
 
while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    # print(lmList)
 
    if len(lmList) != 0:
        fingers = []
 
        # Thumb
        if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)
 
        # 4 Fingers
        for id in range(1, 5):
            if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
 
        # print(fingers)
        totalFingers = fingers.count(1)
        # print(totalFingers)
 
        # h, w, c = overlayList[totalFingers - 1].shape
        # img[0:200, 0:200] = overlayList[totalFingers - 1]
 
        # cv2.rectangle(img, (20, 225), (170, 425), (0, 255, 0), cv2.FILLED)
        if totalFingers==0:
            cv2.putText(img,'All LED Off', (45, 375), cv2.FONT_HERSHEY_PLAIN,5, (0, 0, 255), 10)

        elif totalFingers==1:
            cv2.putText(img, 'LED 1 On', (45, 375), cv2.FONT_HERSHEY_PLAIN,5, (0, 255, 0), 10)
            requests.get('http://192.168.239.251/?relay1=on')

        elif totalFingers==2:
            cv2.putText(img, 'LED 1 Off', (45, 375), cv2.FONT_HERSHEY_PLAIN,5, (0, 0, 255), 10)
            requests.get('http://192.168.239.251/?relay1=off')

        elif totalFingers==3:
            cv2.putText(img, 'LED 2 On', (45, 375), cv2.FONT_HERSHEY_PLAIN,5, (0, 255, 0), 10)
            requests.get('http://192.168.239.251/?relay2=on')

        elif totalFingers==4:
            cv2.putText(img, 'LED 2 Off', (45, 375), cv2.FONT_HERSHEY_PLAIN,5, (0, 0, 255), 10)
            requests.get('http://192.168.239.251/?relay2=off')

        elif totalFingers==5:
            cv2.putText(img, 'All LED On', (45, 375), cv2.FONT_HERSHEY_PLAIN,5, (0, 255, 0), 10)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
 
    # cv2.putText(img, f'FPS: {int(fps)}', (400, 70), cv2.FONT_HERSHEY_PLAIN,3, (255, 0, 0), 3)
 
    cv2.imshow("Image", img)
    # cv2.waitKey(1)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break