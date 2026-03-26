import { useEffect, useState } from "react";
import client from "../api/client";

function MetricCard({ title, value, subtitle }) {
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
      <p style={{ margin: 0, color: "#6b7280" }}>{title}</p>
      <h2 style={{ margin: "8px 0" }}>{value}</h2>
      <p style={{ margin: 0, color: "#6b7280" }}>{subtitle}</p>
    </div>
  );
}

export default function Optimization() {
  const [data, setData] = useState(null);
  const [days, setDays] = useState(30);
  const [loading, setLoading] = useState(false);

  const loadRecommendations = async () => {
    setLoading(true);
    try {
      const response = await client.get(`/optimization/recommendations?days=${days}`);
      setData(response.data);
    } catch (error) {
      console.error("Error loading optimization recommendations:", error);
      alert("Could not load optimization suggestions.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadRecommendations();
  }, []);

  return (
    <div>
      <h2>Optimization</h2>
      <p>Schedule optimization suggestions based on utilization patterns.</p>

      <div style={{ display: "flex", gap: "12px", marginBottom: "20px", flexWrap: "wrap" }}>
        <input
          type="number"
          min="1"
          max="365"
          value={days}
          onChange={(e) => setDays(Number(e.target.value))}
          style={{ padding: "10px", width: "120px" }}
        />
        <button onClick={loadRecommendations} disabled={loading}>
          {loading ? "Loading..." : "Run Optimization"}
        </button>
      </div>

      {data && (
        <>
          <div
            style={{
              display: "grid",
              gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))",
              gap: "16px",
              marginBottom: "24px",
            }}
          >
            <MetricCard
              title="Current Balance Score"
              value={`${data.summary.current_balance_score}%`}
              subtitle="How well room usage is balanced now"
            />
            <MetricCard
              title="Proposed Balance Score"
              value={`${data.summary.proposed_balance_score}%`}
              subtitle="After applying recommendations"
            />
            <MetricCard
              title="Improvement"
              value={`${data.summary.improvement_percentage}%`}
              subtitle="Estimated improvement"
            />
            <MetricCard
              title="Overutilized Spaces"
              value={data.summary.overutilized_spaces}
              subtitle="Rooms needing attention"
            />
          </div>

          <div
            style={{
              background: "white",
              borderRadius: "12px",
              padding: "16px",
              boxShadow: "0 2px 8px rgba(0,0,0,0.08)",
              border: "1px solid #e5e7eb",
              marginBottom: "24px",
            }}
          >
            <h3>Recommendations</h3>
            {data.recommendations.length === 0 ? (
              <p>No optimization suggestions found. Generate more utilization data first.</p>
            ) : (
              <table width="100%" cellPadding="8" style={{ borderCollapse: "collapse" }}>
                <thead>
                  <tr style={{ textAlign: "left", borderBottom: "1px solid #ddd" }}>
                    <th>Type</th>
                    <th>From Space</th>
                    <th>To Space</th>
                    <th>Reason</th>
                    <th>Improvement</th>
                  </tr>
                </thead>
                <tbody>
                  {data.recommendations.map((item, index) => (
                    <tr key={index} style={{ borderBottom: "1px solid #f0f0f0" }}>
                      <td>{item.type}</td>
                      <td>
                        {item.from_space.name} <br />
                        <small>{item.from_space.building}</small>
                      </td>
                      <td>
                        {item.to_space ? (
                          <>
                            {item.to_space.name} <br />
                            <small>{item.to_space.building}</small>
                          </>
                        ) : (
                          "-"
                        )}
                      </td>
                      <td>{item.reason}</td>
                      <td>{item.estimated_improvement}%</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </div>

          <div
            style={{
              background: "white",
              borderRadius: "12px",
              padding: "16px",
              boxShadow: "0 2px 8px rgba(0,0,0,0.08)",
              border: "1px solid #e5e7eb",
            }}
          >
            <h3>Space Status Overview</h3>
            <table width="100%" cellPadding="8" style={{ borderCollapse: "collapse" }}>
              <thead>
                <tr style={{ textAlign: "left", borderBottom: "1px solid #ddd" }}>
                  <th>Space</th>
                  <th>Building</th>
                  <th>Average Utilization</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                {data.spaces.map((space) => (
                  <tr key={space.id} style={{ borderBottom: "1px solid #f0f0f0" }}>
                    <td>{space.name}</td>
                    <td>{space.building}</td>
                    <td>{space.average_utilization}%</td>
                    <td>{space.status}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </>
      )}
    </div>
  );
}