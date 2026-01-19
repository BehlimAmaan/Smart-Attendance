from django.urls import path
from .views import GenerateQRAPIView, MarkAttendanceViaQRAPIView

urlpatterns = [
    path("generate/", GenerateQRAPIView.as_view()),
    path("mark/", MarkAttendanceViaQRAPIView.as_view()),
]
