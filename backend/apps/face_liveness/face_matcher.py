import cv2
import numpy as np
import os
import pickle
import face_recognition


class FaceMatcher:
    def __init__(self):
        self.base_dir = "media/face_embeddings"
        os.makedirs(self.base_dir, exist_ok=True)
        self.threshold = 0.6

    def get_embedding(self, face_img):
        """
        Extract face embedding from OpenCV image (BGR)
        """
        if face_img is None:
            return None

        rgb_img = cv2.cvtColor(face_img, cv2.COLOR_BGR2RGB)
        encodings = face_recognition.face_encodings(rgb_img)

        if not encodings:
            return None

        return encodings[0]

    def extract_embedding(self, image_file):
        """
        Extract embedding from uploaded image file
        """
        img = face_recognition.load_image_file(image_file)
        encodings = face_recognition.face_encodings(img)

        if not encodings:
            return None

        return encodings[0]

    def save_embedding(self, user_id, embedding):
        path = os.path.join(self.base_dir, f"{user_id}.pkl")
        with open(path, "wb") as f:
            pickle.dump(embedding, f)

    def load_embedding(self, user_id):
        path = os.path.join(self.base_dir, f"{user_id}.pkl")
        if not os.path.exists(path):
            return None
        with open(path, "rb") as f:
            return pickle.load(f)

    def match(self, stored_embedding, live_embedding):
        distance = np.linalg.norm(stored_embedding - live_embedding)
        return distance < self.threshold, float(distance)
