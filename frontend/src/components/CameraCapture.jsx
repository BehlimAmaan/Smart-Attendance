import { useEffect, useRef, useState } from "react";
import api from "../api/axios";
import { FaceLandmarker, FilesetResolver } from "@mediapipe/tasks-vision";

export default function CameraCapture({ sessionId, onSuccess, onFaceMismatch }) {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);

  const blinkCounterRef = useRef(0);
  const noseXRef = useRef(null);

  const [blinkOk, setBlinkOk] = useState(false);
  const [headOk, setHeadOk] = useState(false);
  const [loading, setLoading] = useState(false);
  const [cameraReady, setCameraReady] = useState(false);

  const getLocation = () =>
    new Promise((resolve, reject) => {
      navigator.geolocation.getCurrentPosition(
        (pos) => resolve(pos.coords),
        reject,
        { enableHighAccuracy: true }
      );
    });

  function eyeAspectRatio(eye) {
    const A = Math.hypot(eye[1].x - eye[5].x, eye[1].y - eye[5].y);
    const B = Math.hypot(eye[2].x - eye[4].x, eye[2].y - eye[4].y);
    const C = Math.hypot(eye[0].x - eye[3].x, eye[0].y - eye[3].y);
    return (A + B) / (2.0 * C);
  }

  function detectBlink(landmarks) {
    const LEFT_EYE = [33, 160, 158, 133, 153, 144];
    const RIGHT_EYE = [362, 385, 387, 263, 373, 380];

    const leftEye = LEFT_EYE.map(i => landmarks[i]);
    const rightEye = RIGHT_EYE.map(i => landmarks[i]);

    const avgEAR =
      (eyeAspectRatio(leftEye) + eyeAspectRatio(rightEye)) / 2;

    if (avgEAR < 0.2) blinkCounterRef.current += 1;
    if (blinkCounterRef.current >= 2 && !blinkOk) setBlinkOk(true);
  }

  function detectHeadMovement(landmarks) {
    const nose = landmarks[1];

    if (!noseXRef.current) {
      noseXRef.current = nose.x;
      return;
    }

    if (Math.abs(nose.x - noseXRef.current) > 0.03 && !headOk) {
      setHeadOk(true);
    }
  }

  useEffect(() => {
    let stream;

    async function startCamera() {
      stream = await navigator.mediaDevices.getUserMedia({
        video: { width: 640, height: 480 }
      });

      const video = videoRef.current;
      video.srcObject = stream;
      video.onloadedmetadata = () => {
        video.play();
        setCameraReady(true);
      };
    }

    startCamera();
    return () => stream?.getTracks().forEach(t => t.stop());
  }, []);

  useEffect(() => {
    if (!cameraReady) return;

    let landmarker;
    let rafId;

    async function startLandmarker() {
      const fileset = await FilesetResolver.forVisionTasks(
        "https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@0.10.3/wasm"
      );

      landmarker = await FaceLandmarker.createFromOptions(fileset, {
        baseOptions: {
          modelAssetPath:
            "https://storage.googleapis.com/mediapipe-assets/face_landmarker.task",
        },
        runningMode: "VIDEO",
        numFaces: 1,
      });

      const detect = () => {
        const video = videoRef.current;
        if (!video || video.readyState < 2) {
          rafId = requestAnimationFrame(detect);
          return;
        }

        const results = landmarker.detectForVideo(video, performance.now());

        if (results.faceLandmarks?.length) {
          const landmarks = results.faceLandmarks[0];
          detectBlink(landmarks);
          detectHeadMovement(landmarks);
        }

        rafId = requestAnimationFrame(detect);
      };

      detect();
    }

    startLandmarker();
    return () => {
      cancelAnimationFrame(rafId);
      landmarker?.close();
    };
  }, [cameraReady]);

  const captureAndSend = async () => {
    if (!blinkOk || !headOk) return;

    setLoading(true);

    const coords = await getLocation();

    const canvas = canvasRef.current;
    const video = videoRef.current;

    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    canvas.getContext("2d").drawImage(video, 0, 0);

    canvas.toBlob(async (blob) => {
      const formData = new FormData();
      formData.append("session_id", sessionId);
      formData.append("method", "FACE");
      formData.append("face_image", blob);
      formData.append("blink_ok", true);
      formData.append("head_ok", true);
      formData.append("latitude", coords.latitude);
      formData.append("longitude", coords.longitude);

      try {
        await api.post("attendance/mark/", formData);
        alert("✅ Attendance marked");
        onSuccess && onSuccess();
      } catch (err) {
        const errorCode = err.response?.data?.error_code;

        if (errorCode === "FACE_MISMATCH") {
          alert("❌ Face mismatch. Please re-register.");
          onFaceMismatch();
        } else {
          alert(err.response?.data?.detail || "❌ Attendance failed");
        }
      } finally {
        setLoading(false);
      }
    }, "image/jpeg");
  };

  return (
    <div className="camera-container">
      <div className="camera-card">
        <h3>Face Attendance</h3>
        <p>Blink twice and move your head</p>

        <video ref={videoRef} autoPlay muted />

        <button
          onClick={captureAndSend}
          disabled={!blinkOk || !headOk || loading}
        >
          {loading ? "Processing..." : "Mark Attendance"}
        </button>
      </div>

      <canvas ref={canvasRef} hidden />
    </div>
  );
}
