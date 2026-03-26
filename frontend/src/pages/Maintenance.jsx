import { useEffect, useState } from "react";
import client from "../api/client";

export default function Maintenance() {
  const [alerts, setAlerts] = useState([]);
  const [loading, setLoading] = useState(false);

  const loadAlerts = async () => {
    const response = await client.get("/maintenance/");
    setAlerts(response.data);
  };

  useEffect(() => {
    loadAlerts();
  }, []);

  const runScan = async () => {
    setLoading(true);
    try {
      await client.post("/maintenance/scan?days=30");
      await loadAlerts();
      alert("Maintenance scan completed.");
    } catch (error) {
      console.error(error);
      alert("Could not run maintenance scan.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h2>Maintenance</h2>
      <p>Predictive maintenance alerts for overused spaces.</p>

      <button onClick={runScan} disabled={loading} style={{ marginBottom: "20px" }}>
        {loading ? "Scanning..." : "Run Maintenance Scan"}
      </button>

      <div
        style={{
          background: "white",
          borderRadius: "12px",
          padding: "16px",
          boxShadow: "0 2px 8px rgba(0,0,0,0.08)",
          border: "1px solid #e5e7eb",
        }}
      >
        <h3>Open Alerts</h3>
        {alerts.length === 0 ? (
          <p>No maintenance alerts yet.</p>
        ) : (
          <table width="100%" cellPadding="8" style={{ borderCollapse: "collapse" }}>
            <thead>
              <tr style={{ textAlign: "left", borderBottom: "1px solid #ddd" }}>
                <th>Title</th>
                <th>Severity</th>
                <th>Status</th>
                <th>Source</th>
                <th>Description</th>
              </tr>
            </thead>
            <tbody>
              {alerts.map((alert) => (
                <tr key={alert.id} style={{ borderBottom: "1px solid #f0f0f0" }}>
                  <td>{alert.title}</td>
                  <td>{alert.severity}</td>
                  <td>{alert.status}</td>
                  <td>{alert.source}</td>
                  <td>{alert.description}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}