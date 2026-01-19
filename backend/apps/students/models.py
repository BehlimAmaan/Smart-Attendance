from django.db import models
from django.conf import settings


class StudentProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="student_profile"
    )
    teacher = models.ForeignKey(
        "teachers.TeacherProfile",
        on_delete=models.CASCADE,
        related_name="students"
    )
    roll_no = models.CharField(max_length=50)
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    batch = models.CharField(max_length=50)
    department = models.CharField(max_length=100)

    class Meta:
        unique_together = ("teacher", "roll_no")

    def __str__(self):
        return f"{self.roll_no} - {self.full_name}"
