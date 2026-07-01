import { Plus } from "lucide-react";
import { Link } from "react-router-dom";
import { ErrorState } from "../../components/feedback/ErrorState";
import { LoadingState } from "../../components/feedback/LoadingState";
import { PageHeader } from "../../components/layout/PageHeader";
import { DataTable } from "../../components/tables/DataTable";
import { useAuth } from "../../hooks/useAuth";
import { useApi } from "../../hooks/useApi";
import { subjectService } from "../../services/subjectService";
import { ROLES } from "../../utils/constants";

export default function SubjectsList() {
  const { user } = useAuth();
  const subjects = useApi(() => subjectService.list({ page_size: 100 }), []);
  if (subjects.isLoading) return <LoadingState label="Loading subjects" />;
  if (subjects.error) return <ErrorState message={subjects.error.message} />;

  return (
    <>
      <PageHeader
        title="Subjects"
        description="Course, department, semester, and credit mapping."
        actions={
          user?.role === ROLES.TEACHER ? (
            <Link className="btn btn-primary btn-md" to="/subjects/create">
              <Plus size={18} aria-hidden="true" />
              <span>New Subject</span>
            </Link>
          ) : null
        }
      />
      <DataTable
        rows={subjects.data?.items || []}
        columns={[
          { key: "subject_code", header: "Code" },
          { key: "subject_name", header: "Name" },
          { key: "department", header: "Department" },
          { key: "semester", header: "Semester" },
          { key: "credits", header: "Credits" },
          { key: "actions", header: "Actions", render: (row) => <Link to={`/subjects/${row.id}`}>View</Link> },
        ]}
      />
    </>
  );
}
