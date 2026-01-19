from django.db import models
from django.utils import timezone
import uuid


class QRToken(models.Model):
    token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    session_id = models.IntegerField()
    expires_at = models.DateTimeField()

    def is_valid(self):
        return timezone.now() < self.expires_at

    def __str__(self):
        return f"QRToken({self.token})"
