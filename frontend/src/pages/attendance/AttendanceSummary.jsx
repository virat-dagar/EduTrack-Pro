import { ClipboardCheck, Clock, UserMinus, UsersRound } from "lucide-react";
import { StatCard } from "../../components/dashboard/StatCard";
import { ErrorState } from "../../components/feedback/ErrorState";
import { LoadingState } from "../../components/feedback/LoadingState";
import { PageHeader } from "../../components/layout/PageHeader";
import { useApi } from "../../hooks/useApi";
import { attendanceService } from "../../services/attendanceService";

export default function AttendanceSummary() {
  const summary = useApi(() => attendanceService.summary(), []);
  if (summary.isLoading) return <LoadingState label="Loading summary" />;
  if (summary.error) return <ErrorState message={summary.error.message} />;
  const data = summary.data || {};

  return (
    <>
      <PageHeader title="Attendance Summary" description="Institution-wide attendance totals." />
      <section className="stat-grid">
        <StatCard title="Records" value={data.total_records} icon={UsersRound} tone="blue" />
        <StatCard title="Present" value={data.present} icon={ClipboardCheck} tone="green" />
        <StatCard title="Absent" value={data.absent} icon={UserMinus} tone="red" />
        <StatCard title="Late" value={data.late} icon={Clock} tone="amber" />
      </section>
    </>
  );
}
