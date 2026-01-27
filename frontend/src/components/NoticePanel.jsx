import { useEffect, useState } from "react";
import api from "../api/axios";

const BACKEND_URL = "http://127.0.0.1:8000";

export default function NoticePanel() {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [type, setType] = useState("ANNOUNCEMENT");
  const [files, setFiles] = useState([]);
  const [notices, setNotices] = useState([]);

  const loadNotices = () => {
    api.get("notices/teacher/")
      .then(res => setNotices(res.data))
      .catch(() => {});
  };

  useEffect(() => {
    loadNotices();
  }, []);

  const submitNotice = async () => {
    if (!title || files.length === 0) {
      alert("Title and at least one file are required");
      return;
    }

    const form = new FormData();
    form.append("title", title);
    form.append("description", description);
    form.append("notice_type", type);
    files.forEach(f => form.append("files", f));

    await api.post("notices/teacher/", form);
    alert("✅ Notice uploaded");

    setTitle("");
    setDescription("");
    setFiles([]);
    loadNotices();
  };

  const deleteNotice = async (id) => {
    const confirmDelete = window.confirm(
      "Are you sure you want to delete this notice?"
    );

    if (!confirmDelete) return;

    try {
      await api.delete(`notices/teacher/${id}/`);
      alert("🗑️ Notice deleted");
      loadNotices();
    } catch {
      alert("❌ Failed to delete notice");
    }
  };

  return (
    <div className="card full-width">
      <h3>📢 Notices</h3>

      <input
        placeholder="Title"
        value={title}
        onChange={e => setTitle(e.target.value)}
      />

      <textarea
        placeholder="Description"
        value={description}
        onChange={e => setDescription(e.target.value)}
      />

      <select value={type} onChange={e => setType(e.target.value)}>
        <option value="ATTENDANCE">Attendance Sheet</option>
        <option value="EXAM">Exam / Marks</option>
        <option value="TIMETABLE">Timetable</option>
        <option value="ANNOUNCEMENT">Announcement</option>
        <option value="HOLIDAY">Holiday</option>
        <option value="OTHER">Other</option>
      </select>

      <input
        type="file"
        multiple
        onChange={e => setFiles([...e.target.files])}
      />

      <button onClick={submitNotice}>📤 Upload Notice</button>

      <hr />

      {notices.map(n => (
        <div
          key={n.id}
          style={{
            marginTop: "14px",
            padding: "10px",
            border: "1px solid rgba(255,255,255,0.1)",
            borderRadius: "8px"
          }}
        >
          <div style={{ display: "flex", justifyContent: "space-between" }}>
            <b>{n.title}</b>
            <button
              onClick={() => deleteNotice(n.id)}
              style={{
                background: "#ef4444",
                color: "white",
                padding: "4px 10px",
                borderRadius: "6px",
                fontSize: "12px"
              }}
            >
              🗑 Delete
            </button>
          </div>

          <p style={{ marginTop: "4px", color: "#94a3b8" }}>
            {n.notice_type}
          </p>

          <ul>
            {n.files.map(f => (
              <li key={f.id}>
                <a
                  href={`${BACKEND_URL}${f.file}`}
                  download
                  target="_blank"
                  rel="noreferrer"
                >
                  📎 Download
                </a>
              </li>
            ))}
          </ul>
        </div>
      ))}
    </div>
  );
}
