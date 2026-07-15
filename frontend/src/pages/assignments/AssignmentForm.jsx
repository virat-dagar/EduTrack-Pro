import { Plus, Save, Trash2 } from "lucide-react";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { toast } from "react-toastify";
import { Button } from "../../components/common/Button";
import { Card } from "../../components/common/Card";
import { Input } from "../../components/common/Input";
import { PageHeader } from "../../components/layout/PageHeader";
import { assignmentService } from "../../services/assignmentService";
import { todayISO } from "../../utils/dateUtils";

const initialQuestion = { question_no: 1, title: "Question 1", max_marks: 5 };

export default function AssignmentForm() {
  const navigate = useNavigate();
  const [values, setValues] = useState({
    classroom_id: "",
    subject_id: "",
    title: "",
    description: "",
    total_marks: "",
    assigned_date: todayISO(),
    due_date: todayISO(),
    is_published: true,
  });
  const [pdfFile, setPdfFile] = useState(null);
  const [questions, setQuestions] = useState([initialQuestion]);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const updateValue = (field, value) => setValues((current) => ({ ...current, [field]: value }));

  const updateQuestion = (index, field, value) => {
    setQuestions((current) =>
      current.map((question, currentIndex) =>
        currentIndex === index ? { ...question, [field]: value } : question,
      ),
    );
  };

  const addQuestion = () => {
    setQuestions((current) => [
      ...current,
      {
        question_no: current.length + 1,
        title: `Question ${current.length + 1}`,
        max_marks: 5,
      },
    ]);
  };

  const removeQuestion = (index) => {
    setQuestions((current) =>
      current
        .filter((_, currentIndex) => currentIndex !== index)
        .map((question, currentIndex) => ({ ...question, question_no: currentIndex + 1 })),
    );
  };

  const questionTotal = questions.reduce((total, question) => total + Number(question.max_marks || 0), 0);

  const handleSubmit = async (event) => {
    event.preventDefault();
    setIsSubmitting(true);
    try {
      let pdfFileUrl = null;
      if (pdfFile) {
        const uploadResponse = await assignmentService.upload(pdfFile);
        pdfFileUrl = uploadResponse.data.file_url;
      }
      await assignmentService.create({
        classroom_id: values.classroom_id ? Number(values.classroom_id) : undefined,
        subject_id: Number(values.subject_id),
        title: values.title,
        description: values.description,
        pdf_file: pdfFileUrl,
        total_marks: values.total_marks ? Number(values.total_marks) : undefined,
        assigned_date: values.assigned_date,
        due_date: values.due_date,
        is_published: values.is_published,
        questions: questions
          .filter((question) => Number(question.max_marks) > 0)
          .map((question) => ({
            question_no: Number(question.question_no),
            title: question.title || null,
            max_marks: Number(question.max_marks),
          })),
      });
      toast.success("Assignment created successfully.");
      navigate("/assignments/list");
    } catch (error) {
      const detail = Array.isArray(error.errors) && error.errors.length
        ? error.errors.map((item) => `${item.field.replace(/^body\./, "")}: ${item.message}`).join(" | ")
        : null;
      toast.error(detail || error.message || "Unable to save assignment.");
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <>
      <PageHeader title="Create Assignment" description="Publish classroom assignments with question-wise grading." />
      <Card>
        <form className="form-grid" onSubmit={handleSubmit}>
          <Input label="Classroom ID" name="classroom_id" type="number" min="1" value={values.classroom_id} onChange={(event) => updateValue("classroom_id", event.target.value)} />
          <Input label="Subject ID" name="subject_id" type="number" min="1" value={values.subject_id} onChange={(event) => updateValue("subject_id", event.target.value)} required />
          <Input label="Title" name="title" value={values.title} onChange={(event) => updateValue("title", event.target.value)} required />
          <Input label="Description" name="description" value={values.description} onChange={(event) => updateValue("description", event.target.value)} required />
          <label className="field" htmlFor="assignment-file">
            <span className="field-label">Assignment file (optional)</span>
            <input
              id="assignment-file"
              className="input"
              type="file"
              accept=".pdf,.doc,.docx,.png,.jpg,.jpeg,.zip"
              onChange={(event) => setPdfFile(event.target.files?.[0] || null)}
            />
          </label>
          <Input label="Fallback Total Marks" name="total_marks" type="number" min="1" step="0.01" value={values.total_marks} onChange={(event) => updateValue("total_marks", event.target.value)} hint={`Question total: ${questionTotal}`} />
          <Input label="Assigned Date" name="assigned_date" type="date" value={values.assigned_date} onChange={(event) => updateValue("assigned_date", event.target.value)} required />
          <Input label="Due Date" name="due_date" type="date" value={values.due_date} onChange={(event) => updateValue("due_date", event.target.value)} required />
          <label className="checkbox-field">
            <input type="checkbox" checked={values.is_published} onChange={(event) => updateValue("is_published", event.target.checked)} />
            <span>Publish immediately</span>
          </label>
          <div className="form-actions">
            <Button type="submit" icon={Save} isLoading={isSubmitting}>Save Assignment</Button>
          </div>
        </form>
      </Card>

      <Card className="mt-4">
        <div className="section-heading">
          <h2>Question-wise marks</h2>
          <Button variant="secondary" icon={Plus} onClick={addQuestion}>Add Question</Button>
        </div>
        <div className="question-list">
          {questions.map((question, index) => (
            <div className="question-row" key={question.question_no}>
              <Input label="No." name={`question_no_${index}`} type="number" min="1" value={question.question_no} onChange={(event) => updateQuestion(index, "question_no", event.target.value)} />
              <Input label="Title" name={`question_title_${index}`} value={question.title} onChange={(event) => updateQuestion(index, "title", event.target.value)} />
              <Input label="Max Marks" name={`question_marks_${index}`} type="number" min="0.5" step="0.5" value={question.max_marks} onChange={(event) => updateQuestion(index, "max_marks", event.target.value)} />
              <Button variant="secondary" icon={Trash2} disabled={questions.length === 1} onClick={() => removeQuestion(index)}>Remove</Button>
            </div>
          ))}
        </div>
      </Card>
    </>
  );
}