import { Save } from "lucide-react";
import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { toast } from "react-toastify";
import { Button } from "../../components/common/Button";
import { Card } from "../../components/common/Card";
import { Input } from "../../components/common/Input";
import { PageHeader } from "../../components/layout/PageHeader";
import { subjectService } from "../../services/subjectService";

const initialValues = {
  subject_code: "",
  subject_name: "",
  course: "B.Tech",
  department: "Computer Science",
  semester: 1,
  credits: 4,
  description: "",
  is_active: true,
};

export default function SubjectForm() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [values, setValues] = useState(initialValues);
  const [isSubmitting, setIsSubmitting] = useState(false);

  useEffect(() => {
    if (!id) return;
    subjectService.get(id).then((response) => setValues({ ...initialValues, ...response.data }));
  }, [id]);

  const updateValue = (field, value) => setValues((current) => ({ ...current, [field]: value }));

  const handleSubmit = async (event) => {
    event.preventDefault();
    setIsSubmitting(true);
    try {
      const payload = { ...values, semester: Number(values.semester), credits: Number(values.credits) };
      if (id) await subjectService.update(id, payload);
      else await subjectService.create(payload);
      toast.success(id ? "Subject updated successfully." : "Subject created successfully.");
      navigate("/subjects/list");
    } catch (error) {
      toast.error(error.message || "Unable to save subject.");
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <>
      <PageHeader title={id ? "Edit Subject" : "Create Subject"} description="Maintain semester and course mapping." />
      <Card>
        <form className="form-grid" onSubmit={handleSubmit}>
          {!id ? <Input label="Subject Code" name="subject_code" value={values.subject_code} onChange={(event) => updateValue("subject_code", event.target.value)} required /> : null}
          <Input label="Subject Name" name="subject_name" value={values.subject_name} onChange={(event) => updateValue("subject_name", event.target.value)} required />
          <Input label="Course" name="course" value={values.course} onChange={(event) => updateValue("course", event.target.value)} required />
          <Input label="Department" name="department" value={values.department} onChange={(event) => updateValue("department", event.target.value)} required />
          <Input label="Semester" name="semester" type="number" min="1" value={values.semester} onChange={(event) => updateValue("semester", event.target.value)} required />
          <Input label="Credits" name="credits" type="number" min="1" value={values.credits} onChange={(event) => updateValue("credits", event.target.value)} required />
          <Input label="Description" name="description" value={values.description || ""} onChange={(event) => updateValue("description", event.target.value)} />
          <div className="form-actions">
            <Button type="submit" icon={Save} isLoading={isSubmitting}>Save Subject</Button>
          </div>
        </form>
      </Card>
    </>
  );
}
