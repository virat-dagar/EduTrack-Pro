import heroDark from "../assets/hero-dark.png";
import heroLight from "../assets/hero-light.png";
import { useTheme } from "../hooks/useTheme";

export function AuthLayout({ children }) {

  const { theme } = useTheme();

  const heroImage = theme === "dark" ? heroDark : heroLight;

  return (
    <main className={`auth-layout ${theme}`}>
      <section className="auth-visual" aria-label="EduTrack Pro">
        <img src={heroImage} alt="" />

        <div className={theme === "dark" ? "auth-text dark" : "auth-text light"}>
          <h1>EduTrack Pro</h1>
          <p>Academic records, insights, and reporting in one calm workspace.</p>
        </div>
      </section>

      <section className="auth-panel">
        {children}
      </section>
    </main>
  );
}