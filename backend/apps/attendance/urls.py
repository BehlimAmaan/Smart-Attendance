from django.urls import path
from .views import (
    StartAttendanceSessionAPIView,
    EndAttendanceSessionAPIView,
    MarkAttendanceAPIView,
)
from .views import GenerateQRTokenAPIView, ActiveAttendanceSessionAPIView, LiveAttendanceAPIView


urlpatterns = [
    path("start/", StartAttendanceSessionAPIView.as_view()),
    path("end/<int:session_id>/", EndAttendanceSessionAPIView.as_view()),
    path("mark/", MarkAttendanceAPIView.as_view()),
    path("qr/", GenerateQRTokenAPIView.as_view(), name="generate-qr"),
    path("active/", ActiveAttendanceSessionAPIView.as_view()),
    path("live/", LiveAttendanceAPIView.as_view()),
]
