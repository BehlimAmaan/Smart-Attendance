import { useEffect, useRef, useState } from "react";
import api from "../../api/axios";
import QrScanner from "qr-scanner";

export default function ScanQR({ sessionId, onSuccess }) {
  const videoRef = useRef(null);
  const scannerRef = useRef(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    scannerRef.current = new QrScanner(
      videoRef.current,
      async (result) => {
        try {
          await api.post("attendance/mark/", {
            session_id: sessionId,
            method: "QR",
            qr_token: result.data,
          });

          alert("✅ Attendance marked via QR");
          onSuccess && onSuccess();
          scannerRef.current.stop();
        } catch (err) {
          setError(err.response?.data?.detail || "Invalid QR code");
        }
      },
      {
        returnDetailedScanResult: true,
      }
    );

    scannerRef.current.start();

    return () => {
      scannerRef.current?.stop();
    };
  }, [sessionId, onSuccess]);

  return (
    <div className="card">
      <h3>Scan QR Code</h3>

      <video
        ref={videoRef}
        style={{ width: "100%", borderRadius: "10px" }}
      />

      {error && (
        <p style={{ color: "#ef4444", fontWeight: "bold" }}>
          {error}
        </p>
      )}

      <p className="hint">
        Point your camera at the QR shown by the teacher
      </p>
    </div>
  );
}
