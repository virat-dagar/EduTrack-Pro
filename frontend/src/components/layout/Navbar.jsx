import { LogOut, Menu, Moon, Sun } from "lucide-react";
import { useNavigate } from "react-router-dom";
import { Button } from "../common/Button";
import { useAuth } from "../../hooks/useAuth";
import { useSidebar } from "../../hooks/useSidebar";
import { useTheme } from "../../hooks/useTheme";

export function Navbar() {
  const { user, logout } = useAuth();
  const { toggleSidebar } = useSidebar();
  const { theme, toggleTheme } = useTheme();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/login", { replace: true });
  };

  return (
    <header className="topbar">
      <Button variant="ghost" size="icon" icon={Menu} onClick={toggleSidebar} aria-label="Toggle sidebar" />
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
