import { useEffect, useState } from "react";
import api from "../../api/axios";

export default function StudentNotices() {
  const [notices, setNotices] = useState([]);

  useEffect(() => {
    api.get("notices/student/")
      .then(res => setNotices(res.data));
  }, []);

  return (
    <div className="card full-width">
      <h3>📌 Notices</h3>

      {notices.map(n => (
        <div key={n.id} style={{marginBottom: "12px"}}>
          <b>{n.title}</b>
          <p>{n.description}</p>
          <ul>
            {n.files.map(f => (
              <li key={f.id}>
                <a href={f.file} download>📥 Download</a>
              </li>
            ))}
          </ul>
        </div>
      ))}
    </div>
  );
}
