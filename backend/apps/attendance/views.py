from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
import pickle
import math

from django.db import transaction, IntegrityError
from django.utils import timezone
from datetime import timedelta
import secrets

from apps.face_liveness.liveness_engine import LivenessEngine
from apps.face_liveness.face_matcher import FaceMatcher
from anti_spoofing.spoof_detector import SpoofDetector

from .models import AttendanceSession, AttendanceRecord, QRToken
from .serializers import AttendanceSessionSerializer

import cv2
import numpy as np


liveness_engine = LivenessEngine()
face_matcher = FaceMatcher()
spoof_detector = SpoofDetector()


# ✅ FIXED LOCATION CHECK (GPS-REALISTIC)
def is_within_radius(lat1, lon1, lat2, lon2, radius, accuracy=0):
    R = 6371000  # meters

    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)

    a = (
        math.sin(dphi / 2) ** 2 +
        math.cos(phi1) * math.cos(phi2) *
        math.sin(dlambda / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c

    # Dynamic buffer for GPS noise (minimum 50m)
    allowed_distance = radius + max(accuracy, 50)

    return distance <= allowed_distance


class StartAttendanceSessionAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.user.role != "TEACHER":
            return Response({"detail": "Only teachers"}, status=403)

        subject = request.data.get("subject")
        latitude = request.data.get("latitude")
        longitude = request.data.get("longitude")
        radius = request.data.get("radius", 150)
        duration = request.data.get("duration_minutes")

        if not subject or latitude is None or longitude is None or not duration:
            return Response(
                {"detail": "Subject, location and duration required"},
                status=400
            )

        start_time = timezone.now()
        end_time = start_time + timedelta(minutes=int(duration))

        with transaction.atomic():
            AttendanceSession.objects.filter(
                teacher=request.user,
                is_active=True
            ).update(is_active=False)

            session = AttendanceSession.objects.create(
                teacher=request.user,
                subject=subject,
                latitude=latitude,
                longitude=longitude,
                radius_meters=radius,
                duration_minutes=duration,
                start_time=start_time,
                end_time=end_time
            )

        return Response(
            AttendanceSessionSerializer(session).data,
            status=201
        )


class EndAttendanceSessionAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, session_id):
        if request.user.role != "TEACHER":
            return Response({"detail": "Only teachers"}, status=403)

        try:
            session = AttendanceSession.objects.get(
                id=session_id,
                teacher=request.user,
                is_active=True
            )
        except AttendanceSession.DoesNotExist:
            return Response({"detail": "Active session not found"}, status=404)

        session.is_active = False
        session.end_time = timezone.now()
        session.save()

        return Response({"detail": "Session ended"}, status=200)


class GenerateQRTokenAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role != "TEACHER":
            return Response({"detail": "Only teachers"}, status=403)

        try:
            session = AttendanceSession.objects.get(
                teacher=request.user,
                is_active=True
            )
        except AttendanceSession.DoesNotExist:
            return Response({"detail": "No active session"}, status=404)

        token = secrets.token_hex(16)
        qr = QRToken.objects.create(session=session, token=token)

        return Response({
            "session_id": session.id,
            "qr_token": qr.token,
            "expires_in": 5
        })


class MarkAttendanceAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.user.role != "STUDENT":
            return Response({"detail": "Only students"}, status=403)

        session_id = request.data.get("session_id")
        method = request.data.get("method")

        if not session_id or not method:
            return Response({"detail": "session_id and method required"}, status=400)

        try:
            session = AttendanceSession.objects.get(
                id=session_id,
                is_active=True
            )
        except AttendanceSession.DoesNotExist:
            return Response({"detail": "Session not active"}, status=404)

        if session.has_expired():
            session.is_active = False
            session.save()
            return Response(
                {"detail": "Attendance session has ended"},
                status=403
            )

        try:
            student_profile = request.user.student_profile
        except Exception:
            return Response(
                {"detail": "Student profile not found"},
                status=403
            )

        if student_profile.teacher.user != session.teacher:
            return Response(
                {"detail": "Unauthorized attendance attempt"},
                status=403
            )

        # ✅ LOCATION CHECK FIXED
        if method == "FACE":
            lat = request.data.get("latitude")
            lon = request.data.get("longitude")
            accuracy = request.data.get("accuracy", 0)

            if lat is None or lon is None:
                return Response({"detail": "Location required"}, status=400)

            lat = float(lat)
            lon = float(lon)
            accuracy = float(accuracy)

            if accuracy > 300:
                location_ok = True
            else:
                location_ok = is_within_radius(
                    lat,
                    lon,
                    session.latitude,
                    session.longitude,
                    session.radius_meters,
                    accuracy
                )

            if not location_ok:
                return Response(
                    {
                        "detail": "You are outside the attendance area",
                        "allowed_radius": session.radius_meters,
                        "gps_accuracy": accuracy
                    },
                    status=403
                )

        if method == "FACE":
            face_image = request.FILES.get("face_image")
            if not face_image:
                return Response({"detail": "Face image required"}, status=400)

            img_array = np.frombuffer(face_image.read(), np.uint8)
            face_img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

            if face_img is None:
                return Response({"detail": "Invalid image"}, status=400)

            if not spoof_detector.is_real(face_img):
                return Response({"detail": "Spoof detected"}, status=400)

            blink_ok = request.data.get("blink_ok") == "true"
            head_ok = request.data.get("head_ok") == "true"

            is_live, _ = liveness_engine.verify_liveness(
                blink_ok=blink_ok,
                head_ok=head_ok,
                spoof_ok=True
            )

            if not is_live:
                return Response({"detail": "Liveness failed"}, status=400)

            if not request.user.face_embedding:
                return Response({"detail": "Face not registered"}, status=403)

            stored_embedding = pickle.loads(request.user.face_embedding)
            live_embedding = face_matcher.get_embedding(face_img)

            if live_embedding is None:
                return Response({"detail": "No face detected"}, status=400)

            match, similarity = face_matcher.match(
                stored_embedding,
                live_embedding
            )

            if not match:
                request.user.face_embedding = None
                request.user.save()
                return Response(
                    {
                        "detail": "Face mismatch",
                        "error_code": "FACE_MISMATCH",
                        "similarity": round(similarity, 4)
                    },
                    status=403
                )

        try:
            AttendanceRecord.objects.create(
                student=request.user,
                session=session,
                method=method
            )
        except IntegrityError:
            return Response(
                {"detail": "Attendance already marked"},
                status=400
            )

        return Response({"detail": "Attendance marked"}, status=201)


class ActiveAttendanceSessionAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        session = AttendanceSession.objects.filter(
            is_active=True
        ).order_by("-start_time").first()

        if not session:
            return Response({"active": False})

        if session.has_expired():
            session.is_active = False
            session.save()
            return Response({"active": False})

        return Response({
            "active": True,
            "session_id": session.id,
            "subject": session.subject,
            "teacher": session.teacher.email,
            "start_time": session.start_time,
            "end_time": session.end_time,
            "remaining_seconds": int(
                (session.end_time - timezone.now()).total_seconds()
            )
        })


class LiveAttendanceAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role != "TEACHER":
            return Response({"detail": "Only teachers"}, status=403)

        try:
            session = AttendanceSession.objects.get(
                teacher=request.user,
                is_active=True
            )
        except AttendanceSession.DoesNotExist:
            return Response({"active": False})

        records = (
            AttendanceRecord.objects
            .filter(session=session)
            .select_related("student__student_profile")
            .order_by("marked_at")
        )

        present_students = [
            {
                "roll_no": r.student.student_profile.roll_no,
                "full_name": r.student.student_profile.full_name,
                "marked_at": r.marked_at.strftime("%H:%M:%S"),
                "method": r.method
            }
            for r in records
        ]

        total_students = session.teacher.teacher_profile.students.count()

        return Response({
            "active": True,
            "session_id": session.id,
            "subject": session.subject,
            "total_students": total_students,
            "present_count": len(present_students),
            "present_students": present_students
        })
