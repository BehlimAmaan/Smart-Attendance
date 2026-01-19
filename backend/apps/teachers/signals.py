from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.accounts.models import User
from .models import TeacherProfile


@receiver(post_save, sender=User)
def create_teacher_profile(sender, instance, created, **kwargs):
    if created and instance.role == "TEACHER":
        TeacherProfile.objects.get_or_create(user=instance)
