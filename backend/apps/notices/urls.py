from django.urls import path
from .views import TeacherNoticeView, StudentNoticeView

urlpatterns = [
    path("teacher/", TeacherNoticeView.as_view()),
    path("teacher/<int:notice_id>/", TeacherNoticeView.as_view()),
    path("student/", StudentNoticeView.as_view()),
]
