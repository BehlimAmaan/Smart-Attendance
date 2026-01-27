from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import Notice
from .serializers import NoticeSerializer
from apps.students.models import StudentProfile


class TeacherNoticeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        teacher = request.user.teacher_profile
        notices = Notice.objects.filter(teacher=teacher).order_by("-created_at")
        return Response(NoticeSerializer(notices, many=True).data)

    def post(self, request):
        teacher = request.user.teacher_profile

        notice = Notice.objects.create(
            teacher=teacher,
            title=request.data.get("title"),
            description=request.data.get("description", ""),
            notice_type=request.data.get("notice_type"),
        )

        for f in request.FILES.getlist("files"):
            notice.files.create(file=f)

        return Response(
            {"message": "Notice created successfully"},
            status=status.HTTP_201_CREATED
        )

    def delete(self, request, notice_id):
        teacher = request.user.teacher_profile

        try:
            notice = Notice.objects.get(id=notice_id, teacher=teacher)
        except Notice.DoesNotExist:
            return Response(
                {"detail": "Notice not found or permission denied"},
                status=status.HTTP_404_NOT_FOUND
            )

        notice.delete()
        return Response(
            {"message": "Notice deleted successfully"},
            status=status.HTTP_200_OK
        )


class StudentNoticeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        student = request.user.student_profile
        notices = Notice.objects.filter(
            teacher=student.teacher
        ).order_by("-created_at")

        return Response(NoticeSerializer(notices, many=True).data)
