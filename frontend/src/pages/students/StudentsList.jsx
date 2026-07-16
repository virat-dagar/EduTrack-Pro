import { Download, Plus, Search, Upload } from "lucide-react";
import { useState } from "react";
import { Link } from "react-router-dom";
import { toast } from "react-toastify";
import { Button } from "../../components/common/Button";
import { Input } from "../../components/common/Input";
import { ErrorState } from "../../components/feedback/ErrorState";
import { LoadingState } from "../../components/feedback/LoadingState";
import { PageHeader } from "../../components/layout/PageHeader";
import { DataTable } from "../../components/tables/DataTable";
import { useApi } from "../../hooks/useApi";
import { studentService } from "../../services/studentService";

export default function StudentsList() {
  const students = useApi(() => studentService.list({ page_size: 100 }), []);
  const [isExporting, setIsExporting] = useState(false);

  const handleExport = async () => {
    setIsExporting(true);
    try {
      const blob = await studentService.exportStudents();
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = url;
      link.download = "students.csv";
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
    } catch (error) {
      toast.error(error.message || "Unable to export students.");
    } finally {
      setIsExporting(false);
    }
  };

  if (students.isLoading) return <LoadingState label="Loading students" />;
  if (students.error) return <ErrorState message={students.error.message} />;

  const rows = students.data?.items || [];

  return (
    <>
      <PageHeader
        title="Students"
        description="Manage enrolled student profiles."
        actions={
          <>
            <Link className="btn btn-primary btn-md" to="/students/create">
              <Plus size={18} aria-hidden="true" />
              <span>New Student</span>
            </Link>
            <Link className="btn btn-primary btn-md" to="/students/import">
              <Upload size={18} aria-hidden="true" />
              <span>Import CSV/Excel</span>
            </Link>
            <button
    className="btn btn-primary btn-md export-btn"
    onClick={handleExport}
>
    <Download size={18} />
    <span>Export Students</span>
</button>
          </>
        }
      />
<div className="toolbar">
    <div className="search-box">

        <Input
            label="Search"
            name="student-search"
            placeholder="Name, roll number, department"
        />
    </div>
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
