import React from "react";
import { NavLink, Route, Routes } from "react-router-dom";
import Dashboard from "./pages/Dashboard";
import Tasks from "./pages/Tasks";
import Habits from "./pages/Habits";
import Calendar from "./pages/Calendar";
import Notes from "./pages/Notes";
import Analytics from "./pages/Analytics";
import Settings from "./pages/Settings";

function TopNav() {
  const linkClass = ({ isActive }: { isActive: boolean }) =>
    isActive ? "active" : "";
  return (
    <div className="glass nav">
      <NavLink to="/" end className={linkClass}>Dashboard</NavLink>
      <NavLink to="/tasks" className={linkClass}>Tasks</NavLink>
      <NavLink to="/habits" className={linkClass}>Habits</NavLink>
      <NavLink to="/calendar" className={linkClass}>Calendar</NavLink>
      <NavLink to="/notes" className={linkClass}>Notes</NavLink>
      <NavLink to="/analytics" className={linkClass}>Analytics</NavLink>
      <NavLink to="/settings" className={linkClass}>Settings</NavLink>
    </div>
  );
}

export default function App() {
  return (
    <div className="container">
      <div className="glass header" style={{ marginBottom: 14 }}>
        <div>
          <h1>LocalLife</h1>
          <p>本地优先 · 隐私友好 · 精致生活控制台</p>
        </div>
        <span className="badge">Stage A · 骨架可运行</span>
      </div>

      <TopNav />

      <div style={{ height: 14 }} />

      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/tasks" element={<Tasks />} />
        <Route path="/habits" element={<Habits />} />
        <Route path="/calendar" element={<Calendar />} />
        <Route path="/notes" element={<Notes />} />
        <Route path="/analytics" element={<Analytics />} />
        <Route path="/settings" element={<Settings />} />
      </Routes>
    </div>
  );
}
