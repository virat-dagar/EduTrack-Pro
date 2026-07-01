import {
  Bar,
  BarChart,
  CartesianGrid,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import { Card } from "../common/Card";
import { EmptyState } from "../feedback/EmptyState";

export function ChartCard({ title, data = [], dataKey = "value", xKey = "name", type = "bar" }) {
  return (
    <Card className="chart-card">
      <h2>{title}</h2>
      {data.length === 0 ? (
        <EmptyState title="No chart data yet" />
      ) : (
        <ResponsiveContainer width="100%" height={260}>
          {type === "line" ? (
            <LineChart data={data}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey={xKey} />
              <YAxis />
              <Tooltip />
              <Line type="monotone" dataKey={dataKey} stroke="var(--color-accent)" strokeWidth={2} />
            </LineChart>
          ) : (
            <BarChart data={data}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey={xKey} />
              <YAxis />
              <Tooltip />
              <Bar dataKey={dataKey} fill="var(--color-accent)" radius={[6, 6, 0, 0]} />
            </BarChart>
          )}
        </ResponsiveContainer>
      )}
    </Card>
  );
}
