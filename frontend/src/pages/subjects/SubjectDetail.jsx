import { Edit } from "lucide-react";
import { Link, useParams } from "react-router-dom";
import { Card } from "../../components/common/Card";
import { ErrorState } from "../../components/feedback/ErrorState";
import { LoadingState } from "../../components/feedback/LoadingState";
import { PageHeader } from "../../components/layout/PageHeader";
import { useAuth } from "../../hooks/useAuth";
import { useApi } from "../../hooks/useApi";
import { subjectService } from "../../services/subjectService";
import { ROLES } from "../../utils/constants";

export default function SubjectDetail() {
  const { id } = useParams();
  const { user } = useAuth();
  const subject = useApi(() => subjectService.get(id), [id]);

  if (subject.isLoading) return <LoadingState label="Loading subject" />;
  if (subject.error) return <ErrorState message={subject.error.message} />;

  const data = subject.data;
  return (
    <>
      <PageHeader
        title={data.subject_name}
        description={`${data.subject_code} · Semester ${data.semester}`}
        actions={user?.role === ROLES.TEACHER ? <Link className="btn btn-secondary btn-md" to={`/subjects/edit/${data.id}`}><Edit size={18} aria-hidden="true" /><span>Edit</span></Link> : null}
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
