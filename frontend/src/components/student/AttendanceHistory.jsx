import { useEffect, useState } from "react";
import api from "../../api/axios";

export default function AttendanceHistory() {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api
      .get("students/attendance-history/")
      .then((res) => {
        setHistory(res.data.history || []);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <div className="card">
        <p>Loading attendance history...</p>
      </div>
    );
  }

  if (history.length === 0) {
    return (
      <div className="card">
        <h3>Attendance History</h3>
        <p>No attendance records found.</p>
      </div>
    );
  }

  return (
    <div className="card full-width">
      <h3>Attendance History</h3>

      <table className="table">
        <thead>
          <tr>
            <th>Date</th>
            <th>Subject</th>
            <th>Status</th>
            <th>Method</th>
          </tr>
        </thead>
        <tbody>
          {history.map((row, index) => (
            <tr key={index}>
              <td>{row.date}</td>
              <td>{row.subject}</td>
              <td
                style={{
                  color: row.status === "Present" ? "green" : "red",
                  fontWeight: "bold",
                }}
              >
                {row.status}
              </td>
              <td>{row.method}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
