import { useEffect, useRef, useState } from "react";
import api from "../api/axios";

export default function RegisterFace() {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    let stream;

    async function startCamera() {
      try {
        stream = await navigator.mediaDevices.getUserMedia({
          video: { width: 640, height: 480 },
        });

        const video = videoRef.current;
        video.srcObject = stream;
        video.onloadedmetadata = () => video.play();
      } catch {
        alert("Camera access denied");
      }
    }

    startCamera();

    return () => {
      if (stream) stream.getTracks().forEach((t) => t.stop());
    };
  }, []);

  const captureAndRegister = () => {
    const video = videoRef.current;
    const canvas = canvasRef.current;

    if (!video || video.videoWidth === 0) {
      alert("Camera not ready");
      return;
    }

    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    canvas.getContext("2d").drawImage(video, 0, 0);

    canvas.toBlob(async (blob) => {
      setLoading(true);

      const formData = new FormData();
      formData.append("face_image", blob);

      try {
        await api.post("accounts/register-face/", formData);
        alert("✅ Face registered successfully");
        window.location.href = "/student";
      } catch (err) {
        const code = err.response?.data?.error_code;

        if (code === "FACE_REREGISTER_MISMATCH") {
          alert(
            "❌ This face does not match your previously registered face.\n\n" +
            "For security reasons, only the same person can re-register."
          );
        } else {
          alert(err.response?.data?.detail || "❌ Registration failed");
        }
      } finally {
        setLoading(false);
      }
    }, "image/jpeg");
  };

  return (
    <div className="register-page">
      <header className="top-bar">
        <h1>Face Registration</h1>
      </header>

      <main className="content">
        <div className="card">
          <h3>Align Your Face Properly</h3>
          <p>Ensure good lighting and look straight at the camera.</p>

          <div className="video-box">
            <video ref={videoRef} autoPlay playsInline muted />
          </div>

          <canvas ref={canvasRef} style={{ display: "none" }} />

          <button onClick={captureAndRegister} disabled={loading}>
            {loading ? "Saving..." : "Register Face"}
          </button>
        </div>
      </main>
    </div>
  );
}
