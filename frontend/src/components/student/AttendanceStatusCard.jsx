export default function AttendanceStatusCard({ session, marked }) {
  if (!session) {
    return (
      <div className="card warning">
        <h3>No Active Attendance</h3>
        <p>Please wait for your teacher to start attendance.</p>
      </div>
    );
  }

  if (marked) {
    return (
      <div className="card success">
        <h3>Attendance Marked</h3>
        <p>
          <b>Subject:</b> {session.subject}
        </p>
        <p>✅ Your attendance has been recorded.</p>
      </div>
    );
  }

  return (
    <div className="card info">
      <h3>Attendance Active</h3>
      <p>
        <b>Subject:</b> {session.subject}
      </p>
      <p>
        <b>Teacher:</b> {session.teacher}
      </p>
      <p>Please mark your attendance below.</p>
    </div>
  );
}
