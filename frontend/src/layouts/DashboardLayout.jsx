import { Outlet } from "react-router-dom";
import { Navbar } from "../components/layout/Navbar";
import { Sidebar } from "../components/layout/Sidebar";

export function DashboardLayout() {
  return (
    <div className="dashboard-shell">
      <a className="skip-link" href="#main-content">
        Skip to content
      </a>
      <Sidebar />
      <div className="dashboard-main">
        <Navbar />
        <main id="main-content" className="content">
          <Outlet />
        </main>
        <footer className="footer">EduTrack Pro · Academic management dashboard</footer>
      </div>
    </div>
  );
}
