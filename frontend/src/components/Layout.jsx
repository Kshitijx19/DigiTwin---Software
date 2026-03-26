export default function Layout({ children }) {
  const user = JSON.parse(localStorage.getItem("user"));

  return (
    <div>
      <div
        style={{
          background: "linear-gradient(90deg, #1e3a8a, #2563eb)",
          color: "white",
          padding: "15px 25px",
          display: "flex",
          justifyContent: "space-evenly",
          alignItems: "center",
          boxShadow: "0 4px 10px rgba(0,0,0,0.1)"
        }}
      >
        {/* LEFT SIDE */}
        <div style={{ display: "flex", gap: "50px", justifyContent: "space-evenly", alignItems: "center" }}>
          <h2 style={{ margin: 0 }}>DigiTwin</h2>

          <a href="/" style={{ color: "white", textDecoration: "none" }}>Dashboard</a>
          <a href="/spaces" style={{ color: "white", textDecoration: "none" }}>Spaces</a>
          <a href="/analytics" style={{ color: "white", textDecoration: "none" }}>Analytics</a>
          <a href="/optimization" style={{ color: "white", textDecoration: "none" }}>Optimization</a>
          <a href="/feedback" style={{ color: "white", textDecoration: "none" }}>Feedback</a>
          {user?.role !== "user" && (
            <a href="/maintenance" style={{ color: "white", textDecoration: "none" }}>Maintenance</a>
          )}
        </div>

        {/* RIGHT SIDE */}
        <button
          onClick={() => {
            localStorage.removeItem("user");
            window.location.href = "/login";
          }}
          style={{
            background: "#ef4444",
            padding: "8px 14px",
            borderRadius: "8px"
          }}
        >
          Logout
        </button>
      </div>

      <div className="container">{children}</div>
    </div>
  );
}