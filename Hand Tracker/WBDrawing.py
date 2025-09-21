import cv2
import mediapipe as mp
import numpy as np

# Initialize camera
cap = cv2.VideoCapture(0)

# Initialize Mediapipe Hands
mpHands = mp.solutions.hands
hands = mpHands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.8)
mpDraw = mp.solutions.drawing_utils

# Define square resolution
square_size = 640
whiteboard = np.ones((square_size, square_size, 3), dtype=np.uint8) * 255  # Whiteboard

# Drawing parameters
draw_color = (0, 0, 0)  # Default: Black
brush_thickness = 5
eraser_thickness = 50

# Previous position of the index finger
prev_x, prev_y = None, None
dot_x, dot_y = None, None  # Position for the temporary black dot

# Function to get finger position
def get_finger_position(landmarks, finger, img_shape):
    h, w, _ = img_shape
    x = int(landmarks.landmark[finger].x * w)
    y = int(landmarks.landmark[finger].y * h)
    return x, y

# Function to count raised fingers
def count_raised_fingers(hand_landmarks):
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

# Function to check if the left thumb is extended
def is_left_thumb_visible(results):
    if results.multi_handedness:
        for idx, hand in enumerate(results.multi_handedness):
            label = hand.classification[0].label  # 'Left' or 'Right'
            if label == "Left" and results.multi_hand_landmarks:
                thumb_tip = results.multi_hand_landmarks[idx].landmark[mpHands.HandLandmark.THUMB_TIP]
                thumb_mcp = results.multi_hand_landmarks[idx].landmark[mpHands.HandLandmark.THUMB_MCP]
                # Check if the thumb is extended (y-coordinate of tip < MCP)
                if thumb_tip.y < thumb_mcp.y:
                    return True
    return False

while True:
    success, img = cap.read()
    if not success:
        break

    # Flip the image horizontally for a mirrored effect
    img = cv2.flip(img, 1)

    # Resize camera feed to a square
    img = cv2.resize(img, (square_size, square_size))

    # Convert to RGB and process with Mediapipe
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    drawing_allowed = not is_left_thumb_visible(results)  # Drawing is allowed if the left thumb is not visible

    if results.multi_hand_landmarks:
        for idx, handLms in enumerate(results.multi_hand_landmarks):
            # Draw hand landmarks on camera feed
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

            # Get the current hand's label ('Left' or 'Right')
            hand_label = results.multi_handedness[idx].classification[0].label

            if hand_label == "Right":  # Use the right hand for drawing
                # Get the position of the index finger
                x, y = get_finger_position(handLms, mpHands.HandLandmark.INDEX_FINGER_TIP, img.shape)

                # Save the position of the dot for display
                dot_x, dot_y = x, y

                # Count raised fingers to change color or erase
                fingers = count_raised_fingers(handLms)
                raised_count = sum(fingers)

                # Change color or enable eraser based on the number of raised fingers
                if raised_count == 2:
                    draw_color = (0, 0, 255)  # Red
                elif raised_count == 3:
                    draw_color = (0, 255, 0)  # Green
                elif raised_count == 4:
                    draw_color = (255, 0, 0)  # Blue
                elif raised_count == 5:
                    draw_color = (255, 255, 255)  # Eraser mode

                # Draw on the whiteboard
                if drawing_allowed:
                    thickness = eraser_thickness if draw_color == (255, 255, 255) else brush_thickness
                    if prev_x is not None and prev_y is not None:
                        cv2.line(whiteboard, (prev_x, prev_y), (x, y), draw_color, thickness)
                    prev_x, prev_y = x, y
                else:
                    # Reset previous position if drawing is not allowed
                    prev_x, prev_y = None, None

    # Display the temporary dot on the whiteboard
    temp_whiteboard = whiteboard.copy()
    if dot_x is not None and dot_y is not None:
        cv2.circle(temp_whiteboard, (dot_x, dot_y), 5, (0, 0, 0), -1)

    # Concatenate camera feed and whiteboard side by side
    combined_frame = np.hstack((img, temp_whiteboard))

    # Show the combined frame
    cv2.imshow('Camera Feed and Whiteboard', combined_frame)

    # Keyboard controls
    key = cv2.waitKey(1)
    if key & 0xFF == ord('q'):  # Press 'q' to exit
        break
    elif key & 0xFF == ord('s'):  # Press 's' to save the whiteboard
        cv2.imwrite('whiteboard.png', whiteboard)
        print("Whiteboard saved as 'board.png'!")

# Release resources
cap.release()
cv2.destroyAllWindows()
