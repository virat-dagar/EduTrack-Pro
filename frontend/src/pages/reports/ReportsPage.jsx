import { useEffect, useState } from "react";
import { Button } from "../../components/common/Button";
import { Card } from "../../components/common/Card";
import { Input } from "../../components/common/Input";
import { ErrorState } from "../../components/feedback/ErrorState";
import { LoadingState } from "../../components/feedback/LoadingState";
import { PageHeader } from "../../components/layout/PageHeader";
import { useAuth } from "../../hooks/useAuth";
import { reportService } from "../../services/reportService";
import { studentService } from "../../services/studentService";
import { ROLES } from "../../utils/constants";

const reportLoaders = {
  attendance: reportService.attendance,
  marks: reportService.marks,
  institution: reportService.institution,
};

export default function ReportsPage({ type }) {
  const { user } = useAuth();
  const [studentId, setStudentId] = useState("");
  const [report, setReport] = useState(null);
  const [error, setError] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    let ignore = false;
    async function loadReport() {
      setIsLoading(true);
      setError(null);
      try {
        let response;
        if (type === "students") {
          if (user?.role === ROLES.STUDENT) {
            const profile = await studentService.me();
            response = await reportService.student(profile.data.id);
          } else if (studentId) {
            response = await reportService.student(studentId);
          } else {
            response = { data: null };
          }
        } else {
          response = await reportLoaders[type]();
        }
        if (!ignore) setReport(response.data);
      } catch (apiError) {
        if (!ignore) setError(apiError);
      } finally {
        if (!ignore) setIsLoading(false);
      }
    }
    loadReport();
    return () => {
      ignore = true;
    };
  }, [type, user?.role, studentId]);

  if (isLoading) return <LoadingState label="Loading report" />;
  if (error) return <ErrorState message={error.message} />;

  return (
    <>
      <PageHeader title="Reports" description="Structured academic summaries for review and demonstration." />
      {type === "students" && user?.role === ROLES.TEACHER ? (
        <Card className="toolbar-card">
          <Input label="Student ID" name="student_id" type="number" min="1" value={studentId} onChange={(event) => setStudentId(event.target.value)} />
          <Button onClick={() => setStudentId(studentId)}>Generate</Button>
        </Card>
      ) : null}
      <Card>
        {report ? (
          <dl className="detail-grid">
            {Object.entries(report).map(([key, value]) => (
              <div key={key}>
                <dt>{key.replaceAll("_", " ")}</dt>
                <dd>{typeof value === "object" ? JSON.stringify(value) : String(value ?? "-")}</dd>
              </div>
            ))}
          </dl>
        ) : (
          <p className="muted">Enter a student ID to generate the report.</p>
        )}
      </Card>
    </>
  );
}
