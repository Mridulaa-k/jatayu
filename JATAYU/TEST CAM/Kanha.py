import cv2
import dlib
import numpy as np
import mediapipe as mp
import paho.mqtt.client as mqtt

# MQTT Configuration
MQTT_BROKER = "broker.emqx.io"
MQTT_PORT = 1883
MQTT_TOPIC = "jatayu/sleep_alert"

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.connect(MQTT_BROKER, MQTT_PORT, 60)

# Load pre-trained face detector and facial landmark model
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("D:\PROJECT\JATAYU\Shape predictor\shape_predictor_68_face_landmarks.dat\shape_predictor_68_face_landmarks.dat")

# Initialize Mediapipe Pose Estimation
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Constants
EAR_THRESHOLD = 0.22  # Threshold for closed eyes
FRAME_THRESHOLD = 30   # 1 second at 30 FPS
sleep_frame_count = 0  # Counter for how long eyes remain closed

def calculate_eye_aspect_ratio(eye_landmarks):
    """ Compute the Eye Aspect Ratio (EAR) to detect if eyes are closed """
    vertical_1 = np.linalg.norm(np.array([eye_landmarks[1].x, eye_landmarks[1].y]) - np.array([eye_landmarks[5].x, eye_landmarks[5].y]))
    vertical_2 = np.linalg.norm(np.array([eye_landmarks[2].x, eye_landmarks[2].y]) - np.array([eye_landmarks[4].x, eye_landmarks[4].y]))
    horizontal = np.linalg.norm(np.array([eye_landmarks[0].x, eye_landmarks[0].y]) - np.array([eye_landmarks[3].x, eye_landmarks[3].y]))
    return (vertical_1 + vertical_2) / (2.0 * horizontal)

# Initialize webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector(gray, 1)

    for face in faces:
        landmarks = predictor(gray, face)

        # Extract eye landmarks
        left_eye_landmarks = [landmarks.part(i) for i in range(36, 42)]
        right_eye_landmarks = [landmarks.part(i) for i in range(42, 48)]

        left_ear = calculate_eye_aspect_ratio(left_eye_landmarks)
        right_ear = calculate_eye_aspect_ratio(right_eye_landmarks)

        is_sleeping = left_ear < EAR_THRESHOLD and right_ear < EAR_THRESHOLD

        if is_sleeping:
            sleep_frame_count += 1
        else:
            sleep_frame_count = max(0, sleep_frame_count - 2)

        # Trigger sleep alert if eyes are closed for FRAME_THRESHOLD frames
        if sleep_frame_count >= FRAME_THRESHOLD:
            cv2.putText(frame, "Person is Sleeping!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
            client.publish(MQTT_TOPIC, "ALERT")
            sleep_frame_count = 0  # Reset after alert

    # Pose estimation - detect overall posture
    result = pose.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    if result.pose_landmarks:
        cv2.putText(frame, "Monitoring Posture...", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)

    # Display the frame with updated sleep detection
    cv2.imshow("Sleep Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
client.disconnect()
