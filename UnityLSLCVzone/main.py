import cv2 #the open cv library
from cvzone.HandTrackingModule import HandDetector
import socket #socket for upd communication
import numpy as np
#Import all my libraries
# Window settings and sets up the webcam

width, height = 720, 360 #The window size
cap = cv2.VideoCapture(0)
cap.set(3, width)
cap.set(4, height)

# Hand Detector
detector = HandDetector(maxHands=1, detectionCon=0.1)
#sets the amount of hands and the confidence of the detection. ie how sure it is that there is a hand present
# Initializes the UDP Socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverAddressPort = ("127.0.0.1", 5052)
#The localadress and the port that the data is sent to


# Main Loop
#Captures the frames and sends it to the designated port
while True:
    success, img = cap.read()
    if not success:
        continue  # Skips if frame isn't captured properly

    #didn't work how i wanted    
    # Flip the image horizontally
    #img = cv2.flip(img, 1)

    # Detect hands
    #hands = detector.findHands(img, flipType=True)
    hands, img = detector.findHands(img)
    #draw=True


    if hands:
        hand = hands[0]
        lmList = hand['lmList']# The list for the landmarks
        # Get the coordinates of the landmarks  
        data = []

        for lm in lmList:
            data.extend([lm[0], height - lm[1], lm[2]])

        # Send the full data list in one go
        sock.sendto(str.encode(str(data)), serverAddressPort)

    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('e'):
        break  # Escape the program on "e" keypress

cap.release()
cv2.destroyAllWindows()
