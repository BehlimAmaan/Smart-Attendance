import pandas as pd
import secrets
import string

from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.db import transaction

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status

from apps.students.models import StudentProfile
from apps.attendance.models import AttendanceSession, AttendanceRecord

User = get_user_model()



def generate_temp_password(length=8):
    chars = string.ascii_letters + string.digits
    return "".join(secrets.choice(chars) for _ in range(length))


def send_credentials_email(email, password):
    send_mail(
        subject="Your Smart Attendance Login Credentials",
        message=f"""
Hello,

Your student account has been created.

Login details:
Email: {email}
Temporary Password: {password}

IMPORTANT:
- This is a temporary password
- You MUST change it on first login

Login here:
http://localhost:5173/

Regards,
Smart Attendance System
""",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        fail_silently=False,
    )



class BulkStudentUploadAPIView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    REQUIRED_COLUMNS = {
        "roll_no",
        "full_name",
        "email",
        "phone",
        "batch",
        "department",
    }

    def post(self, request):
        if request.user.role != "TEACHER":
            return Response(
                {"detail": "Only teachers can upload students"},
                status=status.HTTP_403_FORBIDDEN,
            )

        file = request.FILES.get("file")
        if not file:
            return Response(
                {"detail": "Excel file is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            df = pd.read_excel(file)
        except Exception:
            return Response(
                {"detail": "Invalid Excel file"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not self.REQUIRED_COLUMNS.issubset(df.columns):
            return Response(
                {
                    "detail": "Invalid Excel format",
                    "required_columns": list(self.REQUIRED_COLUMNS),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        teacher_profile = request.user.teacher_profile

        created = []
        skipped = []

        with transaction.atomic():
            for index, row in df.iterrows():
                email = str(row["email"]).strip().lower()
                roll_no = str(row["roll_no"]).strip()

                if not email or not roll_no:
                    skipped.append(
                        {"row": index + 2, "reason": "Missing email or roll_no"}
                    )
                    continue

                if User.objects.filter(email=email).exists():
                    skipped.append(
                        {"row": index + 2, "reason": "Email already exists"}
                    )
                    continue

                temp_password = generate_temp_password()

                user = User.objects.create_user(
                    username=email,
                    email=email,
                    password=temp_password,
                    role="STUDENT",
                )

                StudentProfile.objects.create(
                    user=user,
                    teacher=teacher_profile,
                    roll_no=roll_no,
                    full_name=row["full_name"],
                    phone=row["phone"],
                    batch=row["batch"],
                    department=row["department"],
                )

                send_credentials_email(email, temp_password)

                created.append(email)

        return Response(
            {
                "students_created": len(created),
                "students_skipped": skipped,
                "email_sent": True,
            },
            status=status.HTTP_201_CREATED,
        )



class AddSingleStudentAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.user.role != "TEACHER":
            return Response(
                {"detail": "Only teachers can add students"},
                status=status.HTTP_403_FORBIDDEN,
            )

        required_fields = [
            "roll_no",
            "full_name",
            "email",
            "phone",
            "batch",
            "department",
        ]

        for field in required_fields:
            if not request.data.get(field):
                return Response(
                    {"detail": f"{field} is required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        email = request.data["email"].strip().lower()
        roll_no = request.data["roll_no"].strip()

        if User.objects.filter(email=email).exists():
            return Response(
                {"detail": "Email already exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        teacher_profile = request.user.teacher_profile
        temp_password = generate_temp_password()

        with transaction.atomic():
            user = User.objects.create_user(
                username=email,
                email=email,
                password=temp_password,
                role="STUDENT",
            )

            StudentProfile.objects.create(
                user=user,
                teacher=teacher_profile,
                roll_no=roll_no,
                full_name=request.data["full_name"],
                phone=request.data["phone"],
                batch=request.data["batch"],
                department=request.data["department"],
            )

            send_credentials_email(email, temp_password)

        return Response(
            {
                "detail": "Student added successfully",
                "email": email,
                "email_sent": True,
            },
            status=status.HTTP_201_CREATED,
        )



class TeacherStudentListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role != "TEACHER":
            return Response(
                {"detail": "Only teachers can view students"},
                status=status.HTTP_403_FORBIDDEN,
            )

        teacher_profile = request.user.teacher_profile

        students = StudentProfile.objects.filter(
            teacher=teacher_profile
        ).select_related("user")

        total_sessions = AttendanceSession.objects.filter(
            teacher=request.user,
            is_active=False,
        ).count()

        student_data = []

        for student in students:
            present_count = AttendanceRecord.objects.filter(
                student=student.user,
                session__teacher=request.user,
            ).count()

            percentage = (
                (present_count / total_sessions) * 100
                if total_sessions > 0
                else 0
            )

            student_data.append(
                {
                    "roll_no": student.roll_no,
                    "full_name": student.full_name,
                    "email": student.user.email,
                    "batch": student.batch,
                    "department": student.department,
                    "present_sessions": present_count,
                    "total_sessions": total_sessions,
                    "attendance_percentage": round(percentage, 2),
                }
            )

        return Response(
            {
                "total_students": students.count(),
                "students": student_data,
            },
            status=status.HTTP_200_OK,
        )



class ExportAttendanceReportAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role != "TEACHER":
            return HttpResponse(status=403)

        teacher = request.user
        teacher_profile = teacher.teacher_profile

        students = StudentProfile.objects.filter(
            teacher=teacher_profile
        ).select_related("user")

        total_sessions = AttendanceSession.objects.filter(
            teacher=teacher,
            is_active=False,
        ).count()

        report_rows = []

        for student in students:
            present_count = AttendanceRecord.objects.filter(
                student=student.user,
                session__teacher=teacher,
            ).count()

            percentage = (
                (present_count / total_sessions) * 100
                if total_sessions > 0
                else 0
            )

            report_rows.append(
                {
                    "Roll No": student.roll_no,
                    "Full Name": student.full_name,
                    "Email": student.user.email,
                    "Batch": student.batch,
                    "Department": student.department,
                    "Present Sessions": present_count,
                    "Total Sessions": total_sessions,
                    "Attendance Percentage": round(percentage, 2),
                }
            )

        df = pd.DataFrame(report_rows)
        file_format = request.GET.get("format", "excel")

        if file_format == "csv":
            response = HttpResponse(content_type="text/csv")
            response["Content-Disposition"] = (
                'attachment; filename="attendance_report.csv"'
            )
            df.to_csv(response, index=False)
            return response

        response = HttpResponse(
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        response["Content-Disposition"] = (
            'attachment; filename="attendance_report.xlsx"'
        )

        with pd.ExcelWriter(response, engine="openpyxl") as writer:
            df.to_excel(writer, index=False, sheet_name="Attendance Report")

        return response



class TeacherProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role != "TEACHER":
            return Response(status=403)

        teacher = request.user.teacher_profile

        return Response(
            {
                "name": request.user.username,
                "email": request.user.email,
                "department": teacher.department,
            }
        )

    def put(self, request):
        if request.user.role != "TEACHER":
            return Response(status=403)

        user = request.user
        teacher = user.teacher_profile

        user.username = request.data.get("name", user.username)
        teacher.department = request.data.get(
            "department", teacher.department
        )

        user.save()
        teacher.save()

        return Response(
            {"detail": "Profile updated successfully"},
            status=status.HTTP_200_OK,
        )
