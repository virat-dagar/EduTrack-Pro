import { ArrowLeft, KeyRound, Save } from "lucide-react";
import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { toast } from "react-toastify";
import { Button } from "../../components/common/Button";
import { Card } from "../../components/common/Card";
import { Input } from "../../components/common/Input";
import { PageHeader } from "../../components/layout/PageHeader";
import { studentService } from "../../services/studentService";
import { todayISO } from "../../utils/dateUtils";

const initialValues = {
  classroom_id: "",
  roll_number: "",
  enrollment_number: "",
  first_name: "",
  last_name: "",
  date_of_birth: "2005-01-01",
  gender: "Other",
  email: "",
  phone: "",
  course: "B.Tech",
  department: "Computer Science",
  semester: 1,
  section: "A",
  academic_year: "2026-27",
  admission_date: todayISO(),
  is_active: true,
};

export default function StudentForm() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [values, setValues] = useState(initialValues);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [createdCredentials, setCreatedCredentials] = useState(null);

  useEffect(() => {
    if (!id) return;
    studentService.get(id).then((response) => setValues({ ...initialValues, ...response.data }));
  }, [id]);

  const updateValue = (field, value) => setValues((current) => ({ ...current, [field]: value }));

  const handleSubmit = async (event) => {
    event.preventDefault();
    setIsSubmitting(true);
    try {
      const payload = {
        ...values,
        semester: Number(values.semester),
        classroom_id: values.classroom_id ? Number(values.classroom_id) : undefined,
      };
      if (!payload.enrollment_number) delete payload.enrollment_number;
      if (!payload.classroom_id) delete payload.classroom_id;
      if (id) {
        await studentService.update(id, payload);
        toast.success("Student updated successfully.");
        navigate("/students/list");
      } else {
        const response = await studentService.create(payload);
        setCreatedCredentials(response.data.generated_credentials || null);
        toast.success("Student created successfully.");
      }
    } catch (error) {
      toast.error(error.message || "Unable to save student.");
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <>
      <PageHeader title={id ? "Edit Student" : "Create Student"} description="Keep academic profile data accurate." />
      {createdCredentials ? (
        <Card className="mb-4">
          <div className="credential-panel">
            <KeyRound size={24} aria-hidden="true" />
            <div>
              <h2>Student login generated</h2>
              <p className="muted">Share these credentials with the student. The password is stored only as a secure hash.</p>
              <dl className="detail-grid">
                <div>
                  <dt>User ID</dt>
                  <dd>{createdCredentials.user_id}</dd>
                </div>
                <div>
                  <dt>Email</dt>
                  <dd>{createdCredentials.email}</dd>
                </div>
                <div>
                  <dt>Temporary Password</dt>
                  <dd>{createdCredentials.password}</dd>
                </div>
              </dl>
              <Button variant="secondary" icon={ArrowLeft} onClick={() => navigate("/students/list")}>Back to Students</Button>
            </div>
          </div>
        </Card>
      ) : null}
      <Card>
        <form className="form-grid" onSubmit={handleSubmit}>
          <Input label="Classroom ID" name="classroom_id" type="number" min="1" value={values.classroom_id || ""} onChange={(event) => updateValue("classroom_id", event.target.value)} />
          <Input label="Roll Number" name="roll_number" value={values.roll_number} onChange={(event) => updateValue("roll_number", event.target.value)} required disabled={Boolean(id)} />
          <Input label="Enrollment Number" name="enrollment_number" value={values.enrollment_number} onChange={(event) => updateValue("enrollment_number", event.target.value)} disabled={Boolean(id)} />
          <Input label="First Name" name="first_name" value={values.first_name} onChange={(event) => updateValue("first_name", event.target.value)} required />
          <Input label="Last Name" name="last_name" value={values.last_name} onChange={(event) => updateValue("last_name", event.target.value)} required />
          <Input label="Date of Birth" name="date_of_birth" type="date" value={values.date_of_birth} onChange={(event) => updateValue("date_of_birth", event.target.value)} required />
          <Input label="Gender" name="gender" value={values.gender} onChange={(event) => updateValue("gender", event.target.value)} required />
          <Input label="Email" name="email" type="email" value={values.email} onChange={(event) => updateValue("email", event.target.value)} required />
          <Input label="Phone" name="phone" value={values.phone} onChange={(event) => updateValue("phone", event.target.value)} required />
          <Input label="Course" name="course" value={values.course} onChange={(event) => updateValue("course", event.target.value)} required />
          <Input label="Department" name="department" value={values.department} onChange={(event) => updateValue("department", event.target.value)} required />
          <Input label="Semester" name="semester" type="number" min="1" value={values.semester} onChange={(event) => updateValue("semester", event.target.value)} required />
          <Input label="Section" name="section" value={values.section || ""} onChange={(event) => updateValue("section", event.target.value)} />
          <Input label="Academic Year" name="academic_year" value={values.academic_year} onChange={(event) => updateValue("academic_year", event.target.value)} required />
          {!id ? <Input label="Admission Date" name="admission_date" type="date" value={values.admission_date} onChange={(event) => updateValue("admission_date", event.target.value)} required /> : null}
          <div className="form-actions">
            <Button type="submit" icon={Save} isLoading={isSubmitting}>Save Student</Button>
          </div>
        </form>
      </Card>
    </>
  );
}
