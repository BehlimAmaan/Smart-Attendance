from django.urls import path
from .views import BulkStudentUploadAPIView, AddSingleStudentAPIView, TeacherStudentListAPIView, ExportAttendanceReportAPIView, TeacherProfileAPIView

urlpatterns = [
    path("upload-students/", BulkStudentUploadAPIView.as_view()),
    path("add-student/", AddSingleStudentAPIView.as_view()),
    path("students/", TeacherStudentListAPIView.as_view()),
    path("attendance-report/", ExportAttendanceReportAPIView.as_view()),
    path("profile/", TeacherProfileAPIView.as_view()),

]
