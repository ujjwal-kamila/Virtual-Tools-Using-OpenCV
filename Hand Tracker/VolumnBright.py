import cv2
import mediapipe as mp
import pyautogui
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import wmi
import time

# Initialize camera
cap = cv2.VideoCapture(0)

# Initialize Mediapipe Hands
mpHands = mp.solutions.hands
hands = mpHands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.8)
mpDraw = mp.solutions.drawing_utils

# Initialize the volume control (Windows only)
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, 0, None)
volume = interface.QueryInterface(IAudioEndpointVolume)

# Initialize WMI for brightness control
wmi_service = wmi.WMI(namespace='wmi')
monitors = wmi_service.WmiMonitorBrightnessMethods()

# Function to get the position of the index, thumb, middle, and ring fingers
def get_finger_positions(hand_landmarks, img_shape):
    h, w, _ = img_shape
    finger_positions = {
        "thumb": (int(hand_landmarks.landmark[mpHands.HandLandmark.THUMB_TIP].x * w), 
                  int(hand_landmarks.landmark[mpHands.HandLandmark.THUMB_TIP].y * h)),
        "index": (int(hand_landmarks.landmark[mpHands.HandLandmark.INDEX_FINGER_TIP].x * w),
                  int(hand_landmarks.landmark[mpHands.HandLandmark.INDEX_FINGER_TIP].y * h)),
        "middle": (int(hand_landmarks.landmark[mpHands.HandLandmark.MIDDLE_FINGER_TIP].x * w),
                   int(hand_landmarks.landmark[mpHands.HandLandmark.MIDDLE_FINGER_TIP].y * h)),
        "ring": (int(hand_landmarks.landmark[mpHands.HandLandmark.RING_FINGER_TIP].x * w),
                 int(hand_landmarks.landmark[mpHands.HandLandmark.RING_FINGER_TIP].y * h)),
    }
    return finger_positions

# Function to adjust volume and brightness
def adjust_volume_brightness(finger_positions):
    # Volume control (Thumb + Index Finger)
    index_y = finger_positions['index'][1]
    thumb_y = finger_positions['thumb'][1]
    
    if abs(index_y - thumb_y) > 50:  # Significant vertical movement between thumb and index
        if index_y < thumb_y:  # Thumb below index, increase volume
            current_volume = volume.GetMasterVolumeLevelScalar()
            new_volume = min(current_volume + 0.05, 1.0)  # Increase volume but don't exceed max
            volume.SetMasterVolumeLevelScalar(new_volume, None)
            print(f"Volume Up: {new_volume*100:.0f}%")
        elif index_y > thumb_y:  # Thumb above index, decrease volume
            current_volume = volume.GetMasterVolumeLevelScalar()
            new_volume = max(current_volume - 0.05, 0.0)  # Decrease volume but don't go below 0
            volume.SetMasterVolumeLevelScalar(new_volume, None)
            print(f"Volume Down: {new_volume*100:.0f}%")

    # Brightness control (Middle + Ring Finger)
    middle_y = finger_positions['middle'][1]
    ring_y = finger_positions['ring'][1]
    
    if abs(middle_y - ring_y) > 50:  # Significant vertical movement between middle and ring
        if middle_y < ring_y:  # Fingers closer, increase brightness
            for monitor in monitors:
                current_brightness = monitor.WmiGetBrightness()[1]
                print(f"Current Brightness: {current_brightness}%")  # Debugging output
                new_brightness = min(current_brightness + 10, 100)  # Increase brightness but don't exceed 100%
                monitor.WmiSetBrightness(Brightness=new_brightness, Timeout=1)
                print(f"Brightness Up: {new_brightness}%")
        elif middle_y > ring_y:  # Fingers further, decrease brightness
            for monitor in monitors:
                current_brightness = monitor.WmiGetBrightness()[1]
                print(f"Current Brightness: {current_brightness}%")  # Debugging output
                new_brightness = max(current_brightness - 10, 0)  # Decrease brightness but don't go below 0%
                monitor.WmiSetBrightness(Brightness=new_brightness, Timeout=1)
                print(f"Brightness Down: {new_brightness}%")

# Main loop
while True:
    success, img = cap.read()
    if not success:
        break

    # Flip the image for mirror effect
    img = cv2.flip(img, 1)
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    
    # If hand landmarks are found
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)
            
            # Get finger positions
            finger_positions = get_finger_positions(handLms, img.shape)
            
            # Adjust volume and brightness based on finger movements
            adjust_volume_brightness(finger_positions)
            
            # Display Finger positions for debugging
            cv2.putText(img, 'Volume & Brightness Control', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

    # Show the frame
    cv2.imshow('Hand Gesture Control', img)

    if cv2.waitKey(1) & 0xFF == ord('q'):  # Exit on pressing 'q'
        break

cap.release()
cv2.destroyAllWindows()
