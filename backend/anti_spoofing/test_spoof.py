import cv2
from anti_spoofing.spoof_detector import SpoofDetector

detector = SpoofDetector()

img = cv2.imread("C:\major project\Smart-Attendance\backend\WhatsApp Image 2026-01-09 at 11.59.22 AM.jpeg")   

result = detector.is_real(img)
print("Is real face?", result)
