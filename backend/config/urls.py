from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/accounts/", include("apps.accounts.urls")),
    path("api/attendance/", include("apps.attendance.urls")),
    path("api/teachers/", include("apps.teachers.urls")),
    path("api/qr/", include("apps.qr_attendance.urls")),
    path("api/students/", include("apps.students.urls")),
    path("api/notices/", include("apps.notices.urls")),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
