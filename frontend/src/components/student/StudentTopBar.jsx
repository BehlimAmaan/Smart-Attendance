export default function StudentTopBar() {
  const email = localStorage.getItem("username");

  return (
    <header className="top-bar">
      <div>
        <b>Student Dashboard</b>
      </div>

      <div className="top-right">
        <span>{email}</span>

        <button onClick={() => window.location.href = "/change-password"}>
          Change Password
        </button>

        <button
          onClick={() => {
            localStorage.clear();
            window.location.href = "/";
          }}
        >
          Logout
        </button>
      </div>
    </header>
  );
}
