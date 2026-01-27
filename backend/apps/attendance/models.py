from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta

User = settings.AUTH_USER_MODEL


# ATTENDANCE SESSION
class AttendanceSession(models.Model):
    teacher = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="attendance_sessions"
    )
    subject = models.CharField(max_length=100)

    # GEOFENCING
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    radius_meters = models.PositiveIntegerField(default=150)

    # TIME CONTROL
    duration_minutes = models.PositiveIntegerField()
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField()

    is_active = models.BooleanField(default=True)

    def has_expired(self):
        return timezone.now() > self.end_time

    def __str__(self):
        return f"{self.subject} ({self.teacher})"


# ATTENDANCE RECORD
class AttendanceRecord(models.Model):
    METHOD_CHOICES = (
        ("FACE", "Face"),
        ("QR", "QR Code"),
    )

    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="attendance_records"
    )

    session = models.ForeignKey(
        AttendanceSession,
        on_delete=models.CASCADE,
        related_name="records"
    )

    method = models.CharField(
        max_length=10,
        choices=METHOD_CHOICES
    )

    marked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["student", "session"],
                name="unique_attendance_per_student_per_session"
            )
        ]

    def __str__(self):
        return f"{self.student} - {self.session.subject}"


# QR TOKEN
class QRToken(models.Model):
    session = models.ForeignKey(
        AttendanceSession,
        on_delete=models.CASCADE,
        related_name="qr_tokens"
    )

    token = models.CharField(max_length=64, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)

    def is_expired(self):
        return timezone.now() > self.created_at + timedelta(seconds=5)
