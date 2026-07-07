import { Eye, Plus } from "lucide-react";
import { Link } from "react-router-dom";
import { ErrorState } from "../../components/feedback/ErrorState";
import { LoadingState } from "../../components/feedback/LoadingState";
import { PageHeader } from "../../components/layout/PageHeader";
import { DataTable } from "../../components/tables/DataTable";
import { Badge } from "../../components/ui/Badge";
import { useAuth } from "../../hooks/useAuth";
import { useApi } from "../../hooks/useApi";
import { assignmentService } from "../../services/assignmentService";
import { ROLES } from "../../utils/constants";
import { formatDate } from "../../utils/dateUtils";

function statusTone(status) {
  if (status === "Reviewed") return "success";
  if (status === "Submitted") return "warning";
  if (status === "Late") return "danger";
  return "neutral";
}

export default function AssignmentsList() {
  const { user } = useAuth();
  const assignments = useApi(() => assignmentService.list({ page_size: 100 }), []);

  if (assignments.isLoading) return <LoadingState label="Loading assignments" />;
  if (assignments.error) return <ErrorState message={assignments.error.message} />;

  const isStudent = user?.role === ROLES.STUDENT;

  return (
    <>
      <PageHeader
        title={isStudent ? "My Assignments" : "Assignments"}
        description={isStudent ? "View work assigned to your classroom, upload solutions, and track grades." : "Deadlines, submissions, and review status."}
        actions={user?.role === ROLES.TEACHER ? <Link className="btn btn-primary btn-md" to="/assignments/create"><Plus size={18} aria-hidden="true" /><span>New Assignment</span></Link> : null}
      />
      <DataTable
        rows={assignments.data?.items || []}
        columns={[
          { key: "title", header: "Title" },
          { key: "subject", header: "Subject" },
          { key: "classroom", header: "Classroom", render: (row) => row.classroom || "-" },
          { key: "total_marks", header: "Marks" },
          { key: "due_date", header: "Due", render: (row) => formatDate(row.due_date) },
          {
            key: "status",
            header: isStudent ? "My Status" : "Status",
            render: (row) => isStudent
              ? <Badge tone={statusTone(row.submission_status)}>{row.submission_status || "Pending"}</Badge>
              : <Badge tone={row.is_active ? "success" : "neutral"}>{row.is_active ? "Active" : "Inactive"}</Badge>,
          },
          {
            key: "grade",
            header: "Grade",
            render: (row) => row.submission_grade ? `${row.submission_grade} (${row.submission_percentage}%)` : "-",
          },
          {
            key: "actions",
            header: "Actions",
            render: (row) => (
              <Link className="btn btn-secondary btn-sm" to={`/assignments/${row.id}`}>
                <Eye size={16} aria-hidden="true" />
                <span>{isStudent ? "Open" : "View"}</span>
              </Link>
            ),
          },
        ]}
      />
    </>
  );
}
