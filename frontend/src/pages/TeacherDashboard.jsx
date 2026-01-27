import { useState, useEffect } from "react";
import api from "../api/axios";
import { QRCodeCanvas } from "qrcode.react";
import "./TeacherDashboard.css";
import NoticePanel from "../components/NoticePanel";

export default function TeacherDashboard() {
  const [subject, setSubject] = useState("");
  const [className, setClassName] = useState("");
  const [semester, setSemester] = useState("");
  const [duration, setDuration] = useState(10);
  const [session, setSession] = useState(null);
  const [file, setFile] = useState(null);
  const [uploadResult, setUploadResult] = useState(null);
  const [qrToken, setQrToken] = useState(null);
  const [liveData, setLiveData] = useState(null);
  const [students, setStudents] = useState([]);
  const [locationStatus, setLocationStatus] = useState("idle");
  const [remainingSeconds, setRemainingSeconds] = useState(null);

  /* ---------------- GET LOCATION ---------------- */
  const getLocation = () => {
    return new Promise((resolve, reject) => {
      if (!navigator.geolocation) {
        setLocationStatus("error");
        reject(new Error("Geolocation not supported"));
        return;
      }

      setLocationStatus("loading");

      navigator.geolocation.getCurrentPosition(
        (pos) => {
          setLocationStatus("success");
          resolve(pos.coords);
        },
        () => {
          setLocationStatus("error");
          reject(new Error("Location permission denied"));
        },
        {
          enableHighAccuracy: true,
          maximumAge: 0,
          timeout: 10000,
        }
      );
    });
  };
  /* ---------------- START SESSION ---------------- */
  const startSession = async () => {
    if (!subject || !className || !semester) {
      alert("Please fill subject, class and semester");
      return;
    }
    try {
      const coords = await getLocation();

      const res = await api.post("attendance/start/", {
        subject,
        latitude: coords.latitude,
        longitude: coords.longitude,
        radius: 150,
        duration_minutes: duration,
      });

      setSession(res.data);
      setRemainingSeconds(res.data.remaining_seconds);
    } catch (err) {
      alert(
        err.message ||
        err.response?.data?.detail ||
        "Failed to start session"
      );
    }
  };

  /* ---------------- END SESSION ---------------- */
  const endSession = async () => {
    try {
      await api.post(`attendance/end/${session.id}/`);
      setSession(null);
      setQrToken(null);
      setLiveData(null);
    } catch {
      alert("Failed to end session");
    }
  };

  /* ---------------- BULK UPLOAD ---------------- */
  const uploadStudents = async () => {
    if (!file) {
      alert("Please select an Excel file");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await api.post(
        "teachers/upload-students/",
        formData,
        { headers: { "Content-Type": "multipart/form-data" } }
      );
      setUploadResult(res.data);
      alert("Students uploaded successfully");
    } catch {
      alert("Upload failed");
    }
  };

  const downloadAttendanceReport = async () => {
    try {
      const response = await api.get("teachers/attendance-report/", {
        responseType: "blob",
      });

      const blob = new Blob([response.data], {
        type:
          "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
      });

      const url = window.URL.createObjectURL(blob);
      const link = document.createElement("a");

      link.href = url;
      link.download = "attendance_report.xlsx";
      document.body.appendChild(link);
      link.click();

      link.remove();
      window.URL.revokeObjectURL(url);
    } catch {
      alert("❌ Failed to download report");
    }
  };

  /* ---------------- QR CODE ---------------- */
  useEffect(() => {
    if (!session) return;

    const fetchQR = async () => {
      const res = await api.get("attendance/qr/");
      setQrToken(res.data.qr_token);
    };

    fetchQR();
    const interval = setInterval(fetchQR, 5000);
    return () => clearInterval(interval);
  }, [session]);

  /* ---------------- LIVE ATTENDANCE ---------------- */
  useEffect(() => {
    if (!session) return;

    const fetchLive = async () => {
      try {
        const res = await api.get("attendance/live/");
        setLiveData(res.data);

      } catch {
        setLiveData(null);
      }
    };

    fetchLive(); // initial call
    const interval = setInterval(fetchLive, 3000);

    return () => clearInterval(interval);
  }, [session]);

  /* ---------------- STUDENT LIST ---------------- */
  useEffect(() => {
    api.get("teachers/students/")
      .then((res) => setStudents(res.data.students))
      .catch(() => {});
  }, []);

  useEffect(() => {
    if (remainingSeconds === null) return;

    const timer = setInterval(() => {
      setRemainingSeconds((prev) => {
        if (prev === null) return prev;
        if (prev <= 1) {
          clearInterval(timer);
          return 0;
        }
        return prev - 1;
      });
    }, 1000);

    return () => clearInterval(timer);
  }, [remainingSeconds !== null]);

  useEffect(() => {
    if (remainingSeconds === 0) {
      alert("⏱ Attendance session has ended automatically");

      setSession(null);
      setQrToken(null);
      setLiveData(null);
    }
  }, [remainingSeconds]);

  /* ---------------- UI ---------------- */
  return (
    <div className="teacher-page">
      {/* TOP BAR */}
      <header className="top-bar">
        <div className="top-left">Smart Attendance</div>
        <div className="top-center">Teacher Dashboard</div>

        <div className="top-right">
          <div className="profile-actions">
            <button
              className="btn btn-secondary"
              onClick={() => (window.location.href = "/teacher/profile")}
            >
              👤 Edit Profile
            </button>

            <button
              className="btn btn-secondary"
              onClick={() => (window.location.href = "/change-password")}
            >
              🔒 Change Password
            </button>
          </div>

          <button
            className="btn btn-danger"
            onClick={() => {
              localStorage.clear();
              window.location.href = "/";
            }}
          >
            🚪 Logout
          </button>
        </div>
      </header>

      <main className="content">
        {/* ALERTS */}
        {students.length === 0 && (
          <div className="alert warning">
            ⚠️ No students uploaded yet. Please upload student data to start attendance sessions.
          </div>
        )}

        {session && liveData && liveData.present_count === 0 && (
          <div className="alert info">
            ℹ️ Attendance session is active but no student has marked attendance yet.
          </div>
        )}

        {/* BULK STUDENT UPLOAD */}
        <div className="card">
          <h3>Bulk Student Upload</h3>
          <input
            type="file"
            accept=".xlsx, .xls"
            onChange={(e) => setFile(e.target.files[0])}
          />
          <button onClick={uploadStudents}>📤 Upload Excel File</button>
          {uploadResult && (
            <div style={{marginTop: '15px', padding: '12px', background: 'rgba(16, 185, 129, 0.1)', borderRadius: '8px'}}>
              ✅ <strong>{uploadResult.students_created}</strong> students created successfully
            </div>
          )}
        </div>
        
        {/* NOTICE PANEL */}
        <NoticePanel />

        {/* START / END ATTENDANCE */}
        <div className={`card ${session ? 'session-active' : ''}`}>
          {!session ? (
            <>
              <h3>Start Attendance Session</h3>
              <div className={`location-indicator location-${locationStatus}`}>
                {locationStatus === "idle" && "📍 Location not checked yet"}
                {locationStatus === "loading" && "⏳ Fetching location..."}
                {locationStatus === "success" && "✅ Location detected"}
                {locationStatus === "error" && "❌ Location permission denied"}
              </div>

              <input
                placeholder="Enter Subject Name"
                value={subject}
                onChange={(e) => setSubject(e.target.value)}
              />
              <input
                placeholder="Class / Division (e.g. CSE-A)"
                value={className}
                onChange={(e) => setClassName(e.target.value)}
              />
              <input
                placeholder="Semester (e.g. Sem 6)"
                value={semester}
                onChange={(e) => setSemester(e.target.value)}
              />
              <input
                type="number"
                min="1"
                placeholder="Session Duration (minutes)"
                value={duration}
                onChange={(e) => setDuration(e.target.value)}
              />
              <button className="primary" onClick={startSession}>
                ▶️ Start Attendance Session
              </button>
            </>
          ) : (
            <>
              <h3>Attendance Session Active</h3>
              <div className="status-box">
                <p style={{color: '#10b981', fontSize: '16px', fontWeight: 'bold'}}>
                  🟢 LIVE ATTENDANCE RUNNING
                </p>
                <p>
                  <b>Subject:</b> {session.subject}
                </p>
                {remainingSeconds !== null && (
                  <p style={{ fontWeight: "bold", color: "#f59e0b" }}>
                    ⏳ Time left: {Math.floor(remainingSeconds / 60)}:
                    {(remainingSeconds % 60).toString().padStart(2, "0")}
                  </p>
                )}


                {liveData && (
                  <p>
                    <b>Attendance:</b> {liveData.present_count} /{" "}
                    {liveData.total_students} students
                  </p>
                )}
              </div>

              <button className="danger" onClick={endSession}>
                ⏹️ End Session
              </button>

              {qrToken && (
                <div className="qr-box">
                  <p>Scan this QR Code to mark attendance (Auto-refreshes every 5s)</p>
                  <div style={{background: 'white', padding: '15px', borderRadius: '12px', display: 'inline-block'}}>
                    <QRCodeCanvas value={qrToken} size={180} />
                  </div>
                </div>
              )}
            </>
          )}
        </div>

        {/* LIVE ATTENDANCE */}
        {liveData?.active && (
          <div className="card full-width">
            <h3>Live Attendance Tracking</h3>
            <div className="table-container">
              <table className="table">
                <thead>
                  <tr>
                    <th>Roll No</th>
                    <th>Student Name</th>
                    <th>Marked At</th>
                    <th>Method</th>
                    <th>Status</th>
                  </tr>
                </thead>
                <tbody>
                  {liveData.present_students.map((s) => (
                    <tr key={s.roll_no}>
                      <td>{s.roll_no}</td>
                      <td>{s.full_name}</td>
                      <td>{s.marked_at}</td>
                      <td>
                        <span style={{
                          padding: '4px 12px',
                          borderRadius: '20px',
                          fontSize: '12px',
                          fontWeight: '600',
                          background: s.method === 'QR' ? 'rgba(99, 102, 241, 0.2)' : 'rgba(16, 185, 129, 0.2)',
                          color: s.method === 'QR' ? '#818cf8' : '#10b981'
                        }}>
                          {s.method}
                        </span>
                      </td>
                      <td>
                        <span style={{
                          padding: '4px 12px',
                          borderRadius: '20px',
                          fontSize: '12px',
                          fontWeight: '600',
                          background: 'rgba(16, 185, 129, 0.2)',
                          color: '#10b981'
                        }}>
                          ✅ Present
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {/* STUDENT LIST */}
        <div className="card full-width">
          <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px'}}>
            <h3 style={{margin: 0}}>My Students</h3>
            <div style={{display: 'flex', gap: '12px'}}>
              <button 
                onClick={() => (window.location.href = "/add-student")}
                style={{width: 'auto', padding: '10px 20px'}}
              >
                ➕ Add Student
              </button>
              <button 
                onClick={() => {}}
                style={{width: 'auto', padding: '10px 20px', background: 'linear-gradient(135deg, #8b5cf6, #7c3aed)'}}
              >
                🔄 Refresh List
              </button>
            </div>
          </div>
          
          <div className="table-container">
            <table className="table">
              <thead>
                <tr>
                  <th>Roll No</th>
                  <th>Student Name</th>
                  <th>Email Address</th>
                  <th>Attendance %</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                {students.map((s) => (
                  <tr key={s.roll_no}>
                    <td>
                      <span style={{
                        padding: '4px 8px',
                        background: 'rgba(99, 102, 241, 0.1)',
                        borderRadius: '6px',
                        fontWeight: '600'
                      }}>
                        {s.roll_no}
                      </span>
                    </td>
                    <td>{s.full_name}</td>
                    <td>{s.email}</td>
                    <td>
                      <div style={{display: 'flex', alignItems: 'center', gap: '10px'}}>
                        <div style={{
                          flex: 1,
                          height: '8px',
                          background: 'rgba(255, 255, 255, 0.1)',
                          borderRadius: '4px',
                          overflow: 'hidden'
                        }}>
                          <div style={{
                            width: `${s.attendance_percentage}%`,
                            height: '100%',
                            background: s.attendance_percentage > 75 ? '#10b981' : 
                                      s.attendance_percentage > 50 ? '#f59e0b' : '#ef4444',
                            borderRadius: '4px'
                          }}></div>
                        </div>
                        <span style={{
                          fontWeight: '600',
                          color: s.attendance_percentage > 75 ? '#10b981' : 
                                s.attendance_percentage > 50 ? '#f59e0b' : '#ef4444'
                        }}>
                          {s.attendance_percentage}%
                        </span>
                      </div>
                    </td>
                    <td>
                      <span style={{
                        padding: '4px 12px',
                        borderRadius: '20px',
                        fontSize: '12px',
                        fontWeight: '600',
                        background: s.attendance_percentage > 75 ? 'rgba(16, 185, 129, 0.2)' : 
                                  s.attendance_percentage > 50 ? 'rgba(245, 158, 11, 0.2)' : 'rgba(239, 68, 68, 0.2)',
                        color: s.attendance_percentage > 75 ? '#10b981' : 
                              s.attendance_percentage > 50 ? '#f59e0b' : '#ef4444'
                      }}>
                        {s.attendance_percentage > 75 ? 'Good' : 
                         s.attendance_percentage > 50 ? 'Average' : 'Low'}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          <p style={{marginTop: '15px', color: '#94a3b8', fontSize: '14px'}}>
            Total: <strong>{students.length}</strong> students
          </p>
        </div>

        {/* SUMMARY & REPORTS */}
        <div className="card">
          <h3>Attendance Summary</h3>
          <div style={{
            display: 'grid',
            gridTemplateColumns: '1fr 1fr',
            gap: '15px',
            marginTop: '20px'
          }}>
            <div style={{
              background: 'rgba(15, 23, 42, 0.7)',
              padding: '20px',
              borderRadius: '12px',
              textAlign: 'center'
            }}>
              <div style={{fontSize: '32px', fontWeight: 'bold', color: '#60a5fa'}}>
                {students.length}
              </div>
              <div style={{color: '#94a3b8', marginTop: '5px'}}>Total Students</div>
            </div>
            <div style={{
              background: 'rgba(15, 23, 42, 0.7)',
              padding: '20px',
              borderRadius: '12px',
              textAlign: 'center'
            }}>
              <div style={{fontSize: '32px', fontWeight: 'bold', color: '#10b981'}}>
                {students.length
                  ? Math.round(
                      students.reduce(
                        (a, s) => a + s.attendance_percentage,
                        0
                      ) / students.length
                    )
                  : 0}%
              </div>
              <div style={{color: '#94a3b8', marginTop: '5px'}}>Avg Attendance</div>
            </div>
          </div>
        </div>

        {/* REPORTS */}
        <div className="card">
          <h3>Reports & Analytics</h3>
          <div style={{display: 'flex', flexDirection: 'column', gap: '12px', marginTop: '15px'}}>
            <button onClick={downloadAttendanceReport}>
              📥 Download Attendance Report (Excel)
            </button>
            <button style={{background: 'linear-gradient(135deg, #8b5cf6, #7c3aed)'}}>
              📈 View Detailed Analytics
            </button>
            <button style={{background: 'linear-gradient(135deg, #f59e0b, #d97706)'}}>
              📅 Generate Monthly Report
            </button>
          </div>
        </div>
      </main>
    </div>
  );
}