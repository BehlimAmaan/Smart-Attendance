import cv2
from anti_spoofing.spoof_detector import SpoofDetector

detector = SpoofDetector()

img = cv2.imread("WhatsApp Image 2026-01-09 at 11.59.22 AM.jpeg")
print("Image is None?", img is None)

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

faces = face_cascade.detectMultiScale(
    gray,
    scaleFactor=1.2,
    minNeighbors=5,
    minSize=(100, 100)
)

if len(faces) == 0:
    print("No face detected")
    exit()

x, y, w, h = sorted(faces, key=lambda f: f[2] * f[3], reverse=True)[0]
face_crop = img[y:y+h, x:x+w]

result = detector.is_real(face_crop)
print("Is real face?", result)
