import { Building2, Plus } from "lucide-react";
import { useState } from "react";
import { toast } from "react-toastify";
import { Button } from "../../components/common/Button";
import { Card } from "../../components/common/Card";
import { Input } from "../../components/common/Input";
import { ErrorState } from "../../components/feedback/ErrorState";
import { LoadingState } from "../../components/feedback/LoadingState";
import { PageHeader } from "../../components/layout/PageHeader";
import { DataTable } from "../../components/tables/DataTable";
import { useApi } from "../../hooks/useApi";
import { classroomService } from "../../services/classroomService";
  
const initialValues = {
  department: "Computer Science",
  course: "B.Tech",
  semester: 5,
  section: "A",
  academic_year: "2026-27",
};

export default function ClassroomsList() {
  const classrooms = useApi(() => classroomService.list({ page_size: 100 }), []);
  const [values, setValues] = useState(initialValues);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const updateValue = (field, value) => setValues((current) => ({ ...current, [field]: value }));

  const handleSubmit = async (event) => {
    event.preventDefault();
    setIsSubmitting(true);
    try {
      await classroomService.create({ ...values, semester: Number(values.semester) });
      toast.success("Classroom created successfully.");
      setValues(initialValues);
      classrooms.refetch();
    } catch (error) {
      toast.error(error.message || "Unable to create classroom.");
    } finally {
      setIsSubmitting(false);
    }
  };

  if (classrooms.isLoading) return <LoadingState label="Loading classrooms" />;
  if (classrooms.error) return <ErrorState message={classrooms.error.message} />;

  return (
    <>
      <PageHeader title="Classrooms" description="Organize students by department, course, semester, and section." />
      <Card className="mb-4">
        <form className="form-grid" onSubmit={handleSubmit}>
          <Input label="Department" name="department" value={values.department} onChange={(event) => updateValue("department", event.target.value)} required />
          <Input label="Course" name="course" value={values.course} onChange={(event) => updateValue("course", event.target.value)} required />
          <Input label="Semester" name="semester" type="number" min="1" value={values.semester} onChange={(event) => updateValue("semester", event.target.value)} required />
          <Input label="Section" name="section" value={values.section} onChange={(event) => updateValue("section", event.target.value)} required />
          <Input label="Academic Year" name="academic_year" value={values.academic_year} onChange={(event) => updateValue("academic_year", event.target.value)} required />
          <div className="form-actions">
            <Button type="submit" icon={Plus} isLoading={isSubmitting}>Create Classroom</Button>
          </div>
        </form>
      </Card>
      <DataTable
        rows={classrooms.data?.items || []}
        columns={[
          { key: "id", header: "ID" },
          { key: "classroom_name", header: "Classroom", render: (row) => <span><Building2 size={16} aria-hidden="true" /> {row.classroom_name}</span> },
          { key: "department", header: "Department" },
          { key: "course", header: "Course" },
          { key: "semester", header: "Semester" },
          { key: "section", header: "Section" },
          { key: "student_count", header: "Students" },
        ]}
      />
    </>
  );
}
