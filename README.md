# Smart Attendance System 🚀

**Face Recognition + Liveness Detection Based Attendance Platform**

## Overview

Smart Attendance is a **secure, AI-powered attendance management system** designed for educational institutions.
It uses **face recognition**, **liveness detection**, and **anti-spoofing techniques** to prevent proxy attendance and ensure authenticity.

The system supports **role-based access** for Teachers and Students and provides a **QR-code fallback mechanism** when camera-based attendance fails.

This project is built with **Django + React** and follows **industry-level backend architecture**.

---

## Key Features

### Teacher Features

* Secure registration and login using JWT authentication
* Bulk student registration using Excel upload
* Start and end attendance sessions
* Live attendance monitoring
* Face-based attendance marking
* Auto-refreshing QR code (changes every 5 seconds) as fallback
* View and export attendance reports
* Full control over attendance sessions

### Student Features

* Secure login
* Face registration (one-time or controlled)
* Mark attendance using face recognition with liveness detection
* QR-based attendance if camera fails
* View attendance history and summary
* Change password securely

---

## Security & AI Capabilities

* **Face Recognition** for identity verification
* **Liveness Detection** (blink, head movement, facial cues)
* **CNN-based Anti-Spoofing** to prevent photo/video attacks
* **JWT Authentication with Auto Token Refresh**
* **Role-Based Access Control (RBAC)**

---

## Tech Stack

### Backend

* Python
* Django & Django REST Framework
* PostgreSQL
* JWT Authentication
* OpenCV
* PyTorch (Anti-spoofing CNN)

### Frontend

* React (Vite)
* Axios (JWT + Auto Refresh)
* MediaPipe (Face & landmarks)
* HTML, CSS, JavaScript

---

## Project Structure

```
Smart-Attendance/
│
├── backend/
│   │
│   ├── manage.py
│   ├── requirements.txt
│   ├── blink_detection_task_test.py
│   ├── face_detection_test.py
│   ├── head_movement_task_test.py
│   ├── test_spoof_detection.py
│   │
│   ├── config/
│   │   ├── __init__.py
│   │   ├── asgi.py
│   │   ├── settings.py          # PostgreSQL, JWT, AUTH_USER_MODEL
│   │   ├── urls.py              # Main API routing
│   │   └── wsgi.py
│   │
│   ├── apps/
│   │   │
│   │   ├── accounts/            # AUTH & SECURITY
│   │   │   ├── __init__.py
│   │   │   ├── admin.py
│   │   │   ├── apps.py
│   │   │   ├── models.py        # Custom User (role, face_embedding, is_first_login)
│   │   │   ├── serializers.py   # Login (email-based)
│   │   │   ├── forms.py 
│   │   │   ├── views.py         # Login, ChangePassword, RegisterFace
│   │   │   ├── urls.py
│   │   │   └── migrations/
│   │   │
│   │   ├── teachers/            # TEACHER DOMAIN
│   │   │   ├── __init__.py
│   │   │   ├── apps.py
│   │   │   ├── models.py        # TeacherProfile
│   │   │   ├── views.py         # Bulk upload, Add single student,
│   │   │   ├── signals.py
│   │   │   ├── serializers.py                 
│   │   │   ├── urls.py
│   │   │   └── migrations/
│   │   │
│   │   ├── students/            # STUDENT DOMAIN
│   │   │   ├── __init__.py
│   │   │   ├── apps.py
│   │   │   ├── models.py        # StudentProfile (linked to TeacherProfile)
│   │   │   ├── views.py         # (attendance summary & history – next)
│   │   │   ├── urls.py
│   │   │   └── migrations/
│   │   │
│   │   ├── attendance/          # ATTENDANCE ENGINE
│   │   │   ├── __init__.py
│   │   │   ├── admin.py
│   │   │   ├── apps.py
│   │   │   ├── models.py        
│   │   │   ├── serializers.py
│   │   │   ├── views.py         
│   │   │   ├── urls.py
│   │   │   └── migrations/
│   │   │
│   │   ├── face_liveness/       # LIVENESS & FACE MATCHING
│   │   │   ├── __init__.py
│   │   │   ├── apps.py
│   │   │   ├── liveness_engine.py
│   │   │   ├── face_matcher.py
│   │   │   └── views.py
│   │   │
│   │   ├── qr_attendance/       # (LOGIC MOVED INTO attendance)
│   │   │   ├── apps.py
│   │   │   ├── models.py        
│   │   │   ├── views.py         
│   │   │   ├── urls.py
│   │   │
│   │   ├── reports/             # FUTURE EXTENSIONS
│   │   │   ├── __init__.py
│   │   │   ├── apps.py
│   │   │   ├── models.py        
│   │   │   ├── views.py         
│   │   │   ├── urls.py
│   │   │   ├── test.py
│   │   │   └── migrations/
│   │
│   ├── anti_spoofing/            # CNN SPOOF DETECTION
│   │   ├── spoof_detector.py
│   │   ├── model.py
│   |	  ├── test_spoof.py
│   │   └── 2.7_80x80_MiniFASNetV2.pth
│   │
│   └── tests/                    # EXPERIMENTAL TESTS
│       ├── blink_detection_task_test.py
│       ├── face_detection_test.py
│       ├── head_movement_task_test.py
│       └── test_spoof_detection.py
│
├── frontend/
│   │
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   │
│   ├── src/
│   │   ├── main.jsx
│   │   ├── App.jsx               # Routes (login, dashboards, change-password)
│   │   ├── index.css
│   │   ├── App.jsx
│   │   │
│   │   ├── api/
│   │   │   └── axios.js           # JWT + auto refresh
│   │   │
│   │   ├── pages/
│   │   │   ├── Login.jsx
│   │   │   ├── Login.css
│   │   │   ├── ForgotPassword.jsx
│   │   │   ├── EditTeachersProfile.jsx
│   │   │   ├── ChangePassword.jsx
│   │   │   ├── TeacherDashboard.jsx
│   │   │   ├── TeacherDashboard.css
│   │   │   ├── ResetPassword.jsx
│   │   │   ├── StudentDashboard.jsx   
│   │   │   └── AddStudent.jsx
│   │   │
│   │   ├──auth/
│   │   │   └── login.jsx
│   │   │
│   │   ├──components/
│   │   │   |
│   │   │   ├── student/
│   │   │   ├── AttendanceHistory.jsx
│   │   │   ├── AttendanceStatusCard.jsx
│   │   │   ├── AttendanceSummary.jsx
│   │   │   ├── ScanQR.jsx
│   │   │   └── StudentTopBar.jsx
│   │   │   │
│   │   │   ├── AlertsBanner.jsx
│   │   │   ├── AttendanceControls.jsx
│   │   │   ├── AttendanceStatus.jsx
│   │   │   ├── CameraCapture.jsx
│   │   │   ├── LiveAttendanceTable.jsx
│   │   │   ├── RegisterFace.jsx
│   │   │   ├── ReportsSection.jsx
│   │   │   ├── StudentManagement.jsx
│   │   │   ├── StudentTopBar.jsx
│   │   │   └── TeacherTopBar.jsx
│   │   │
│   │   └── styles/
│   │       └── common.css         # Shared UI polish
│
├── docs/
│
├── README.md
└── PROJECT_CONTEXT.txt


---

## Attendance Flow (Simplified)

1. Teacher starts an attendance session
2. Student logs in and opens camera
3. Face detection + liveness check performed
4. Anti-spoofing model validates authenticity
5. Face matched with registered embedding
6. Attendance marked successfully
7. QR code used if camera fails

---

## Installation & Setup

### Backend Setup

```
cd backend
python -m venv venv
venv\Scripts\activate   (Windows)
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### Frontend Setup

```
cd frontend
npm install
npm run dev
```

---

## Environment Variables

Create a `.env` file in backend:

```
SECRET_KEY=your_secret_key
DEBUG=True
DATABASE_URL=postgresql://user:password@localhost/dbname
```

---

## Future Enhancements

* Subject-wise attendance
* Graphical attendance analytics
* Email & notification alerts
* Mobile app integration
* Cloud deployment (Docker + Nginx)
* Multi-institution support

---

## Use Case

This project is suitable for:

* Colleges and Universities
* Schools
* Training Institutes
* Secure examination attendance

---

Author

Amaan Behlim
CSE (AI/ML) | Smart Attendance System
Focused on **AI + Backend + Security Engineering**

---

## License

This project is for **educational and research purposes**.
Commercial usage requires proper authorization.




