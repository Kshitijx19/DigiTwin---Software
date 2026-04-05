import { BrowserRouter, Routes, Route } from "react-router-dom";

import Layout from "./components/Layout";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Dashboard from "./pages/Dashboard";
import Spaces from "./pages/Spaces";
import Analytics from "./pages/Analytics";
import Optimization from "./pages/Optimization";
import Feedback from "./pages/Feedback";
import Maintenance from "./pages/Maintenance";

export default function App() {
  const user = JSON.parse(localStorage.getItem("user"));

  return (
    <BrowserRouter>
      <Layout>
        <Routes>
          {/* AUTH */}
          <Route path="/login" element={!user ? <Login /> : <Dashboard />} />
          <Route path="/register" element={!user ? <Register /> : <Dashboard />} />

          {/* COMMON */}
          <Route path="/" element={user ? <Dashboard /> : <Login />} />
          <Route path="/analytics" element={user ? <Analytics /> : <Login />} />
          <Route path="/optimization" element={user ? <Optimization /> : <Login />} />
          <Route path="/feedback" element={user ? <Feedback /> : <Login />} />

          {/* ADMIN / MANAGER */}
          <Route path="/spaces" element={user ? <Spaces /> : <Login />} />

          {/*  ONLY ADMIN + MANAGER */}
          <Route
            path="/maintenance"
            element={
              user?.role === "admin" || user?.role === "manager"
                ? <Maintenance />
                : <Dashboard />
            }
          />
        </Routes>
      </Layout>
    </BrowserRouter>
  );
}
