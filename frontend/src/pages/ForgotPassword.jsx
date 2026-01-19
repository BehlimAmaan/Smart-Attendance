import { useState } from "react";
import api from "../api/axios";
import { Mail } from "lucide-react";
import { useNavigate } from "react-router-dom";

export default function ForgotPassword() {
  const [email, setEmail] = useState("");
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleSubmit = async () => {
    if (!email) {
      setError("Please enter your email");
      return;
    }

    try {
      setLoading(true);
      setError("");
      setMessage("");

      const res = await api.post("accounts/forgot-password/", { email });

      setMessage(res.data.detail);
      setTimeout(() => navigate("/"), 3000);
    } catch {
      setError("Something went wrong. Try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-layout">
      <div className="login-form">
        <div className="form-container forgot-password">
          <h2>Forgot Password</h2>
          <p className="subtitle">
            Enter your registered email to receive reset link
          </p>

          {error && <div className="error-card">{error}</div>}
          {message && <div className="success-card">{message}</div>}

          <div className="input-group">
            <Mail className="input-icon" />
            <input
              type="email"
              placeholder="Email address"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              disabled={loading}
              className="modern-input"
            />
          </div>

          <button
            onClick={handleSubmit}
            disabled={loading}
            className="login-button"
          >
            {loading ? "Sending..." : "Send Reset Link"}
          </button>
        </div>
      </div>
    </div>
  );
}
