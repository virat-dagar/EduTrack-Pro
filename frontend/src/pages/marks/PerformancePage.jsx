import { Award, Star } from "lucide-react";
import { useEffect, useState } from "react";
import { useAuth } from "../../hooks/useAuth";
import { marksService } from "../../services/marksService";
import { studentService } from "../../services/studentService";
import { StatCard } from "../../components/dashboard/StatCard";
import { ErrorState } from "../../components/feedback/ErrorState";
import { LoadingState } from "../../components/feedback/LoadingState";
import { PageHeader } from "../../components/layout/PageHeader";
import { ROLES } from "../../utils/constants";
import { formatPercent } from "../../utils/formatters";

export default function PerformancePage() {
  const { user } = useAuth();
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    let ignore = false;
    async function loadPerformance() {
      setIsLoading(true);
      setError(null);
      try {
        let response;
        if (user?.role === ROLES.STUDENT) {
          const profile = await studentService.me();
          response = await marksService.average(profile.data.id);
        } else {
          response = await marksService.summary();
        }
        if (!ignore) setData(response.data);
      } catch (apiError) {
        if (!ignore) setError(apiError);
      } finally {
        if (!ignore) setIsLoading(false);
      }
    }
    loadPerformance();
    return () => {
      ignore = true;
    };
  }, [user?.role]);

  if (isLoading) return <LoadingState label="Loading performance" />;
  if (error) return <ErrorState message={error.message} />;

  const summary = data || {};
  return (
    <>
      <PageHeader title="Performance" description="Calculated from marks records." />
      <section className="stat-grid">
        <StatCard title="Average" value={formatPercent(summary.average_percentage || summary.average_marks)} icon={Star} tone="amber" />
        <StatCard title="Grade" value={summary.grade || "Institution"} icon={Award} tone="green" />
      </section>
    </>
  );
}
