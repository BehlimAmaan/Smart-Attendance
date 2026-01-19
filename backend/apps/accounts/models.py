from django.contrib.auth.models import AbstractUser
from django.db import models
import pickle


class User(AbstractUser):
    ROLE_CHOICES = (
        ('STUDENT', 'Student'),
        ('TEACHER', 'Teacher'),
    )

    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    face_embedding = models.BinaryField(null=True, blank=True)
    is_first_login = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.username} ({self.role})"
