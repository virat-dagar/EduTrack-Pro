import { Card } from "../common/Card";

export function StatCard({ title, value, detail, icon: Icon, tone = "blue" }) {
  return (
    <Card className={`stat-card stat-${tone}`}>
      <div className="stat-icon">{Icon ? <Icon size={22} aria-hidden="true" /> : null}</div>
      <div>
        <p>{title}</p>
        <strong>{value}</strong>
        {detail ? <span>{detail}</span> : null}
      </div>
    </Card>
  );
}
