import { useState } from "react";
import api from "../api/axios";
import { useNavigate } from "react-router-dom";
import { Eye, EyeOff, Mail, Lock, Sparkles } from "lucide-react";



export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleLogin = async () => {
    if (!email || !password) {
      setError("Please enter email and password");
      return;
    }

    try {
      setLoading(true);
      setError("");

      const res = await api.post("accounts/login/", {
        email,
        password,
      });

      localStorage.setItem("access", res.data.access);
      localStorage.setItem("refresh", res.data.refresh);
      localStorage.setItem("role", res.data.role);

      if (res.data.first_login) {
        navigate("/change-password");
        return;
      }

      navigate(res.data.role === "STUDENT" ? "/student" : "/teacher");
    } catch {
      setError("Invalid email or password");
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !loading) {
      handleLogin();
    }
  };

  return (
    <div className="login-layout">
      {/* LEFT BRAND PANEL */}
      <div className="login-brand">
        <div className="brand-content">
          <div className="logo-container">
            <Sparkles className="logo-icon" />
            <h1>Smart Attendance</h1>
          </div>
          <p className="brand-tagline">
            AI-powered attendance system<br />
            using Face Recognition & Liveness Detection
          </p>
          
          <div className="features-list">
            <div className="feature-item">
              <div className="feature-dot"></div>
              <span>Real-time facial recognition</span>
            </div>
            <div className="feature-item">
              <div className="feature-dot"></div>
              <span>Advanced liveness detection</span>
            </div>
            <div className="feature-item">
              <div className="feature-dot"></div>
              <span>Secure & contactless</span>
            </div>
          </div>
        </div>
        
        <div className="brand-footer">
          <div className="tech-badge">AI-Powered</div>
          <div className="tech-badge">Secure</div>
          <div className="tech-badge">Fast</div>
        </div>
      </div>

      {/* RIGHT FORM PANEL */}
      <div className="login-form">
        <div className="form-container">
          <div className="form-header">
            <h2>Welcome Back</h2>
            <p className="subtitle">Sign in to your account</p>
          </div>

          <div className="form-card">
            {error && (
              <div className="error-card">
                <div className="error-icon">!</div>
                <div className="error-text">{error}</div>
              </div>
            )}

            <div className="input-group">
              <Mail className="input-icon" />
              <input
                type="email"
                placeholder="Email address"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                disabled={loading}
                onKeyPress={handleKeyPress}
                className="modern-input"
              />
            </div>

            <div className="input-group">
              <Lock className="input-icon" />
              <input
                type={showPassword ? "text" : "password"}
                placeholder="Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                disabled={loading}
                onKeyPress={handleKeyPress}
                className="modern-input"
              />
              <button 
                type="button" 
                className="password-toggle"
                onClick={() => setShowPassword(!showPassword)}
                disabled={loading}
              >
                {showPassword ? <EyeOff size={20} /> : <Eye size={20} />}
              </button>
            </div>

            <button 
              onClick={handleLogin} 
              disabled={loading}
              className="login-button"
            >
              {loading ? (
                <>
                  <div className="spinner"></div>
                  Logging in...
                </>
              ) : (
                'Login'
              )}
            </button>

            <div className="form-footer">
              <a href="/forgot-password" className="forgot-link">
                Forgot password?
              </a>
              <div className="signup-prompt">
                New to Smart Attendance?{" "}
                <span className="admin-only-text">
                  Create Teacher Account (Admin only)
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}