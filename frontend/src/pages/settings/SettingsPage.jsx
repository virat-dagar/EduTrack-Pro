import { Moon, Sun } from "lucide-react";
import { Button } from "../../components/common/Button";
import { Card } from "../../components/common/Card";
import { PageHeader } from "../../components/layout/PageHeader";
import { useTheme } from "../../hooks/useTheme";

export default function SettingsPage() {
  const { theme, toggleTheme } = useTheme();
  return (
    <>
      <PageHeader title="Settings" description="Personalize your workspace." />
      <Card className="settings-card">
        <div>
          <h2>Theme</h2>
          <p>Current theme: {theme}</p>
        </div>
        <Button icon={theme === "dark" ? Sun : Moon} onClick={toggleTheme}>
          Toggle Theme
        </Button>
      </Card>
    </>
  );
}
