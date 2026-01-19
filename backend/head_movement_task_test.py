import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

MODEL_PATH = "models/face_landmarker.task"
YAW_THRESHOLD = 0.03     # left / right
PITCH_THRESHOLD = 0.03   # up / down

NOSE_TIP = 1
LEFT_EYE = 33
RIGHT_EYE = 263
FOREHEAD = 10
CHIN = 152

base_options = python.BaseOptions(model_asset_path=MODEL_PATH)
options = vision.FaceLandmarkerOptions(
    base_options=base_options,
    running_mode=vision.RunningMode.VIDEO,
    num_faces=1
)

detector = vision.FaceLandmarker.create_from_options(options)

cap = cv2.VideoCapture(0)

movement_detected = {
    "LEFT": False,
    "RIGHT": False,
    "UP": False,
    "DOWN": False
}

print("Turn your head LEFT and RIGHT. Press Q to quit.")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)

    results = detector.detect_for_video(
        mp_image,
        int(cap.get(cv2.CAP_PROP_POS_MSEC))
    )

    status = "NO MOVEMENT"

    if results.face_landmarks:
        landmarks = results.face_landmarks[0]

        nose = landmarks[NOSE_TIP]
        left_eye = landmarks[LEFT_EYE]
        right_eye = landmarks[RIGHT_EYE]
        forehead = landmarks[FOREHEAD]
        chin = landmarks[CHIN]

        eye_center_x = (left_eye.x + right_eye.x) / 2
        yaw = nose.x - eye_center_x

        if yaw > YAW_THRESHOLD:
            movement_detected["RIGHT"] = True
            status = "HEAD RIGHT"
        elif yaw < -YAW_THRESHOLD:
            movement_detected["LEFT"] = True
            status = "HEAD LEFT"

        face_center_y = (forehead.y + chin.y) / 2
        pitch = nose.y - face_center_y

        if pitch > PITCH_THRESHOLD:
            movement_detected["DOWN"] = True
            status = "HEAD DOWN"
        elif pitch < -PITCH_THRESHOLD:
            movement_detected["UP"] = True
            status = "HEAD UP"

    cv2.putText(
        frame,
        f"Status: {status}",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )

    completed = all(movement_detected.values())
    cv2.putText(
        frame,
        f"Movement Completed: {completed}",
        (20, 80),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.9,
        (255, 255, 0),
        2
    )

    cv2.imshow("Head Movement Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
