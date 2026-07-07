import { Download, FileUp, Send, Star, UsersRound } from "lucide-react";
import { useCallback, useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { toast } from "react-toastify";
import { Button } from "../../components/common/Button";
import { Card } from "../../components/common/Card";
import { Input } from "../../components/common/Input";
import { ErrorState } from "../../components/feedback/ErrorState";
import { LoadingState } from "../../components/feedback/LoadingState";
import { PageHeader } from "../../components/layout/PageHeader";
import { DataTable } from "../../components/tables/DataTable";
import { Badge } from "../../components/ui/Badge";
import { useApi } from "../../hooks/useApi";
import { useAuth } from "../../hooks/useAuth";
import { assignmentService } from "../../services/assignmentService";
import { submissionService } from "../../services/submissionService";
import { ROLES } from "../../utils/constants";
import { formatDate } from "../../utils/dateUtils";

const API_ORIGIN = (import.meta.env.VITE_API_BASE_URL || "http://localhost:8000/api/v1").replace("/api/v1", "");

function fileUrl(path) {
  if (!path) return "";
  return path.startsWith("http") ? path : `${API_ORIGIN}${path}`;
}

function statusTone(status) {
  if (status === "Reviewed") return "success";
  if (status === "Submitted") return "warning";
  if (status === "Late") return "danger";
  return "neutral";
}

export default function AssignmentDetail() {
  const { id } = useParams();
  const { role } = useAuth();
  const assignment = useApi(() => assignmentService.get(id), [id]);
  const [summary, setSummary] = useState(null);
  const [submissions, setSubmissions] = useState([]);
  const [selectedSubmission, setSelectedSubmission] = useState(null);
  const [studentSubmission, setStudentSubmission] = useState(null);
  const [gradeScores, setGradeScores] = useState([]);
  const [gradeFeedback, setGradeFeedback] = useState("");
  const [submissionForm, setSubmissionForm] = useState({ file: null, submission_notes: "" });
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isGrading, setIsGrading] = useState(false);

  const loadTeacherData = useCallback(async () => {
    if (role !== ROLES.TEACHER) return;
    try {
      const [summaryResponse, submissionResponse] = await Promise.all([
        assignmentService.submissionSummary(id),
        submissionService.list({ assignment_id: id, page_size: 100 }),
      ]);
      setSummary(summaryResponse.data);
      setSubmissions(submissionResponse.data.items || []);
    } catch {
      setSummary(null);
      setSubmissions([]);
    }
  }, [id, role]);

  useEffect(() => {
    const timer = window.setTimeout(() => {
      loadTeacherData();
    }, 0);
    return () => window.clearTimeout(timer);
  }, [loadTeacherData]);

  useEffect(() => {
    const timer = window.setTimeout(async () => {
      if (role !== ROLES.STUDENT || !assignment.data?.my_submission_id) {
        setStudentSubmission(null);
        return;
      }
      try {
        const response = await submissionService.get(assignment.data.my_submission_id);
        setStudentSubmission(response.data);
      } catch {
        setStudentSubmission(null);
      }
    }, 0);
    return () => window.clearTimeout(timer);
  }, [assignment.data?.my_submission_id, role]);

  const selectSubmission = (item, questions) => {
    setSelectedSubmission(item);
    setGradeFeedback(item.feedback || "");
    setGradeScores(
      questions.map((question) => {
        const existing = item.question_grades?.find((grade) => grade.question_id === question.id);
        return {
          question_id: question.id,
          question_no: question.question_no,
          max_marks: question.max_marks,
          obtained_marks: existing?.obtained_marks ?? "",
        };
      }),
    );
  };

  const updateScore = (questionId, value) => {
    setGradeScores((current) =>
      current.map((score) => (score.question_id === questionId ? { ...score, obtained_marks: value } : score)),
    );
  };

  const submitGrade = async () => {
    if (!selectedSubmission) return;
    setIsGrading(true);
    try {
      await submissionService.review(selectedSubmission.id, {
        status: "Reviewed",
        feedback: gradeFeedback,
        question_scores: gradeScores.map((score) => ({
          question_id: score.question_id,
          obtained_marks: Number(score.obtained_marks),
        })),
      });
      toast.success("Submission graded successfully.");
      setSelectedSubmission(null);
      setGradeScores([]);
      await loadTeacherData();
    } catch (error) {
      toast.error(error.message || "Unable to grade submission.");
    } finally {
      setIsGrading(false);
    }
  };

  const handleStudentSubmit = async (event) => {
    event.preventDefault();
    if (!submissionForm.file) {
      toast.error("Choose a solution file to upload.");
      return;
    }
    setIsSubmitting(true);
    try {
      const uploadResponse = await submissionService.upload(submissionForm.file);
      const payload = {
        submitted_file: uploadResponse.data.file_url,
        submission_notes: submissionForm.submission_notes,
      };
      if (assignment.data.my_submission_id && assignment.data.submission_status !== "Reviewed") {
        await submissionService.update(assignment.data.my_submission_id, payload);
        toast.success("Submission updated successfully.");
      } else {
        await submissionService.create({ ...payload, assignment_id: Number(id) });
        toast.success("Assignment submitted successfully.");
      }
      setSubmissionForm({ file: null, submission_notes: "" });
      assignment.refetch();
    } catch (error) {
      toast.error(error.message || "Unable to submit assignment.");
    } finally {
      setIsSubmitting(false);
    }
  };

  if (assignment.isLoading) return <LoadingState label="Loading assignment" />;
  if (assignment.error) return <ErrorState message={assignment.error.message} />;
  const data = assignment.data;
  const isStudent = role === ROLES.STUDENT;
  const isReviewed = data.submission_status === "Reviewed";
  const canUpload = isStudent && (!data.my_submission_id || data.submission_status !== "Reviewed");

  return (
    <>
      <PageHeader title={data.title} description={`${data.subject || `Subject ${data.subject_id}`} · ${data.total_marks} marks · Due ${formatDate(data.due_date)}`} />

      <div className="content-grid">
        <Card>
          <div className="section-heading">
            <h2>Assignment package</h2>
            <Badge tone={data.is_published ? "success" : "neutral"}>{data.is_published ? "Published" : "Draft"}</Badge>
          </div>
          <dl className="detail-grid">
            <div>
              <dt>Classroom</dt>
              <dd>{data.classroom || data.classroom_id || "-"}</dd>
            </div>
            <div>
              <dt>Assigned</dt>
              <dd>{formatDate(data.assigned_date)}</dd>
            </div>
            <div>
              <dt>Due</dt>
              <dd>{formatDate(data.due_date)}</dd>
            </div>
            <div>
              <dt>File</dt>
              <dd>{data.pdf_file ? <a href={fileUrl(data.pdf_file)} target="_blank" rel="noreferrer"><Download size={16} aria-hidden="true" /> Download</a> : "-"}</dd>
            </div>
          </dl>
          <p>{data.description}</p>
        </Card>

        {isStudent ? (
          <Card>
            <div className="section-heading">
              <h2>My submission</h2>
              <Badge tone={statusTone(data.submission_status)}>{data.submission_status || "Pending"}</Badge>
            </div>
            {data.my_submission_id ? (
              <dl className="detail-grid">
                <div>
                  <dt>Submission ID</dt>
                  <dd>{data.my_submission_id}</dd>
                </div>
                <div>
                  <dt>File</dt>
                  <dd>{data.submission_file ? <a href={fileUrl(data.submission_file)} target="_blank" rel="noreferrer">View uploaded file</a> : "-"}</dd>
                </div>
                <div>
                  <dt>Grade</dt>
                  <dd>{data.submission_grade ? `${data.submission_grade} (${data.submission_percentage}%)` : "Not graded"}</dd>
                </div>
              </dl>
            ) : (
              <p className="muted">No solution submitted yet.</p>
            )}
          </Card>
        ) : (
          <Card>
            <div className="credential-panel">
              <UsersRound size={24} aria-hidden="true" />
              <div>
                <h2>Submissions</h2>
                <p className="muted">
                  {summary ? `${summary.submitted} submitted, ${summary.pending} pending, ${summary.reviewed} reviewed.` : "Submission summary unavailable."}
                </p>
              </div>
            </div>
          </Card>
        )}
      </div>

      <Card>
        <div className="section-heading">
          <h2>Questions</h2>
          <span className="muted">Total: {data.total_marks} marks</span>
        </div>
        <DataTable
          rows={data.questions || []}
          columns={[
            { key: "question_no", header: "Question" },
            { key: "title", header: "Title" },
            { key: "max_marks", header: "Max Marks" },
          ]}
        />
      </Card>

      {canUpload ? (
        <Card className="mt-4">
          <div className="section-heading">
            <h2>{data.my_submission_id ? "Update solution" : "Upload solution"}</h2>
            <span className="muted">PDF, DOC, image, or ZIP up to the configured backend limit.</span>
          </div>
          <form className="form-grid" onSubmit={handleStudentSubmit}>
            <label className="field" htmlFor="solution-file">
              <span className="field-label">Solution File</span>
              <input id="solution-file" className="input" type="file" accept=".pdf,.doc,.docx,.png,.jpg,.jpeg,.zip" onChange={(event) => setSubmissionForm((current) => ({ ...current, file: event.target.files?.[0] || null }))} required />
            </label>
            <Input label="Notes" name="submission_notes" value={submissionForm.submission_notes} onChange={(event) => setSubmissionForm((current) => ({ ...current, submission_notes: event.target.value }))} />
            <div className="form-actions">
              <Button type="submit" icon={data.my_submission_id ? FileUp : Send} isLoading={isSubmitting}>{data.my_submission_id ? "Update Submission" : "Submit Assignment"}</Button>
            </div>
          </form>
        </Card>
      ) : null}

      {isStudent && isReviewed && studentSubmission ? (
        <Card className="mt-4">
          <div className="section-heading">
            <h2>Grade and feedback</h2>
            <Badge tone="success">{studentSubmission.grade || "Reviewed"}</Badge>
          </div>
          <dl className="detail-grid">
            <div>
              <dt>Total</dt>
              <dd>{studentSubmission.total_marks ?? "-"} marks</dd>
            </div>
            <div>
              <dt>Percentage</dt>
              <dd>{studentSubmission.percentage ?? "-"}%</dd>
            </div>
            <div>
              <dt>Feedback</dt>
              <dd>{studentSubmission.feedback || "-"}</dd>
            </div>
          </dl>
          <DataTable
            rows={studentSubmission.question_grades || []}
            columns={[
              { key: "question_no", header: "Question" },
              { key: "obtained_marks", header: "Obtained" },
              { key: "max_marks", header: "Max" },
              { key: "feedback", header: "Feedback", render: (row) => row.feedback || "-" },
            ]}
          />
        </Card>
      ) : null}

      {role === ROLES.TEACHER ? (
        <Card className="mt-4">
          <div className="section-heading">
            <h2>Student submissions</h2>
            <span className="muted">{submissions.length} records</span>
          </div>
          <DataTable
            rows={submissions}
            columns={[
              { key: "id", header: "ID" },
              { key: "student_id", header: "Student ID" },
              { key: "status", header: "Status" },
              { key: "submitted_file", header: "File", render: (row) => row.submitted_file ? <a href={fileUrl(row.submitted_file)} target="_blank" rel="noreferrer">View file</a> : "-" },
              { key: "grade", header: "Grade", render: (row) => row.grade || "-" },
              {
                key: "actions",
                header: "Actions",
                render: (row) => <Button variant="secondary" size="sm" icon={Star} onClick={() => selectSubmission(row, data.questions || [])}>Grade</Button>,
              },
            ]}
          />
        </Card>
      ) : null}

      {selectedSubmission ? (
        <Card className="mt-4">
          <div className="section-heading">
            <h2>Grade submission #{selectedSubmission.id}</h2>
            <Button variant="secondary" onClick={() => setSelectedSubmission(null)}>Cancel</Button>
          </div>
          <div className="question-list">
            {gradeScores.map((score) => (
              <div className="question-row" key={score.question_id}>
                <span>Q{score.question_no}</span>
                <span className="muted">Max {score.max_marks}</span>
                <Input label="Obtained" name={`score_${score.question_id}`} type="number" min="0" max={score.max_marks} step="0.5" value={score.obtained_marks} onChange={(event) => updateScore(score.question_id, event.target.value)} required />
              </div>
            ))}
          </div>
          <Input label="Feedback" name="grade_feedback" value={gradeFeedback} onChange={(event) => setGradeFeedback(event.target.value)} />
          <div className="form-actions">
            <Button icon={Star} isLoading={isGrading} onClick={submitGrade}>Save Grade</Button>
          </div>
        </Card>
      ) : null}
    </>
  );
}
