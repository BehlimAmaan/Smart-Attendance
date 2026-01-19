from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
import numpy as np
import cv2
import pickle
from .face_matcher import FaceMatcher

face_matcher = FaceMatcher()

class RegisterFaceAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.user.role != "STUDENT":
            return Response(
                {"detail": "Only students can register face"},
                status=status.HTTP_403_FORBIDDEN
            )

        face_image = request.FILES.get("face_image")
        if not face_image:
            return Response(
                {"detail": "Face image required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        img_array = np.frombuffer(face_image.read(), np.uint8)
        face_img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

        embedding = face_matcher.get_embedding(face_img)

        request.user.face_embedding = pickle.dumps(embedding)
        request.user.save()

        return Response(
            {"detail": "Face registered successfully"},
            status=status.HTTP_200_OK
        )
