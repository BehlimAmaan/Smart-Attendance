from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.utils import timezone
from datetime import timedelta
from django.shortcuts import get_object_or_404

from .models import QRToken
from apps.attendance.models import AttendanceSession, AttendanceRecord


class GenerateQRAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.user.role != "TEACHER":
            return Response(
                {"detail": "Only teachers can generate QR"},
                status=status.HTTP_403_FORBIDDEN
            )

        session = (
            AttendanceSession.objects
            .filter(is_active=True)
            .order_by("-start_time")
            .first()
        )

        if not session:
            return Response(
                {"detail": "No active attendance session"},
                status=status.HTTP_400_BAD_REQUEST
            )

        qr = QRToken.objects.create(
            session_id=session.id,
            expires_at=timezone.now() + timedelta(seconds=5)
        )

        return Response({
            "qr_token": str(qr.token),
            "expires_in": 5
        })


class MarkAttendanceViaQRAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.user.role != "STUDENT":
            return Response(
                {"detail": "Only students can mark attendance"},
                status=status.HTTP_403_FORBIDDEN
            )

        token = request.data.get("token")
        if not token:
            return Response(
                {"detail": "QR token required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        qr = get_object_or_404(QRToken, token=token)

        if not qr.is_valid():
            return Response(
                {"detail": "QR code expired"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if AttendanceRecord.objects.filter(
            student=request.user,
            session_id=qr.session_id
        ).exists():
            return Response(
                {"detail": "Attendance already marked"},
                status=status.HTTP_400_BAD_REQUEST
            )

        AttendanceRecord.objects.create(
            student=request.user,
            session_id=qr.session_id,
            method="QR"
        )

        return Response({"detail": "Attendance marked via QR"})
