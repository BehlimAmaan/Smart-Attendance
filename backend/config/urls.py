from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/accounts/", include("apps.accounts.urls")),
    path("api/attendance/", include("apps.attendance.urls")),
    path("api/teachers/", include("apps.teachers.urls")),
    path("api/qr/", include("apps.qr_attendance.urls")),
    path("api/students/", include("apps.students.urls")),
]
