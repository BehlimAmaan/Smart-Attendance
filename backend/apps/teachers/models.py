from django.db import models
from django.conf import settings


class TeacherProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="teacher_profile"
    )
    department = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username
