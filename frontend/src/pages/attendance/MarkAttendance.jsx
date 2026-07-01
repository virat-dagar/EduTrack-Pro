import { Save } from "lucide-react";
import { useState } from "react";
import { toast } from "react-toastify";
import { Button } from "../../components/common/Button";
import { Card } from "../../components/common/Card";
import { Input } from "../../components/common/Input";
import { PageHeader } from "../../components/layout/PageHeader";
import { attendanceService } from "../../services/attendanceService";
import { ATTENDANCE_STATUSES } from "../../utils/constants";
import { todayISO } from "../../utils/dateUtils";

export default function MarkAttendance() {
  const [values, setValues] = useState({
    student_id: "",
    subject_id: "",
    attendance_date: todayISO(),
    status: "Present",
    remarks: "",
  });
  const [isSubmitting, setIsSubmitting] = useState(false);
  const updateValue = (field, value) => setValues((current) => ({ ...current, [field]: value }));

  const handleSubmit = async (event) => {
    event.preventDefault();
    setIsSubmitting(true);
    try {
      await attendanceService.create({
        ...values,
        student_id: Number(values.student_id),
        subject_id: Number(values.subject_id),
      });
      toast.success("Attendance marked successfully.");
      setValues({ ...values, remarks: "" });
    } catch (error) {
      toast.error(error.message || "Unable to mark attendance.");
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <>
      <PageHeader title="Mark Attendance" description="Record daily attendance for a student and subject." />
      <Card>
        <form className="form-grid" onSubmit={handleSubmit}>
          <Input label="Student ID" name="student_id" type="number" min="1" value={values.student_id} onChange={(event) => updateValue("student_id", event.target.value)} required />
          <Input label="Subject ID" name="subject_id" type="number" min="1" value={values.subject_id} onChange={(event) => updateValue("subject_id", event.target.value)} required />
          <Input label="Date" name="attendance_date" type="date" value={values.attendance_date} onChange={(event) => updateValue("attendance_date", event.target.value)} required />
          <label className="field" htmlFor="status">
            <span className="field-label">Status</span>
            <select id="status" className="input" value={values.status} onChange={(event) => updateValue("status", event.target.value)}>
              {ATTENDANCE_STATUSES.map((status) => <option key={status}>{status}</option>)}
            </select>
          </label>
          <Input label="Remarks" name="remarks" value={values.remarks} onChange={(event) => updateValue("remarks", event.target.value)} />
          <div className="form-actions">
            <Button type="submit" icon={Save} isLoading={isSubmitting}>Save Attendance</Button>
          </div>
        </form>
      </Card>
    </>
  );
}
