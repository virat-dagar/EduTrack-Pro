import { Award, BookOpen, ClipboardCheck, ListChecks, Star, TrendingUp } from "lucide-react";
import { ChartCard } from "../../components/charts/ChartCard";
import { Card } from "../../components/common/Card";
import { StatCard } from "../../components/dashboard/StatCard";
import { ErrorState } from "../../components/feedback/ErrorState";
import { LoadingState } from "../../components/feedback/LoadingState";
import { PageHeader } from "../../components/layout/PageHeader";
import { Badge } from "../../components/ui/Badge";
import { useApi } from "../../hooks/useApi";
import { dashboardService } from "../../services/dashboardService";
import { formatPercent } from "../../utils/formatters";
import { useAuth } from "../../hooks/useAuth";

export default function StudentDashboard() {
  const { user } = useAuth();
  const summary = useApi(() => dashboardService.student(), []);
  const charts = useApi(() => dashboardService.studentCharts(), []);

  if (summary.isLoading) return <LoadingState label="Loading dashboard" />;
  if (summary.error) return <ErrorState message={summary.error.message} />;

  const data = summary.data || {};
  const chartData = charts.data || {};

  return (
    <>
      <PageHeader title={`👋 Hii, ${user?.full_name?.split(" ")[0] || "Student"}!`} description="Your academic progress at a glance."/>
      <section className="stat-grid">
        <StatCard title="Attendance" value={formatPercent(data.attendance_percentage)} icon={ClipboardCheck} tone="teal" />
        <StatCard title="Average Marks" value={formatPercent(data.average_marks)} icon={Star} tone="amber" />
        <StatCard title="Grade" value={data.grade} icon={Award} tone="green" />
        <StatCard title="Pending Assignments" value={data.pending_assignments} icon={ListChecks} tone="red" />
        <StatCard title="Subjects" value={data.subjects} icon={BookOpen} tone="blue" />
        <StatCard title="Performance" value={formatPercent(data.performance_score)} icon={TrendingUp} tone="violet" />
      </section>
      <Card className="profile-highlight">
        <span>Scholarship Status</span>
        <Badge tone={data.scholarship_status === "Eligible" ? "success" : "warning"}>{data.scholarship_status}</Badge>
      </Card>
      <section className="content-grid">
        <ChartCard title="Marks by Subject" data={chartData.marks_by_subject || []} xKey="subject" dataKey="average" />
        <ChartCard title="Assignment Progress" data={chartData.assignment_progress || []} />
      </section>
    </>
  );
}
