from django.urls import path
from .views import (
    StudentAttendanceSummaryAPIView,
    StudentAttendanceHistoryAPIView
)

urlpatterns = [
    path(
        "attendance-summary/",
        StudentAttendanceSummaryAPIView.as_view()
    ),
    path(
        "attendance-history/",
        StudentAttendanceHistoryAPIView.as_view()
    ),
]
