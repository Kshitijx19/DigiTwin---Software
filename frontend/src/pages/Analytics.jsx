import { useEffect, useState } from "react";
import client from "../api/client";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  ArcElement,
  Tooltip,
  Legend,
} from "chart.js";
import { Line, Doughnut } from "react-chartjs-2";

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  ArcElement,
  Tooltip,
  Legend
);

function MetricCard({ title, value, subtitle }) {
  return (
    <div
      style={{
        background: "white",
        borderRadius: "16px",
        padding: "18px",
        boxShadow: "0 4px 16px rgba(0,0,0,0.08)",
        border: "1px solid #e5e7eb",
      }}
    >
      <p style={{ margin: 0, color: "#6b7280" }}>{title}</p>
      <h2 style={{ margin: "10px 0" }}>{value}</h2>
      <p style={{ margin: 0, color: "#6b7280" }}>{subtitle}</p>
    </div>
  );
}

export default function Analytics() {
  const [spaces, setSpaces] = useState([]);
  const [selectedSpaceId, setSelectedSpaceId] = useState("");
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(false);

  const loadSpaces = async () => {
    const response = await client.get("/spaces/");
    setSpaces(response.data);
    if (response.data.length > 0 && !selectedSpaceId) {
      setSelectedSpaceId(String(response.data[0].id));
    }
  };

  const loadSummary = async (spaceId) => {
    if (!spaceId) return;
    setLoading(true);
    try {
      const response = await client.get(`/utilization/summary/${spaceId}?days=30`);
      setSummary(response.data);
    } catch (error) {
      console.error("Error loading summary:", error);
      setSummary(null);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadSpaces();
  }, []);

  useEffect(() => {
    if (selectedSpaceId) {
      loadSummary(selectedSpaceId);
    }
  }, [selectedSpaceId]);

  const handleSeedData = async () => {
    if (!selectedSpaceId) return;
    setLoading(true);
    try {
      await client.post(`/utilization/seed/${selectedSpaceId}?days=30`);
      await loadSummary(selectedSpaceId);
      alert("Demo utilization data generated");
    } catch (error) {
      console.error("Error seeding data:", error);
      alert("Could not generate demo data.");
    } finally {
      setLoading(false);
    }
  };

  const dailyChartData = summary
    ? {
        labels: summary.charts.daily.labels,
        datasets: [
          {
            label: "Average Utilization %",
            data: summary.charts.daily.values,
            borderColor: "#2563eb",
            backgroundColor: "rgba(37, 99, 235, 0.15)",
            pointBackgroundColor: "#2563eb",
            pointBorderColor: "#2563eb",
            pointRadius: 4,
            borderWidth: 3,
            tension: 0.35,
            fill: false,
          },
        ],
      }
    : null;

  const statusChartData = summary
    ? {
        labels: ["Idle", "Normal", "Overutilized"],
        datasets: [
          {
            label: "Records",
            data: [
              summary.charts.status_counts.idle,
              summary.charts.status_counts.normal,
              summary.charts.status_counts.overutilized,
            ],
            backgroundColor: ["#3b82f6", "#22c55e", "#ef4444"],
            borderColor: "#ffffff",
            borderWidth: 2,
            hoverOffset: 6,
          },
        ],
      }
    : null;

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        labels: {
          color: "#111827",
        },
      },
    },
  };

  return (
    <div>
      <h2 style={{ marginTop: 0 }}>Analytics</h2>
      <p>Utilization dashboard for the digital twin.</p>

      <div style={{ display: "flex", gap: "12px", flexWrap: "wrap", marginBottom: "20px" }}>
        <select
          value={selectedSpaceId}
          onChange={(e) => setSelectedSpaceId(e.target.value)}
          style={{ padding: "10px", minWidth: "260px" }}
        >
          {spaces.length === 0 ? (
            <option value="">No spaces found</option>
          ) : (
            spaces.map((space) => (
              <option key={space.id} value={space.id}>
                {space.name} - {space.building}
              </option>
            ))
          )}
        </select>

        <button onClick={handleSeedData} disabled={!selectedSpaceId || loading}>
          {loading ? "Working..." : "Generate Demo Data"}
        </button>
      </div>

      {summary && (
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
              title="Average Utilization"
              value={`${summary.summary.average_utilization}%`}
              subtitle="Last 30 days"
            />
            <MetricCard
              title="Idle Records"
              value={summary.summary.idle_records}
              subtitle={`Idle hours: ${summary.summary.idle_hours}`}
            />
            <MetricCard
              title="Overutilized Records"
              value={summary.summary.overutilized_records}
              subtitle="Potential capacity issue"
            />
            <MetricCard
              title="Peak Time Slot"
              value={summary.summary.peak_time_slot || "-"}
              subtitle={`${summary.summary.peak_time_slot_utilization}% average`}
            />
          </div>

          <div
            style={{
              display: "grid",
              gridTemplateColumns: "repeat(auto-fit, minmax(320px, 1fr))",
              gap: "24px",
              marginBottom: "24px",
            }}
          >
            <div
              style={{
                background: "white",
                borderRadius: "16px",
                padding: "18px",
                boxShadow: "0 4px 16px rgba(0,0,0,0.08)",
                border: "1px solid #e5e7eb",
                height: "420px",
              }}
            >
              <h3>Daily Utilization Trend</h3>
              {dailyChartData && <Line data={dailyChartData} options={chartOptions} />}
            </div>

            <div
              style={{
                background: "white",
                borderRadius: "16px",
                padding: "18px",
                boxShadow: "0 4px 16px rgba(0,0,0,0.08)",
                border: "1px solid #e5e7eb",
                height: "420px",
              }}
            >
              <h3>Status Distribution</h3>
              {statusChartData && <Doughnut data={statusChartData} options={chartOptions} />}
            </div>
          </div>

          <div
            style={{
              background: "white",
              borderRadius: "16px",
              padding: "18px",
              boxShadow: "0 4px 16px rgba(0,0,0,0.08)",
              border: "1px solid #e5e7eb",
            }}
          >
            <h3>Recent Records</h3>
            <table width="100%" cellPadding="8" style={{ borderCollapse: "collapse" }}>
              <thead>
                <tr style={{ textAlign: "left", borderBottom: "1px solid #ddd" }}>
                  <th>Date</th>
                  <th>Time Slot</th>
                  <th>Scheduled</th>
                  <th>Actual</th>
                  <th>Utilization %</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                {summary.recent_records.map((record, index) => (
                  <tr key={index} style={{ borderBottom: "1px solid #f0f0f0" }}>
                    <td>{record.date}</td>
                    <td>{record.time_slot}</td>
                    <td>{record.scheduled_users}</td>
                    <td>{record.actual_users}</td>
                    <td>{record.utilization_percent}</td>
                    <td>
  <span
    style={{
      padding: "5px 10px",
      borderRadius: "20px",
      background:
        record.status === "Overutilized"
          ? "#fee2e2"
          : record.status === "Idle"
          ? "#dbeafe"
          : "#dcfce7",
      color:
        record.status === "Overutilized"
          ? "#b91c1c"
          : record.status === "Idle"
          ? "#1d4ed8"
          : "#166534",
      fontWeight: "bold"
    }}
  >
    {record.status}
  </span>
</td>
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