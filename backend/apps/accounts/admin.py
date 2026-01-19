from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.conf import settings

from .models import User
from .forms import AdminTeacherCreationForm


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    add_form = AdminTeacherCreationForm
    model = User

    list_display = ("email", "role", "is_staff", "is_active")
    list_filter = ("role", "is_active")

    ordering = ("email",)
    search_fields = ("email",)

    fieldsets = (
        (None, {"fields": ("email",)}),
        ("Role", {"fields": ("role",)}),
        ("Status", {"fields": ("is_active",)}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "role"),
        }),
    )

    def save_model(self, request, obj, form, change):
        if not change:
            # Login ID = email
            obj.username = obj.email
            obj.is_staff = True
            obj.is_first_login = True

            # Generate temp password
            temp_password = get_random_string(10)
            obj.set_password(temp_password)

            obj.save()

            # Send credentials
            send_mail(
                subject="Your Smart Attendance Teacher Account",
                message=(
                    "Your teacher account has been created.\n\n"
                    f"Login ID (Email): {obj.email}\n"
                    f"Temporary Password: {temp_password}\n\n"
                    "Please login and change your password immediately."
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[obj.email],
                fail_silently=False,
            )
        else:
            obj.save()
