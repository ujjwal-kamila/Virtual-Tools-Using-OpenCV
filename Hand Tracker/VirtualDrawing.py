import cv2
import mediapipe as mp
import numpy as np

# Initialize camera
cap = cv2.VideoCapture(0)

# Initialize Mediapipe Hands
mpHands = mp.solutions.hands
hands = mpHands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.8)
mpDraw = mp.solutions.drawing_utils

# Create a blank canvas for drawing
canvas = None

# Initialize drawing parameters
draw_color = (255, 0, 0)  # Default: Blue
brush_thickness = 5
eraser_thickness = 50

# Previous position of the index finger
prev_x, prev_y = None, None

# Function to find the index finger's position
def get_index_finger_position(landmarks, img_shape):
    h, w, _ = img_shape
    x = int(landmarks.landmark[mpHands.HandLandmark.INDEX_FINGER_TIP].x * w)
    y = int(landmarks.landmark[mpHands.HandLandmark.INDEX_FINGER_TIP].y * h)
    return x, y

# Function to count raised fingers
def count_raised_fingers(hand_landmarks):
    # Finger tip landmarks (thumb, index, middle, ring, pinky)
    finger_tips = [
        mpHands.HandLandmark.THUMB_TIP,
        mpHands.HandLandmark.INDEX_FINGER_TIP,
        mpHands.HandLandmark.MIDDLE_FINGER_TIP,
        mpHands.HandLandmark.RING_FINGER_TIP,
        mpHands.HandLandmark.PINKY_TIP,
    ]
    finger_pips = [
        mpHands.HandLandmark.THUMB_IP,
        mpHands.HandLandmark.INDEX_FINGER_PIP,
        mpHands.HandLandmark.MIDDLE_FINGER_PIP,
        mpHands.HandLandmark.RING_FINGER_PIP,
        mpHands.HandLandmark.PINKY_PIP,
    ]

    fingers = []
    for tip, pip in zip(finger_tips, finger_pips):
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[pip].y:
            fingers.append(1)  # Finger is raised
        else:
            fingers.append(0)  # Finger is not raised
    return fingers

while True:
    success, img = cap.read()
    if not success:
        break

    # Flip the image horizontally for a mirrored effect
    img = cv2.flip(img, 1)

    # Initialize canvas if not already
    if canvas is None:
        canvas = np.zeros_like(img)

    # Convert to RGB and process with Mediapipe
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            # Draw hand landmarks
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)
            
            # Get the position of the index finger tip
            x, y = get_index_finger_position(handLms, img.shape)

            # Count raised fingers to change color or erase
            fingers = count_raised_fingers(handLms)
            raised_count = sum(fingers)

            # Change color based on the number of raised fingers
            if raised_count == 2:
                draw_color = (0, 0, 255)  # Red
            elif raised_count == 3:
                draw_color = (0, 255, 0)  # Green
            elif raised_count == 4:
                draw_color = (255, 0, 0)  # Blue
            elif raised_count == 5:
                draw_color = (0, 0, 0)  # Eraser mode

            # Draw connected lines
            if raised_count > 0:
                thickness = eraser_thickness if draw_color == (0, 0, 0) else brush_thickness
                if prev_x is not None and prev_y is not None:
                    cv2.line(canvas, (prev_x, prev_y), (x, y), draw_color, thickness)
                prev_x, prev_y = x, y
            else:
                # Reset previous position if no fingers are raised
                prev_x, prev_y = None, None

    # Combine canvas and video feed
    img = cv2.addWeighted(img, 0.5, canvas, 0.5, 0)

    # Show the image
    cv2.imshow('Virtual Drawing', img)

    # Keyboard controls
    key = cv2.waitKey(1)
    if key & 0xFF == ord('q'):  # Press 'q' to exit
        break
    elif key & 0xFF == ord('s'):  # Press 's' to save the canvas
        cv2.imwrite('drawing.png', canvas)
        print("Canvas saved as 'drawing.png'!")

# Release resources
cap.release()
cv2.destroyAllWindows()
