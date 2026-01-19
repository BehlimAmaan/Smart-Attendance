import { useState } from "react";
import api from "../api/axios";
import { useNavigate } from "react-router-dom";


export default function ChangePassword() {
  const [password, setPassword] = useState("");
  const [confirm, setConfirm] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleChange = async () => {
    if (!password || !confirm) {
      alert("All fields are required");
      return;
    }

    if (password !== confirm) {
      alert("Passwords do not match");
      return;
    }

    try {
      setLoading(true);
      await api.post("accounts/change-password/", {
        new_password: password,
      });

      alert("✅ Password updated successfully");

      const role = localStorage.getItem("role");
      navigate(role === "STUDENT" ? "/student" : "/teacher");
    } catch (err) {
      alert(err.response?.data?.detail || "Failed to update password");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-wrapper">
      <div className="auth-box">
        <h2>Change Password</h2>
        <p>Please set a new password to continue</p>

        <input
          type="password"
          placeholder="New password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />

        <input
          type="password"
          placeholder="Confirm password"
          value={confirm}
          onChange={(e) => setConfirm(e.target.value)}
        />

        <button onClick={handleChange} disabled={loading}>
          {loading ? "Updating..." : "Update Password"}
        </button>
      </div>
    </div>
  );
}
