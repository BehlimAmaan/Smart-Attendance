from django.urls import path
from .views import (
    LoginAPIView,
    RegisterFaceAPIView,
    ChangePasswordAPIView,
    FaceStatusAPIView,
    ForgotPasswordAPIView,
    ResetPasswordAPIView,
)
urlpatterns = [
    path('login/', LoginAPIView.as_view(), name='login'),
    path("register-face/", RegisterFaceAPIView.as_view()),
    path("change-password/", ChangePasswordAPIView.as_view()),
    path("face-status/", FaceStatusAPIView.as_view()),
    path("forgot-password/", ForgotPasswordAPIView.as_view()),
    path("reset-password/", ResetPasswordAPIView.as_view()),  
]
