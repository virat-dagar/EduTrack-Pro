import { Plus } from "lucide-react";
import { Link } from "react-router-dom";
import { toast } from "react-toastify";
import { Button } from "../../components/common/Button";
import { ErrorState } from "../../components/feedback/ErrorState";
import { LoadingState } from "../../components/feedback/LoadingState";
import { PageHeader } from "../../components/layout/PageHeader";
import { DataTable } from "../../components/tables/DataTable";
import { Badge } from "../../components/ui/Badge";
import { useAuth } from "../../hooks/useAuth";
import { useApi } from "../../hooks/useApi";
import { assignmentService } from "../../services/assignmentService";
import { submissionService } from "../../services/submissionService";
import { ROLES } from "../../utils/constants";
import { formatDate } from "../../utils/dateUtils";

export default function AssignmentsList() {
  const { user } = useAuth();
  const assignments = useApi(() => assignmentService.list({ page_size: 100 }), []);

  const submitAssignment = async (assignmentId) => {
    try {
      await submissionService.create({ assignment_id: assignmentId, submission_notes: "Submitted from EduTrack Pro." });
      toast.success("Assignment submitted successfully.");
    } catch (error) {
      toast.error(error.message || "Unable to submit assignment.");
    }
  };

  if (assignments.isLoading) return <LoadingState label="Loading assignments" />;
  if (assignments.error) return <ErrorState message={assignments.error.message} />;

  return (
    <>
      <PageHeader
        title="Assignments"
        description="Deadlines, submissions, and review status."
        actions={user?.role === ROLES.TEACHER ? <Link className="btn btn-primary btn-md" to="/assignments/create"><Plus size={18} aria-hidden="true" /><span>New Assignment</span></Link> : null}
      />
      <DataTable
        rows={assignments.data?.items || []}
        columns={[
          { key: "title", header: "Title" },
          { key: "subject", header: "Subject" },
          { key: "total_marks", header: "Marks" },
          { key: "due_date", header: "Due", render: (row) => formatDate(row.due_date) },
          { key: "is_active", header: "Status", render: (row) => <Badge tone={row.is_active ? "success" : "neutral"}>{row.is_active ? "Active" : "Inactive"}</Badge> },
          {
            key: "actions",
            header: "Actions",
            render: (row) => user?.role === ROLES.STUDENT ? <Button variant="secondary" size="sm" onClick={() => submitAssignment(row.id)}>Submit</Button> : <Link to={`/assignments/${row.id}`}>View</Link>,
          },
        ]}
      />
    </>
  );
}
