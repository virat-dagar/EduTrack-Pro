import heroImage from "../assets/hero.png";

export function AuthLayout({ children }) {
  return (
    <main className="auth-layout">
      <section className="auth-visual" aria-label="EduTrack Pro">
        <img src={heroImage} alt="" />
        <div>
          <h1>EduTrack Pro</h1>
          <p>Academic records, insights, and reporting in one calm workspace.</p>
        </div>
      </section>
      <section className="auth-panel">{children}</section>
    </main>
  );
}
