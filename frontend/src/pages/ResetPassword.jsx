import { useState } from "react";
import api from "../api/axios";
import { Lock } from "lucide-react";
import { useParams, useNavigate } from "react-router-dom";

export default function ResetPassword() {
  const { uid, token } = useParams();
  const navigate = useNavigate();

  const [password, setPassword] = useState("");
  const [confirm, setConfirm] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [message, setMessage] = useState("");

  const handleReset = async () => {
    if (!password || !confirm) {
      setError("All fields are required");
      return;
    }

    if (password !== confirm) {
      setError("Passwords do not match");
      return;
    }

    try {
      setLoading(true);
      setError("");

      await api.post("accounts/reset-password/", {
        uid,
        token,
        new_password: password,
      });

      setMessage("Password reset successful. Redirecting to login...");
      setTimeout(() => navigate("/"), 3000);
    } catch {
      setError("Invalid or expired reset link");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-layout">
      <div className="login-form">
        <div className="form-container">
          <h2>Reset Password</h2>
          <p className="subtitle">Enter your new password</p>

          {error && <div className="error-card">{error}</div>}
          {message && <div className="success-card">{message}</div>}

          <div className="input-group">
            <Lock className="input-icon" />
            <input
              type="password"
              placeholder="New password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              disabled={loading}
              className="modern-input"
            />
          </div>

          <div className="input-group">
            <Lock className="input-icon" />
            <input
              type="password"
              placeholder="Confirm password"
              value={confirm}
              onChange={(e) => setConfirm(e.target.value)}
              disabled={loading}
              className="modern-input"
            />
          </div>

          <button
            onClick={handleReset}
            disabled={loading}
            className="login-button"
          >
            {loading ? "Resetting..." : "Reset Password"}
          </button>
        </div>
      </div>
    </div>
  );
}
