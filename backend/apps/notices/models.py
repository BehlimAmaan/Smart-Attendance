from django.db import models
from apps.teachers.models import TeacherProfile


class Notice(models.Model):
    NOTICE_TYPES = [
        ("ATTENDANCE", "Attendance Sheet"),
        ("EXAM", "Exam / Marks"),
        ("TIMETABLE", "Timetable"),
        ("ANNOUNCEMENT", "Announcement"),
        ("HOLIDAY", "Holiday"),
        ("OTHER", "Other"),
    ]

    teacher = models.ForeignKey(
        TeacherProfile,
        on_delete=models.CASCADE,
        related_name="notices"
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    notice_type = models.CharField(max_length=20, choices=NOTICE_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.notice_type})"


class NoticeFile(models.Model):
    notice = models.ForeignKey(
        Notice,
        on_delete=models.CASCADE,
        related_name="files"
    )
    file = models.FileField(upload_to="notices/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name
