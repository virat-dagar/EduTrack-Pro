import { Edit } from "lucide-react";
import { Link, useParams } from "react-router-dom";
import { Card } from "../../components/common/Card";
import { ErrorState } from "../../components/feedback/ErrorState";
import { LoadingState } from "../../components/feedback/LoadingState";
import { PageHeader } from "../../components/layout/PageHeader";
import { useAuth } from "../../hooks/useAuth";
import { useApi } from "../../hooks/useApi";
import { studentService } from "../../services/studentService";
import { ROLES } from "../../utils/constants";

export default function StudentDetail() {
  const { id } = useParams();
  const { user } = useAuth();
  const student = useApi(() => studentService.get(id), [id]);

  if (student.isLoading) return <LoadingState label="Loading student" />;
  if (student.error) return <ErrorState message={student.error.message} />;

  const data = student.data;

  return (
    <>
      <PageHeader
        title={`${data.first_name} ${data.last_name}`}
        description={`${data.roll_number} · ${data.department}`}
        actions={
          user?.role === ROLES.TEACHER ? (
            <Link className="btn btn-secondary btn-md" to={`/students/edit/${data.id}`}>
              <Edit size={18} aria-hidden="true" />
              <span>Edit</span>
            </Link>
          ) : null
        }
      />
      <Card>
        <dl className="detail-grid">
          {Object.entries(data).map(([key, value]) => (
            <div key={key}>
              <dt>{key.replaceAll("_", " ")}</dt>
              <dd>{String(value ?? "-")}</dd>
            </div>
          ))}
        </dl>
      </Card>
    </>
  );
}
