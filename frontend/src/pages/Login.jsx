import { useState } from "react";
import client from "../api/client";
import { Link } from "react-router-dom";

export default function Login() {
  const [form, setForm] = useState({ username: "", password: "" });

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const login = async (e) => {
    e.preventDefault();
    try {
      const res = await client.post("/auth/login", form);
      localStorage.setItem("user", JSON.stringify(res.data.user));
      window.location.href = "/";
    } catch {
      alert("Login failed");
    }
  };

  return (
    <div style={{ minHeight: "100vh", display: "grid", placeItems: "center", padding: 24 }}>
      <div className="card card-pad" style={{ width: "100%", maxWidth: 420 }}>
        <div className="page-title" style={{ marginBottom: 18 }}>
          <h2>Login</h2>
          <p>Access your DigiTwin workspace</p>
        </div>

        <form onSubmit={login} className="form-shell">
          <input
            name="username"
            placeholder="Username"
            value={form.username}
            onChange={handleChange}
          />
          <input
            name="password"
            type="password"
            placeholder="Password"
            value={form.password}
            onChange={handleChange}
          />
          <button type="submit">Login</button>
        </form>

        <p style={{ marginTop: 16, textAlign: "center" }}>
          New user? <Link to="/register">Register</Link>
        </p>
      </div>
    </div>
  );
}