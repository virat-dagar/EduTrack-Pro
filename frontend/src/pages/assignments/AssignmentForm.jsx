import { Save } from "lucide-react";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { toast } from "react-toastify";
import { Button } from "../../components/common/Button";
import { Card } from "../../components/common/Card";
import { Input } from "../../components/common/Input";
import { PageHeader } from "../../components/layout/PageHeader";
import { assignmentService } from "../../services/assignmentService";
import { todayISO } from "../../utils/dateUtils";

export default function AssignmentForm() {
  const navigate = useNavigate();
  const [values, setValues] = useState({
    subject_id: "",
    title: "",
    description: "",
    total_marks: "",
    assigned_date: todayISO(),
    due_date: todayISO(),
  });
  const [isSubmitting, setIsSubmitting] = useState(false);
  const updateValue = (field, value) => setValues((current) => ({ ...current, [field]: value }));

  const handleSubmit = async (event) => {
    event.preventDefault();
    setIsSubmitting(true);
    try {
      await assignmentService.create({
        ...values,
        subject_id: Number(values.subject_id),
        total_marks: Number(values.total_marks),
      });
      toast.success("Assignment created successfully.");
      navigate("/assignments/list");
    } catch (error) {
      toast.error(error.message || "Unable to save assignment.");
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <>
      <PageHeader title="Create Assignment" description="Set instructions, marks, and due date." />
      <Card>
        <form className="form-grid" onSubmit={handleSubmit}>
          <Input label="Subject ID" name="subject_id" type="number" min="1" value={values.subject_id} onChange={(event) => updateValue("subject_id", event.target.value)} required />
          <Input label="Title" name="title" value={values.title} onChange={(event) => updateValue("title", event.target.value)} required />
          <Input label="Description" name="description" value={values.description} onChange={(event) => updateValue("description", event.target.value)} required />
          <Input label="Total Marks" name="total_marks" type="number" min="1" step="0.01" value={values.total_marks} onChange={(event) => updateValue("total_marks", event.target.value)} required />
          <Input label="Assigned Date" name="assigned_date" type="date" value={values.assigned_date} onChange={(event) => updateValue("assigned_date", event.target.value)} required />
          <Input label="Due Date" name="due_date" type="date" value={values.due_date} onChange={(event) => updateValue("due_date", event.target.value)} required />
          <div className="form-actions">
            <Button type="submit" icon={Save} isLoading={isSubmitting}>Save Assignment</Button>
          </div>
        </form>
      </Card>
    </>
  );
}
