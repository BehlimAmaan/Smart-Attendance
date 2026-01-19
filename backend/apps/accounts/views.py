from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model

from .serializers import LoginSerializer
import pickle
from apps.face_liveness.face_matcher import FaceMatcher

face_matcher = FaceMatcher()
User = get_user_model()
token_generator = PasswordResetTokenGenerator()

class RegisterFaceAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user

        if user.is_first_login:
            return Response(
                {"detail": "Please change password before face registration"},
                status=status.HTTP_403_FORBIDDEN,
            )

        if user.role != "STUDENT":
            return Response(
                {"detail": "Only students can register face"},
                status=status.HTTP_403_FORBIDDEN,
            )

        face_image = request.FILES.get("face_image")
        if not face_image:
            return Response(
                {"detail": "Face image required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        new_embedding = face_matcher.extract_embedding(face_image)
        if new_embedding is None:
            return Response(
                {"detail": "Face not detected"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if user.face_embedding:
            stored_embedding = pickle.loads(user.face_embedding)

            match, distance = face_matcher.match(
                stored_embedding, new_embedding
            )

            if not match:
                return Response(
                    {
                        "detail": "New face does not match previously registered face",
                        "error_code": "FACE_REREGISTER_MISMATCH",
                        "distance": distance,
                    },
                    status=status.HTTP_403_FORBIDDEN,
                )

        user.face_embedding = pickle.dumps(new_embedding)
        user.save()

        return Response(
            {"detail": "Face registered successfully"},
            status=status.HTTP_200_OK,
        )


class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]
        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "role": user.role,
                "email": user.email,
                "first_login": user.is_first_login,
            },
            status=status.HTTP_200_OK,
        )


class ChangePasswordAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        new_password = request.data.get("new_password")

        if not new_password:
            return Response(
                {"detail": "New password required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.set_password(new_password)
        user.is_first_login = False
        user.save()

        return Response(
            {"detail": "Password updated successfully"},
            status=status.HTTP_200_OK,
        )


class FaceStatusAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(
            {"face_registered": bool(request.user.face_embedding)},
            status=status.HTTP_200_OK,
        )

class ForgotPasswordAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")

        if not email:
            return Response(
                {"detail": "Email is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            # Do not reveal whether email exists
            return Response(
                {"detail": "If the email exists, a reset link has been sent"},
                status=status.HTTP_200_OK,
            )

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = token_generator.make_token(user)

        reset_link = f"{settings.FRONTEND_URL}/reset-password/{uid}/{token}"

        send_mail(
            subject="Reset your Smart Attendance password",
            message=f"Click the link to reset your password:\n{reset_link}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )

        return Response(
            {"detail": "Password reset link sent"},
            status=status.HTTP_200_OK,
        )


class ResetPasswordAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        uidb64 = request.data.get("uid")
        token = request.data.get("token")
        new_password = request.data.get("new_password")

        if not all([uidb64, token, new_password]):
            return Response(
                {"detail": "Invalid request"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except Exception:
            return Response(
                {"detail": "Invalid token"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not token_generator.check_token(user, token):
            return Response(
                {"detail": "Token expired or invalid"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.set_password(new_password)
        user.is_first_login = False
        user.save()

        return Response(
            {"detail": "Password reset successful"},
            status=status.HTTP_200_OK,
        )