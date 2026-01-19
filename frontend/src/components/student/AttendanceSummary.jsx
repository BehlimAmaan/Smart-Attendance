import { useEffect, useState } from "react";
import api from "../../api/axios";

export default function AttendanceSummary() {
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api
      .get("students/attendance-summary/")
      .then((res) => {
        setSummary(res.data);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <div className="card">
        <p>Loading attendance summary...</p>
      </div>
    );
  }

  if (!summary) {
    return null;
  }

return (
    
  <div className="card full-width">
    <h3>My Attendance Summary</h3>

    <p><b>Total Classes:</b> {summary.total_sessions}</p>
    <p><b>Classes Attended:</b> {summary.present_sessions}</p>
    <p>
      <b>Attendance Percentage:</b>{" "}
      <span
        style={{
          color: summary.attendance_percentage < 75 ? "red" : "green",
          fontWeight: "bold",
        }}
      >
        {summary.attendance_percentage}%
      </span>
    </p>
  </div>
);

}
