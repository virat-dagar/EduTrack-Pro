import { AlertTriangle, BookOpen, ClipboardCheck, FileText, ListChecks, Star, UsersRound } from "lucide-react";
import { ChartCard } from "../../components/charts/ChartCard";
import { Card } from "../../components/common/Card";
import { StatCard } from "../../components/dashboard/StatCard";
import { ErrorState } from "../../components/feedback/ErrorState";
import { LoadingState } from "../../components/feedback/LoadingState";
import { PageHeader } from "../../components/layout/PageHeader";
import { useApi } from "../../hooks/useApi";
import { dashboardService } from "../../services/dashboardService";
import { formatPercent } from "../../utils/formatters";
import { useAuth } from "../../hooks/useAuth";

export default function TeacherDashboard() {
  const { user } = useAuth();
  const summary = useApi(() => dashboardService.teacher(), []);
  const charts = useApi(() => dashboardService.teacherCharts(), []);
  const activity = useApi(() => dashboardService.teacherActivity(), []);

  if (summary.isLoading) return <LoadingState label="Loading dashboard" />;
  if (summary.error) return <ErrorState message={summary.error.message} />;

  const data = summary.data || {};
  const chartData = charts.data || {};
  const activities = activity.data?.items || [];

  return (
    <>
      <PageHeader title={`👋 Hii, ${user?.full_name?.split(" ")[0] || "Teacher"}!`} description="Institution-wide academic overview."/>
      <section className="stat-grid">
        <StatCard title="Students" value={data.total_students} icon={UsersRound} tone="blue" />
        <StatCard title="Subjects" value={data.total_subjects} icon={BookOpen} tone="green" />
        <StatCard title="Attendance" value={formatPercent(data.attendance_percentage)} icon={ClipboardCheck} tone="teal" />
        <StatCard title="Average Marks" value={formatPercent(data.average_marks)} icon={Star} tone="amber" />
        <StatCard title="Assignments" value={data.assignments} icon={ListChecks} tone="violet" />
        <StatCard title="Pending Reviews" value={data.pending_reviews} icon={FileText} tone="gray" />
        <StatCard title="At Risk" value={data.at_risk_students} icon={AlertTriangle} tone="red" />
      </section>
      <section className="content-grid">
        <ChartCard title="Attendance Trend" data={chartData.attendance_trend || []} xKey="date" dataKey="percentage" type="line" />
        <ChartCard title="Semester Distribution" data={chartData.semester_distribution || []} />
      </section>
      <Card className="activity-card">
        <h2>Recent Activity</h2>
        <ul className="activity-list">
          {activities.map((item, index) => (
            <li key={`${item.type}-${index}`}>
              <strong>{item.type}</strong>
              <span>{item.message}</span>
            </li>
          ))}
        </ul>
      </Card>
    </>
  );
}
