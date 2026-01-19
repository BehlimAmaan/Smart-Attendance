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
│   ├── config/               # Django settings, URLs, JWT, DB
│   ├── apps/
│   │   ├── accounts/         # Auth, login, password, face registration
│   │   ├── teachers/         # Teacher controls & reports
│   │   ├── students/         # Student profiles & views
│   │   ├── attendance/       # Attendance sessions & records
│   │   ├── face_liveness/    # Face matching & liveness logic
│   │   └── reports/          # Future analytics
│   ├── anti_spoofing/        # CNN spoof detection model
│   └── tests/                # Experimental CV tests
│
├── frontend/
│   ├── src/
│   │   ├── api/              # Axios JWT handler
│   │   ├── pages/            # Login, dashboards
│   │   ├── components/       # Camera & face capture
│   │   └── styles/
│
├── docs/
├── README.md
└── PROJECT_CONTEXT.txt
```

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

## Author

**Amaan Behlim**
CSE (AI/ML) | Smart Attendance System
Focused on **AI + Backend + Security Engineering**

---

## License

This project is for **educational and research purposes**.
Commercial usage requires proper authorization.




