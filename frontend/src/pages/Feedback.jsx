import { useEffect, useState } from "react";
import client from "../api/client";

export default function Feedback() {
  const [spaces, setSpaces] = useState([]);
  const [form, setForm] = useState({
    space_id: "",
    user_name: "",
    issue_type: "General",
    message: "",
    latitude: "",
    longitude: "",
  });

  const loadSpaces = async () => {
    const response = await client.get("/spaces/");
    setSpaces(response.data);
    if (response.data.length > 0 && !form.space_id) {
      setForm((prev) => ({ ...prev, space_id: String(response.data[0].id) }));
    }
  };

  useEffect(() => {
    loadSpaces();
  }, []);

  useEffect(() => {
    const selected = spaces.find((s) => String(s.id) === String(form.space_id));
    if (selected) {
      setForm((prev) => ({
        ...prev,
        latitude: selected.latitude ?? "",
        longitude: selected.longitude ?? "",
      }));
    }
  }, [form.space_id, spaces]);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const useBrowserLocation = () => {
    if (!navigator.geolocation) {
      alert("Geolocation is not supported by this browser.");
      return;
    }

    navigator.geolocation.getCurrentPosition(
      (position) => {
        setForm((prev) => ({
          ...prev,
          latitude: position.coords.latitude,
          longitude: position.coords.longitude,
        }));
      },
      () => {
        alert("Could not get browser location.");
      }
    );
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const payload = {
        ...form,
        space_id: Number(form.space_id),
        latitude: Number(form.latitude),
        longitude: Number(form.longitude),
      };

      await client.post("/feedback/", payload);
      alert("Feedback submitted successfully.");
      setForm({
        space_id: form.space_id,
        user_name: "",
        issue_type: "General",
        message: "",
        latitude: form.latitude,
        longitude: form.longitude,
      });
    } catch (error) {
      console.error(error);
      alert("Feedback submission failed. Make sure you are within the geofence.");
    }
  };

  return (
    <div>
      <h2>Feedback</h2>
      <p>Submit an issue report for a specific space.</p>

      <form
        onSubmit={handleSubmit}
        style={{
          background: "white",
          padding: "16px",
          borderRadius: "12px",
          boxShadow: "0 2px 8px rgba(0,0,0,0.08)",
          maxWidth: "600px",
          display: "grid",
          gap: "12px",
        }}
      >
        <select name="space_id" value={form.space_id} onChange={handleChange}>
          {spaces.map((space) => (
            <option key={space.id} value={space.id}>
              {space.name} - {space.building}
            </option>
          ))}
        </select>

        <input
          name="user_name"
          placeholder="Your name"
          value={form.user_name}
          onChange={handleChange}
        />

        <select name="issue_type" value={form.issue_type} onChange={handleChange}>
          <option value="General">General</option>
          <option value="Furniture">Furniture</option>
          <option value="Projector">Projector</option>
          <option value="AC">AC / Ventilation</option>
          <option value="Electrical">Electrical</option>
          <option value="Cleanliness">Cleanliness</option>
        </select>

        <textarea
          name="message"
          placeholder="Describe the issue"
          rows="4"
          value={form.message}
          onChange={handleChange}
        />

        <div style={{ display: "flex", gap: "12px", flexWrap: "wrap" }}>
          <input
            name="latitude"
            placeholder="Latitude"
            value={form.latitude}
            onChange={handleChange}
          />
          <input
            name="longitude"
            placeholder="Longitude"
            value={form.longitude}
            onChange={handleChange}
          />
        </div>

        <div style={{ display: "flex", gap: "12px", flexWrap: "wrap" }}>
          <button type="button" onClick={useBrowserLocation}>
            Use Browser Location
          </button>
          <button type="submit">Submit Feedback</button>
        </div>
      </form>
    </div>
  );
}