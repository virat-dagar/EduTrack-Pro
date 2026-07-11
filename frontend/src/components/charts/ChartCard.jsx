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
              <Tooltip
  cursor={{
    stroke: "var(--color-accent)",
    strokeWidth: 1,
    strokeDasharray: "4 4",
  }}
  contentStyle={{
    borderRadius: "12px",
    border: "1px solid var(--color-border)",
    background: "var(--color-surface)",
    boxShadow: "0 12px 28px rgba(0,0,0,.18)",
  }}
/>
              <Line
  type="monotone"
  dataKey={dataKey}
  stroke="var(--color-accent)"
  strokeWidth={2}
  dot={{ r: 4 }}
  activeDot={{ r: 6 }}
  isAnimationActive={true}
  animationBegin={250}
  animationDuration={1400}
  animationEasing="ease-out"
/>
            </LineChart>
          ) : (
            <BarChart data={data}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey={xKey} />
              <YAxis />
              <Tooltip />
              <Bar
  dataKey={dataKey}
  fill="var(--color-accent)"
  radius={[6, 6, 0, 0]}
  isAnimationActive={true}
  animationBegin={350}
  animationDuration={1200}
  animationEasing="ease-out"
/>
            </BarChart>
          )}
        </ResponsiveContainer>
      )}
    </Card>
  );
}
