import { Plus, Search } from "lucide-react";
import { Link } from "react-router-dom";
import { Input } from "../../components/common/Input";
import { ErrorState } from "../../components/feedback/ErrorState";
import { LoadingState } from "../../components/feedback/LoadingState";
import { PageHeader } from "../../components/layout/PageHeader";
import { DataTable } from "../../components/tables/DataTable";
import { useApi } from "../../hooks/useApi";
import { studentService } from "../../services/studentService";

export default function StudentsList() {
  const students = useApi(() => studentService.list({ page_size: 100 }), []);

  if (students.isLoading) return <LoadingState label="Loading students" />;
  if (students.error) return <ErrorState message={students.error.message} />;

  const rows = students.data?.items || [];

  return (
    <>
      <PageHeader
        title="Students"
        description="Manage enrolled student profiles."
        actions={
          <Link className="btn btn-primary btn-md" to="/students/create">
            <Plus size={18} aria-hidden="true" />
            <span>New Student</span>
          </Link>
        }
      />
      <div className="toolbar">
        <Input label="Search" name="student-search" placeholder="Name, roll number, department" />
        <Search size={20} aria-hidden="true" />
      </div>
      <DataTable
        rows={rows}
        columns={[
          { key: "roll_number", header: "Roll No." },
          { key: "first_name", header: "Name", render: (row) => `${row.first_name} ${row.last_name}` },
          { key: "department", header: "Department" },
          { key: "course", header: "Course" },
          { key: "semester", header: "Semester" },
          { key: "actions", header: "Actions", render: (row) => <Link to={`/students/${row.id}`}>View</Link> },
        ]}
      />
    </>
  );
}
