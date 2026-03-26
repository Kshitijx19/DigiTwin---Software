import { useEffect, useState } from "react";
import client from "../api/client";
import RoomCard from "../components/RoomCard";

export default function Dashboard() {
  const [spaces, setSpaces] = useState([]);

  useEffect(() => {
    const fetchSpaces = async () => {
      try {
        const response = await client.get("/spaces/");
        setSpaces(response.data);
      } catch (error) {
        console.error("Error fetching spaces:", error);
      }
    };

    fetchSpaces();
  }, []);

  return (
    <div>
      <h2>Dashboard</h2>
      <p>Digital twin overview of academic spaces.</p>

      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))",
          gap: "16px",
          marginTop: "20px",
        }}
      >
        {spaces.length === 0 ? (
          <p>No spaces added yet. Go to Spaces and add one.</p>
        ) : (
          spaces.map((space) => <RoomCard key={space.id} space={space} />)
        )}
      </div>
    </div>
  );
}