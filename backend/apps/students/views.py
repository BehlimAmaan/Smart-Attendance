from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from apps.students.models import StudentProfile
from apps.attendance.models import AttendanceSession, AttendanceRecord



class StudentAttendanceSummaryAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role != "STUDENT":
            return Response(
                {"detail": "Only students can access this"},
                status=status.HTTP_403_FORBIDDEN
            )

        try:
            student_profile = request.user.student_profile
        except StudentProfile.DoesNotExist:
            return Response(
                {"detail": "Student profile not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        teacher_user = student_profile.teacher.user

        completed_sessions = AttendanceSession.objects.filter(
            teacher=teacher_user,
            is_active=False
        )

        total_sessions = completed_sessions.count()

        present_sessions = AttendanceRecord.objects.filter(
            student=request.user,
            session__in=completed_sessions
        ).count()

        percentage = (
            (present_sessions / total_sessions) * 100
            if total_sessions > 0 else 0
        )

        return Response(
            {
                "total_sessions": total_sessions,
                "present_sessions": present_sessions,
                "attendance_percentage": round(percentage, 2),
            },
            status=status.HTTP_200_OK,
        )


class StudentAttendanceHistoryAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role != "STUDENT":
            return Response(
                {"detail": "Only students can access this"},
                status=status.HTTP_403_FORBIDDEN
            )

        try:
            student_profile = request.user.student_profile
        except StudentProfile.DoesNotExist:
            return Response(
                {"detail": "Student profile not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        teacher_user = student_profile.teacher.user

        sessions = AttendanceSession.objects.filter(
            teacher=teacher_user,
            is_active=False
        ).order_by("-start_time")

        records = AttendanceRecord.objects.filter(
            student=request.user,
            session__teacher=teacher_user
        )

        record_map = {r.session_id: r for r in records}

        history = []

        for session in sessions:
            record = record_map.get(session.id)

            if record:
                history.append({
                    "date": session.start_time.date(),
                    "subject": session.subject,
                    "status": "Present",
                    "method": record.method,
                    "time": record.marked_at.strftime("%H:%M:%S"),
                })
            else:
                history.append({
                    "date": session.start_time.date(),
                    "subject": session.subject,
                    "status": "Absent",
                    "method": "-",
                })

        return Response(
            {"history": history},
            status=status.HTTP_200_OK
        )
