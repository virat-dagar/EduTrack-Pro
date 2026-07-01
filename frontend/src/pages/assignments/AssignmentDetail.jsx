import { useParams } from "react-router-dom";
import { Card } from "../../components/common/Card";
import { ErrorState } from "../../components/feedback/ErrorState";
import { LoadingState } from "../../components/feedback/LoadingState";
import { PageHeader } from "../../components/layout/PageHeader";
import { useApi } from "../../hooks/useApi";
import { assignmentService } from "../../services/assignmentService";

export default function AssignmentDetail() {
  const { id } = useParams();
  const assignment = useApi(() => assignmentService.get(id), [id]);

  if (assignment.isLoading) return <LoadingState label="Loading assignment" />;
  if (assignment.error) return <ErrorState message={assignment.error.message} />;
  const data = assignment.data;

  return (
    <>
      <PageHeader title={data.title} description={`Subject ${data.subject_id} · ${data.total_marks} marks`} />
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
