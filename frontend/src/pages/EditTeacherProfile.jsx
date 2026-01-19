import { useEffect, useState } from "react";
import api from "../api/axios";
import { useNavigate } from "react-router-dom";

export default function EditTeacherProfile() {
  const [form, setForm] = useState({
    name: "",
    email: "",
    department: "",
  });

  const navigate = useNavigate();

  useEffect(() => {
    api.get("teachers/profile/")
      .then(res => setForm(res.data))
      .catch(() => alert("Failed to load profile"));
  }, []);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const saveProfile = async () => {
    try {
      await api.put("teachers/profile/", {
        name: form.name,
        department: form.department,
      });
      alert("✅ Profile updated");
      navigate("/teacher");
    } catch {
      alert("Failed to update profile");
    }
  };

  return (
    <div className="page">
      <div className="card">
        <h2>Edit Profile</h2>

        <input
          name="name"
          placeholder="Full Name"
          value={form.name}
          onChange={handleChange}
        />

        <input
          name="email"
          value={form.email}
          disabled
        />

        <input
          name="department"
          placeholder="Department"
          value={form.department}
          onChange={handleChange}
        />

        <button onClick={saveProfile}>Save Changes</button>
      </div>
    </div>
  );
}
