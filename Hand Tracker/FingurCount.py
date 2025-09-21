import cv2
import mediapipe as mp

# Initialize Mediapipe Hands
cap = cv2.VideoCapture(0)
mpHands = mp.solutions.hands
hands = mpHands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.8)
mpDraw = mp.solutions.drawing_utils

# Define green color for connections
connection_style = mpDraw.DrawingSpec(color=(0, 255, 0), thickness=2)

# Define red color for points
landmark_style = mpDraw.DrawingSpec(color=(0, 0, 255), thickness=5)

# Finger tip and pip landmark indices
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

def count_raised_fingers(hand_landmarks):
    """Count the number of raised fingers."""
    fingers = []
    for tip, pip in zip(finger_tips, finger_pips):
        # Check if the tip is above the pip (raised)
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[pip].y:
            fingers.append(1)  # Finger is raised
        else:
            fingers.append(0)  # Finger is not raised
    return sum(fingers)

while True:
    success, img = cap.read()
    if not success:
        break

    # Flip the image horizontally for a mirrored view
    img = cv2.flip(img, 1)
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    total_fingers = 0

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

            # Count the number of raised fingers for this hand
            total_fingers += count_raised_fingers(handLms)

    # Display the number (1 to 10) based on the total fingers detected
    cv2.putText(
        img,
        f'Number: {total_fingers}',
        (50, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (255, 0, 0),
        2
    )

    # Display the image
    cv2.imshow('Finger Count (1 to 10)', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to exit
        break

cap.release()
cv2.destroyAllWindows()
