import cv2
import dlib
import numpy as np
import mediapipe as mp
from time import sleep

# Load pre-trained face detector and pose estimation model from dlib
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("D:\PROJECT\JATAYU\Shape predictor\shape_predictor_68_face_landmarks.dat\shape_predictor_68_face_landmarks.dat")


  # Download from dlib model
mp_pose = mp.solutions.pose

# Helper function for detecting head position (leaning down for sleep)
def detect_head_position(landmarks):
    head_position = landmarks[0].y - landmarks[8].y  # Comparing position of nose vs chin
    return head_position < -0.04  # Negative value indicates head is downward

# Helper function for detecting closed eyes (sleep indicator)
def detect_eyes_closed(eye_landmarks):
    # Calculate aspect ratio to detect closed eyes
    eye_aspect_ratio = (abs(eye_landmarks[1].y - eye_landmarks[5].y) + abs(eye_landmarks[2].y - eye_landmarks[4].y)) / (2.0 * abs(eye_landmarks[0].x - eye_landmarks[3].x))
    return eye_aspect_ratio < 0.25  # Arbitrary threshold to detect eyes closed

# Initialize webcam
cap = cv2.VideoCapture(0)

# Setup Mediapipe Pose Estimation
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convert frame to RGB for pose detection
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Detect faces and landmarks
    faces = detector(rgb_frame, 1)
    for face in faces:
        landmarks = predictor(rgb_frame, face)

        # Analyze pose - head position
        head_leaning = detect_head_position(landmarks.parts())
        if head_leaning:
            cv2.putText(frame, "Person is likely sleeping: Head Down", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        # Detect eyes and check if they are closed (blink detection)
        # Assuming eye landmarks are between 36-41 (left eye) and 42-47 (right eye)
        left_eye_landmarks = [landmarks.part(i) for i in range(36, 42)]
        right_eye_landmarks = [landmarks.part(i) for i in range(42, 48)]

        left_eye_closed = detect_eyes_closed(left_eye_landmarks)
        right_eye_closed = detect_eyes_closed(right_eye_landmarks)

        if left_eye_closed and right_eye_closed:
            cv2.putText(frame, "Eyes Closed: Person might be sleeping", (50, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)

    # Pose estimation - detect overall posture (leaning forward could indicate sleep)
    result = pose.process(rgb_frame)
    if result.pose_landmarks:
        for landmark in result.pose_landmarks.landmark:
            if landmark.visibility < 0.5:  # If some body parts are not visible, skip
                continue
            # If we detect specific body positions (e.g., the chest area should be mostly upright in active people)
            cv2.putText(frame, "Person detected: Monitoring...", (50, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

    # Display the frame with the detected information
    cv2.imshow("Sleep Detection", frame)

    # Exit loop on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources and close windows
cap.release()
cv2.destroyAllWindows()
