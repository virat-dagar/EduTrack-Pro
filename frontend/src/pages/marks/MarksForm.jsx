import { Save } from "lucide-react";
import { useState } from "react";
import { toast } from "react-toastify";
import { Button } from "../../components/common/Button";
import { Card } from "../../components/common/Card";
import { Input } from "../../components/common/Input";
import { PageHeader } from "../../components/layout/PageHeader";
import { marksService } from "../../services/marksService";
import { ASSESSMENT_TYPES } from "../../utils/constants";
import { todayISO } from "../../utils/dateUtils";

export default function MarksForm() {
  const [values, setValues] = useState({
    student_id: "",
    subject_id: "",
    assessment_type: "Mid Semester",
    marks_obtained: "",
    maximum_marks: "",
    examination_date: todayISO(),
    remarks: "",
  });
  const [isSubmitting, setIsSubmitting] = useState(false);
  const updateValue = (field, value) => setValues((current) => ({ ...current, [field]: value }));

  const handleSubmit = async (event) => {
    event.preventDefault();
    setIsSubmitting(true);
    try {
      await marksService.create({
        ...values,
        student_id: Number(values.student_id),
        subject_id: Number(values.subject_id),
        marks_obtained: Number(values.marks_obtained),
        maximum_marks: Number(values.maximum_marks),
      });
      toast.success("Marks added successfully.");
    } catch (error) {
      toast.error(error.message || "Unable to save marks.");
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <>
      <PageHeader title="Add Marks" description="Record assessment scores for a student." />
      <Card>
        <form className="form-grid" onSubmit={handleSubmit}>
          <Input label="Student ID" name="student_id" type="number" min="1" value={values.student_id} onChange={(event) => updateValue("student_id", event.target.value)} required />
          <Input label="Subject ID" name="subject_id" type="number" min="1" value={values.subject_id} onChange={(event) => updateValue("subject_id", event.target.value)} required />
          <label className="field" htmlFor="assessment_type">
            <span className="field-label">Assessment Type</span>
            <select id="assessment_type" className="input" value={values.assessment_type} onChange={(event) => updateValue("assessment_type", event.target.value)}>
              {ASSESSMENT_TYPES.map((type) => <option key={type}>{type}</option>)}
            </select>
          </label>
          <Input label="Marks Obtained" name="marks_obtained" type="number" min="0" step="0.01" value={values.marks_obtained} onChange={(event) => updateValue("marks_obtained", event.target.value)} required />
          <Input label="Maximum Marks" name="maximum_marks" type="number" min="1" step="0.01" value={values.maximum_marks} onChange={(event) => updateValue("maximum_marks", event.target.value)} required />
          <Input label="Examination Date" name="examination_date" type="date" value={values.examination_date} onChange={(event) => updateValue("examination_date", event.target.value)} required />
          <Input label="Remarks" name="remarks" value={values.remarks} onChange={(event) => updateValue("remarks", event.target.value)} />
          <div className="form-actions">
            <Button type="submit" icon={Save} isLoading={isSubmitting}>Save Marks</Button>
          </div>
        </form>
      </Card>
    </>
  );
}
