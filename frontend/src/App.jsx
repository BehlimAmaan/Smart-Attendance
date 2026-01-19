import { BrowserRouter, Routes, Route } from "react-router-dom";
import Login from "./pages/Login";
import StudentDashboard from "./pages/StudentDashboard";
import TeacherDashboard from "./pages/TeacherDashboard";
import RegisterFace from "./components/RegisterFace";
import ChangePassword from "./pages/ChangePassword";
import AddStudent from "./pages/AddStudent";
import EditTeacherProfile from "./pages/EditTeacherProfile";
import ForgotPassword from "./pages/ForgotPassword";
import ResetPassword from "./pages/ResetPassword";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/student" element={<StudentDashboard />} />
        <Route path="/teacher" element={<TeacherDashboard />} />
        <Route path="/register-face" element={<RegisterFace />} />
        <Route path="/change-password" element={<ChangePassword />} />
        <Route path="/add-student" element={<AddStudent />} />
        <Route path="/teacher/profile" element={<EditTeacherProfile />} />
        <Route path="/forgot-password" element={<ForgotPassword />} />
        <Route path="/reset-password/:uid/:token" element={<ResetPassword />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
