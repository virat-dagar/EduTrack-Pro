import { Plus } from "lucide-react";
import { Link } from "react-router-dom";
import { ErrorState } from "../../components/feedback/ErrorState";
import { LoadingState } from "../../components/feedback/LoadingState";
import { PageHeader } from "../../components/layout/PageHeader";
import { DataTable } from "../../components/tables/DataTable";
import { Badge } from "../../components/ui/Badge";
import { useAuth } from "../../hooks/useAuth";
import { useApi } from "../../hooks/useApi";
import { marksService } from "../../services/marksService";
import { ROLES } from "../../utils/constants";
import { formatDate } from "../../utils/dateUtils";
import { formatPercent } from "../../utils/formatters";

export default function MarksList() {
  const { user } = useAuth();
  const marks = useApi(() => marksService.list({ page_size: 100 }), []);
  if (marks.isLoading) return <LoadingState label="Loading marks" />;
  if (marks.error) return <ErrorState message={marks.error.message} />;

  return (
    <>
      <PageHeader
        title="Marks"
        description="Assessment records and calculated grades."
        actions={user?.role === ROLES.TEACHER ? <Link className="btn btn-primary btn-md" to="/marks/create"><Plus size={18} aria-hidden="true" /><span>Add Marks</span></Link> : null}
      />
      <DataTable
        rows={marks.data?.items || []}
        columns={[
          { key: "examination_date", header: "Date", render: (row) => formatDate(row.examination_date) },
          { key: "student_id", header: "Student ID" },
          { key: "subject_id", header: "Subject ID" },
          { key: "assessment_type", header: "Assessment" },
          { key: "percentage", header: "Score", render: (row) => formatPercent(row.percentage) },
          { key: "grade", header: "Grade", render: (row) => <Badge tone={row.grade === "F" ? "danger" : "success"}>{row.grade}</Badge> },
        ]}
      />
    </>
  );
}
