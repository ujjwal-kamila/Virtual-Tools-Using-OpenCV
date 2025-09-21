import cv2
import mediapipe as mp
import time
import numpy as np
import pyautogui

cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands(min_detection_confidence=0.7)
mpDraw = mp.solutions.drawing_utils

screen_width, screen_height = pyautogui.size() # type: ignore

# Define color styles for drawing
connection_style = mpDraw.DrawingSpec(color=(0, 255, 0), thickness=2)
landmark_style = mpDraw.DrawingSpec(color=(0, 0, 255), thickness=5)

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)  # Flip the image to avoid mirror effect
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            lmList = []
            for id, lm in enumerate(handLms.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append((cx, cy))

            if lmList:
                index_finger = lmList[8]  # Index finger tip
                thumb = lmList[4]  # Thumb tip
                
                # Map hand coordinates to screen coordinates
                screen_x = np.interp(index_finger[0], (0, w), (0, screen_width))
                screen_y = np.interp(index_finger[1], (0, h), (0, screen_height))
                
                pyautogui.moveTo(screen_x, screen_y) # type: ignore

                # Check distance between thumb and index finger for clicking action
                distance = np.linalg.norm(np.array(index_finger) - np.array(thumb))
                if distance < 40:  # Adjust threshold as needed
                    pyautogui.click()

            # Draw landmarks
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS, landmark_style, connection_style)
    
    cv2.imshow('Virtual Mouse', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to exit
        break

cap.release()
cv2.destroyAllWindows()
