import { GraduationCap, LogOut, Moon, Sun } from "lucide-react";
import { useNavigate } from "react-router-dom";
import { Button } from "../common/Button";
import { useAuth } from "../../hooks/useAuth";
import { useSidebar } from "../../hooks/useSidebar";
import { useTheme } from "../../hooks/useTheme";

export function Navbar() {
  const { user, logout } = useAuth();
  const { toggleSidebar, isCollapsed } = useSidebar();
  const { theme, toggleTheme } = useTheme();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/login", { replace: true });
  };

  return (
    <header className="topbar">
        <div className="topbar-brand">
      <GraduationCap size={38} />
      <span>EduTrack Pro</span>
          </div>
      <div className="topbar-user">
        <span>{user?.full_name}</span>
        <small>{user?.role}</small>
      </div>
      <Button
        variant="ghost"
        size="icon"
        icon={theme === "dark" ? Sun : Moon}
        onClick={toggleTheme}
        aria-label="Toggle theme"
      />
      <Button variant="secondary" icon={LogOut} onClick={handleLogout}>
        Logout
      </Button>
    </header>
  );
}
