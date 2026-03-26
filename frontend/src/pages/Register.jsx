import { useState } from "react";
import client from "../api/client";
import { Link } from "react-router-dom";

export default function Register() {
  const [form, setForm] = useState({
    username: "",
    password: "",
  });

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const register = async (e) => {
    e.preventDefault();
    try {
      await client.post("/auth/register", {
        username: form.username,
        password: form.password,
        role: "user",
      });

      alert("Registration successful. Please log in.");
      window.location.href = "/login";
    } catch (err) {
      alert(err?.response?.data?.detail || "Registration failed");
    }
  };

  return (
    <div style={{ minHeight: "100vh", display: "grid", placeItems: "center", padding: 24 }}>
      <div className="card card-pad" style={{ width: "100%", maxWidth: 420 }}>
        <div className="page-title" style={{ marginBottom: 18 }}>
          <h2>Register</h2>
          <p>Create a normal user account</p>
        </div>

        <form onSubmit={register} className="form-shell">
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
          <button type="submit">Register</button>
        </form>

        <p style={{ marginTop: 16, textAlign: "center" }}>
          Already have an account? <Link to="/login">Login</Link>
        </p>
      </div>
    </div>
  );
}