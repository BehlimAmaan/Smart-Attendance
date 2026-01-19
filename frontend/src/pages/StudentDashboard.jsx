import { useEffect, useState } from "react";
import api from "../api/axios";
import CameraCapture from "../components/CameraCapture";
import StudentTopBar from "../components/student/StudentTopBar";
import AttendanceStatusCard from "../components/student/AttendanceStatusCard";
import { useNavigate } from "react-router-dom";
import AttendanceSummary from "../components/student/AttendanceSummary";
import AttendanceHistory from "../components/student/AttendanceHistory";
import ScanQR from "../components/student/ScanQR";

export default function StudentDashboard() {
  const [session, setSession] = useState(null);
  const [loading, setLoading] = useState(true);
  const [attendanceMarked, setAttendanceMarked] = useState(false);

  const [faceRegistered, setFaceRegistered] = useState(false);
  const [forceReRegister, setForceReRegister] = useState(false);
  const [useQR, setUseQR] = useState(false);

  const navigate = useNavigate();

  // 🔹 Get active attendance session
  useEffect(() => {
    api
      .get("attendance/active/")
      .then((res) => {
        if (res.data.active) {
          setSession(res.data);
        }
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, []);

  // 🔹 Check face registration status
  useEffect(() => {
    api
      .get("accounts/face-status/")
      .then((res) => setFaceRegistered(res.data.face_registered))
      .catch(() => setFaceRegistered(false));
  }, []);

  // 🔹 Reset QR mode if face mismatch forces re-register
  useEffect(() => {
    if (forceReRegister) {
      setUseQR(false);
    }
  }, [forceReRegister]);

  if (loading) {
    return <p className="loading-text">Loading dashboard...</p>;
  }

  return (
    <div className="student-page">
      <StudentTopBar />

      <main className="content">
        {/* STATUS CARD */}
        <AttendanceStatusCard
          session={session}
          marked={attendanceMarked}
        />

        {/* FACE STATUS */}
        <div className="card">
          <h3>Face Status</h3>

          <p>
            Face registration:{" "}
            <b style={{ color: faceRegistered ? "#22c55e" : "#ef4444" }}>
              {faceRegistered ? "Registered" : "Not Registered"}
            </b>
          </p>

          {!faceRegistered && (
            <button onClick={() => navigate("/register-face")}>
              Register Face
            </button>
          )}

          {faceRegistered && (
            <>
              <p className="warning-text">
                Re-registering requires verification.  
                Only the same face can re-register.
              </p>

              <button
                className="btn btn-warning"
                onClick={() => navigate("/register-face")}
              >
                Re-register Face
              </button>
            </>
          )}
        </div>

        {/* ATTENDANCE ACTION */}
        {session && !attendanceMarked && (
          <div className="card">

            {/* MODE SWITCH */}
            {!forceReRegister && (
              <div style={{ marginBottom: "12px" }}>
                <button
                  className={!useQR ? "btn btn-primary" : "btn btn-secondary"}
                  onClick={() => setUseQR(false)}
                  disabled={attendanceMarked}
                >
                  Face Attendance
                </button>

                <button
                  style={{ marginLeft: "10px" }}
                  className={useQR ? "btn btn-primary" : "btn btn-secondary"}
                  onClick={() => setUseQR(true)}
                  disabled={attendanceMarked}
                >
                  Scan QR Instead
                </button>
              </div>
            )}

            {/* FORCE RE-REGISTER */}
            {forceReRegister ? (
              <>
                <p style={{ color: "#ef4444", fontWeight: "bold" }}>
                  🚨 Face mismatch detected
                </p>
                <p>Please re-register your face to continue.</p>

                <button
                  className="btn btn-danger"
                  onClick={() => navigate("/register-face")}
                >
                  Re-register Face
                </button>
              </>
            ) : useQR ? (
              <ScanQR
                sessionId={session.session_id}
                onSuccess={() => setAttendanceMarked(true)}
              />
            ) : !faceRegistered ? (
              <p style={{ color: "#ef4444", fontWeight: "bold" }}>
                ⚠️ Please register your face before marking attendance
              </p>
            ) : (
              <CameraCapture
                sessionId={session.session_id}
                onSuccess={() => setAttendanceMarked(true)}
                onFaceMismatch={() => setForceReRegister(true)}
              />
            )}
          </div>
        )}

        {/* ATTENDANCE SUMMARY */}
        <AttendanceSummary />

        {/* ATTENDANCE HISTORY */}
        <AttendanceHistory />
      </main>
    </div>
  );
}
