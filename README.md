# CS6900_Project_4
# Pose-Based Exercise Routine Tracker

A real-time "smart gym coach" application built with Python, OpenCV, and MediaPipe. This tool tracks dumbbell bicep curls, counts repetitions automatically, checks for proper form, and detects the weight being used.

## Features

* **Workout Setup:** User-friendly start menu (Tkinter) to customize Reps, Sets, and Rest duration.
* **Real-Time Pose Estimation:** visualizes the user's skeleton (Arm & Body) using MediaPipe.
* **Smart Rep Counting:** Automatically detects full range of motion to count reps.
* **Form Checking Logic:**
    * **Anti-Cheat:** Detects if the user is leaning back or swinging their elbow.
    * **Visual Feedback:** Skeleton turns **RED** if form is incorrect and **GREEN** when correct.
* **Weight Detection:** Automatically detects **5lb** and **10lb** dumbbells using AprilTags.
* **On-Screen UI:** Live overlay showing current Reps, Sets, Workout State (Exercise/Rest), and Weight.

## Installation

    pip install -r requirements.txt
    ```
    *(Key libraries: `opencv-python`, `mediapipe`, `tkinter`, `numpy`)*

## How to Run

1.  Ensure your webcam is connected.
2.  Run the main script:
    ```bash
    python project4.py
    ```
3.  A settings window will appear. Enter your desired Reps, Rest time, and Sets, then click **Start**.

## Usage Guide

1.  **Camera Position:** Stand back from the camera so your upper body is clearly visible.
2.  **Orientation:** Stand sideways with your **Left Arm** facing the camera (the tracker is optimized for the left side profile).
3.  **Using Weights:**
    * Stick **AprilTag ID 5** on a 5lb weight.
    * Stick **AprilTag ID 10** on a 10lb weight.
    * Show the tag to the camera to see the "Weight: X lbs" overlay.
4.  **Perform the Exercise:**
    * Keep your body vertical and elbow pinned to your side.
    * If you lean or swing, the skeleton lines will turn **RED** and the rep will not count.

