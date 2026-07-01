import {
  BarChart3,
  BookOpen,
  ClipboardCheck,
  FileText,
  GraduationCap,
  LayoutDashboard,
  ListChecks,
  Settings,
  UserRound,
  UsersRound,
} from "lucide-react";
import { NavLink } from "react-router-dom";
import { useAuth } from "../../hooks/useAuth";
import { useSidebar } from "../../hooks/useSidebar";
import { ROLES } from "../../utils/constants";

const teacherNav = [
  { to: "/dashboard/teacher", label: "Dashboard", icon: LayoutDashboard },
  { to: "/students/list", label: "Students", icon: UsersRound },
  { to: "/subjects/list", label: "Subjects", icon: BookOpen },
  { to: "/attendance/list", label: "Attendance", icon: ClipboardCheck },
  { to: "/marks/list", label: "Marks", icon: BarChart3 },
  { to: "/assignments/list", label: "Assignments", icon: ListChecks },
  { to: "/reports/institution", label: "Reports", icon: FileText },
];

const studentNav = [
  { to: "/dashboard/student", label: "Dashboard", icon: LayoutDashboard },
  { to: "/profile", label: "Profile", icon: UserRound },
  { to: "/attendance/history", label: "Attendance", icon: ClipboardCheck },
  { to: "/marks/performance", label: "Marks", icon: BarChart3 },
  { to: "/assignments/list", label: "Assignments", icon: ListChecks },
  { to: "/reports/students", label: "Report", icon: FileText },
];

export function Sidebar() {
  const { user } = useAuth();
  const { isCollapsed } = useSidebar();
  const items = user?.role === ROLES.STUDENT ? studentNav : teacherNav;

  return (
    <aside className={`sidebar ${isCollapsed ? "sidebar-collapsed" : ""}`} aria-label="Primary navigation">
      <div className="brand">
        <GraduationCap size={28} aria-hidden="true" />
        <span>EduTrack Pro</span>
      </div>
      <nav className="nav-list">
        {items.map((item) => (
          <NavLink key={item.to} to={item.to} className="nav-link">
            <item.icon size={19} aria-hidden="true" />
            <span>{item.label}</span>
          </NavLink>
        ))}
      </nav>
      <NavLink to="/settings" className="nav-link nav-link-bottom">
        <Settings size={19} aria-hidden="true" />
        <span>Settings</span>
      </NavLink>
    </aside>
  );
}
