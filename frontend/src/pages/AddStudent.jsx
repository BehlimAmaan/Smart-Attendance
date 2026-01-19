import { useState } from "react";
import api from "../api/axios";
import { useNavigate } from "react-router-dom";

export default function AddStudent() {
  const [form, setForm] = useState({
    roll_no: "",
    full_name: "",
    email: "",
    phone: "",
    batch: "",
    department: "",
  });

  const navigate = useNavigate();

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async () => {
    for (let key in form) {
      if (!form[key]) {
        alert("All fields are required");
        return;
      }
    }

    try {
      await api.post("teachers/add-student/", form);
      alert("✅ Student added successfully");
      navigate("/teacher");
    } catch (err) {
      alert(err.response?.data?.detail || "Failed to add student");
    }
  };

  return (
    <div className="page">
      <div className="card">
        <h2>Add Student</h2>

        {Object.keys(form).map((key) => (
          <input
            key={key}
            name={key}
            placeholder={key.replace("_", " ").toUpperCase()}
            value={form[key]}
            onChange={handleChange}
          />
        ))}

        <button onClick={handleSubmit}>Add Student</button>
      </div>
    </div>
  );
}
