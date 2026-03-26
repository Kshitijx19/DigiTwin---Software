import { useEffect, useState } from "react";
import client from "../api/client";
import RoomCard from "../components/RoomCard";

export default function Spaces() {
  const [spaces, setSpaces] = useState([]);
  const [form, setForm] = useState({
    name: "",
    building: "",
    capacity: "",
    space_type: "",
  });

  const loadSpaces = async () => {
    try {
      const response = await client.get("/spaces/");
      setSpaces(response.data);
    } catch (error) {
      console.error("Error fetching spaces:", error);
    }
  };

  useEffect(() => {
    loadSpaces();
  }, []);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await client.post("/spaces/", {
        ...form,
        capacity: Number(form.capacity),
      });
      setForm({ name: "", building: "", capacity: "", space_type: "" });
      loadSpaces();
    } catch (error) {
      console.error("Error creating space:", error);
      alert("Could not create space. Check backend and inputs.");
    }
  };

  return (
    <div>
      <h2>Spaces</h2>

      <form
        onSubmit={handleSubmit}
        style={{
          background: "white",
          padding: "16px",
          borderRadius: "12px",
          boxShadow: "0 2px 8px rgba(0,0,0,0.08)",
          marginBottom: "24px",
          display: "grid",
          gap: "12px",
          maxWidth: "500px",
        }}
      >
        <input name="name" placeholder="Space Name" value={form.name} onChange={handleChange} />
        <input name="building" placeholder="Building" value={form.building} onChange={handleChange} />
        <input name="capacity" placeholder="Capacity" type="number" value={form.capacity} onChange={handleChange} />
        <input name="space_type" placeholder="Type (Classroom/Lab/etc.)" value={form.space_type} onChange={handleChange} />
        <button type="submit">Add Space</button>
      </form>

      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))",
          gap: "16px",
        }}
      >
        {spaces.map((space) => (
          <RoomCard key={space.id} space={space} />
        ))}
      </div>
    </div>
  );
}