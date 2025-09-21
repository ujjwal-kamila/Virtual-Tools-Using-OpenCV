

# ✋ Virtual Tools – Hand Tracking System

A collection of virtual tools powered by real-time hand tracking and gesture recognition using OpenCV and MediaPipe. This project allows you to interact with your computer in a more intuitive and natural way.

## 📌 Overview

The **Virtual Tools** project is a Python-based application that leverages the power of computer vision to track hand movements and gestures in real-time. It provides an interactive way to control applications such as a **virtual whiteboard** for drawing or a **virtual mouse** for system navigation without needing any physical hardware beyond a webcam. This makes human-computer interaction more seamless and futuristic.

## 🚀 Features

  * 🎥 **Real-time Hand Tracking**: Detects and tracks 21 key landmarks on the hand with high accuracy.
  * 🖐️ **Gesture Recognition**: Understands various hand gestures, like pointing and pinching, to trigger actions.
  * 📝 **Virtual Drawing**: Draw on a virtual canvas using your hand movements.
  * 🖱️ **Virtual Mouse Control**: Navigate your desktop, move the cursor, and click using simple hand gestures.
  * 🔊 **Volume & Brightness Control**: Adjust your system's volume and screen brightness with hand gestures.
  * 🔢 **Finger Counting**: A simple tool that counts the number of fingers you hold up.
  * ⚡ **Smooth & Low Latency**: Optimized for a responsive and smooth user experience.

## 🛠️ Tech Stack

  * **Programming Language**: Python
  * **Core Libraries**:
      * **OpenCV**: For camera feed processing and computer vision tasks.
      * **MediaPipe**: For robust, high-fidelity hand and finger tracking.
      * **NumPy**: For numerical operations and array manipulation.
      * **PyAutoGUI**: For programmatically controlling the mouse and keyboard.

## ⚙️ Installation & Setup

Follow these steps to get the project up and running on your local machine.

### 1\. Prerequisites

  * **Python 3.7** or higher. You can download it from Python Official page
  * **pip** package manager (usually comes with Python).

### 2\. Clone the Repository

Open your terminal or command prompt and clone this repository:

```
git clone https://github.com/ujjwal-kamila/Virtual-Tools-Using-OpenCV.git
cd Virtual-Tools-Using-OpenCV
```
### 3\. Create a Virtual Environment (Recommended)

It's a good practice to create a virtual environment to keep project dependencies isolated.

```
# For Windows
python -m venv venv
venv\Scripts\activate

# For macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 4\. Install Dependencies

Install all the required libraries, use the below command.


```
pip install opencv-python mediapipe numpy pyautogui
```

## ▶️ How to Use

Once the setup is complete, you can run the individual tools. All scripts are located in the `Hand Tracker` directory.

```
cd "Hand Tracker"
```

### Virtual Mouse

To start the virtual mouse, run the following command in your terminal:

```
python virtual_mouse.py
```

  * **Move Cursor**: Move your index finger around the screen.
  * **Click**: Bring your thumb and index finger together.

### Virtual Drawing

To launch the virtual drawing tool, run:

```
python VirtualDrawing.py
```

  * **Draw**: Hold up your index finger and move it to draw.
  * **Select**: Hold up your index and middle fingers to enter selection mode.

### Finger Counter

To start the finger counter, run:

```
python FingurCount.py
```

  * The application will display a count of how many fingers you are holding up.

### Volume & Brightness Control

To control your system's volume and brightness, run:

```
python VolumnBright.py
```

  * Use gestures (like pinching and moving your hand up/down) to adjust levels.

## 📁 Project Structure

```
Virtual-Tools-Using-OpenCV/
├── .gitattributes
├── .gitignore
├── LICENSE
├── README.md
│
└───Hand Tracker/
    ├── FingurCount.py        # Counts fingers
    ├── HandTrack.py          # Reusable hand tracking module
    ├── VirtualDrawing.py     # Virtual drawing canvas
    ├── virtual_mouse.py      # Virtual mouse control
    ├── VolumnBright.py       # Volume and brightness control
    └── WBDrawing.py          # Whiteboard drawing application
```

## 🤝 Contributing

Contributions, issues, and feature requests are welcome\! Feel free to check the issues page.



## 📄 License

This project is licensed under the MIT License.

<br>

---

<h3 align="center">
  <b>Happy Coding 👨‍💻 | Keep Practicing 💡</b>
</h3>

---

<h3 align="center">
  <b>Let's Connect!! </b>
  <img src="https://user-images.githubusercontent.com/74038190/214644145-264f4759-7633-441e-9d67-d8dda9d50d26.gif" width=95px>
</h3>

<p align="center">
  <a href="https://ujjwal-kamila.vercel.app/"><img src="https://img.shields.io/badge/Portfolio-Visit-blue?logo=Firefox&logoColor=white"></a>
  <a href="https://www.linkedin.com/in/ujjwal-kamila-8a12a4262/"><img src="https://img.shields.io/badge/LinkedIn-%230077B5.svg?logo=linkedin&logoColor=white"></a>
  <a href="https://leetcode.com/ujjwalkamila86/"><img src="https://img.shields.io/badge/LeetCode-FFA116.svg?logo=LeetCode&logoColor=black"></a>
</p>