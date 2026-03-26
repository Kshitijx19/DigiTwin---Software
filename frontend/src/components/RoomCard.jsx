export default function RoomCard({ space }) {
    return (
      <div
        style={{
          background: "white",
          borderRadius: "12px",
          padding: "16px",
          boxShadow: "0 2px 8px rgba(0,0,0,0.08)",
          border: "1px solid #e5e7eb",
        }}
      >
        <h3 style={{ marginTop: 0 }}>{space.name}</h3>
        <p><strong>Building:</strong> {space.building}</p>
        <p><strong>Capacity:</strong> {space.capacity}</p>
        <p><strong>Type:</strong> {space.space_type}</p>
      </div>
    );
  }