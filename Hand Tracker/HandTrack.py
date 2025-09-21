import cv2
import mediapipe as mp
import time

cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands()
import cv2
import mediapipe as mp

cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

# Define green color for connections
connection_style = mpDraw.DrawingSpec(color=(0, 255, 0), thickness=2)

# Define red color for points
landmark_style = mpDraw.DrawingSpec(color=(0, 0, 255), thickness=5)

while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            # Draw landmarks with red dots and green connections
            mpDraw.draw_landmarks(
                img, 
                handLms, 
                mpHands.HAND_CONNECTIONS, 
                landmark_style, 
                connection_style
            )
    
    cv2.imshow('Image', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to exit
        break

cap.release()
cv2.destroyAllWindows()
