import { CheckCircle2, FileSpreadsheet, Upload } from "lucide-react";
import { useState } from "react";
import { toast } from "react-toastify";
import { Button } from "../../components/common/Button";
import { Card } from "../../components/common/Card";
import { Badge } from "../../components/ui/Badge";
import { DataTable } from "../../components/tables/DataTable";
import { PageHeader } from "../../components/layout/PageHeader";
import { studentService } from "../../services/studentService";

export default function StudentImportPage() {
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [result, setResult] = useState(null);
  const [isPreviewing, setIsPreviewing] = useState(false);
  const [isImporting, setIsImporting] = useState(false);

  const validRows = preview?.rows?.filter((row) => row.is_valid).map((row) => row.data) || [];

  const handlePreview = async (event) => {
    event.preventDefault();
    if (!file) {
      toast.error("Choose a CSV or Excel file first.");
      return;
    }
    setIsPreviewing(true);
    setResult(null);
    try {
      const response = await studentService.previewImport(file);
      setPreview(response.data);
      toast.success("Import preview ready.");
    } catch (error) {
      toast.error(error.message || "Unable to preview import.");
    } finally {
      setIsPreviewing(false);
    }
  };

  const handleCommit = async () => {
    if (!validRows.length) {
      toast.error("There are no valid rows to import.");
      return;
    }
    setIsImporting(true);
    try {
      const response = await studentService.commitImport(validRows);
      setResult(response.data);
      toast.success(`Imported ${response.data.imported} students.`);
    } catch (error) {
      toast.error(error.message || "Unable to import students.");
    } finally {
      setIsImporting(false);
    }
  };

  return (
    <>
      <PageHeader
        title="Import Students"
        description="Upload CSV or Excel rows, preview validation errors, then import valid students with generated logins."
      />
      <Card>
        <form className="form-grid" onSubmit={handlePreview}>
          <label className="field" htmlFor="student-file">
            <span className="field-label">Student File</span>
            <input
              id="student-file"
              className="input"
              type="file"
              accept=".csv,.xls,.xlsx"
              onChange={(event) => setFile(event.target.files?.[0] || null)}
            />
            <span className="field-hint">Required columns: Roll No, First Name, Last Name, Email, Course, Department, Semester, Section.</span>
          </label>
          <div className="form-actions">
            <Button type="submit" icon={FileSpreadsheet} isLoading={isPreviewing}>Preview Import</Button>
          </div>
        </form>
      </Card>

      {preview ? (
        <Card className="mt-4">
          <div className="summary-strip">
            <span>Total rows: {preview.total_rows}</span>
            <span>Valid: {preview.valid_rows}</span>
            <span>Invalid: {preview.invalid_rows}</span>
          </div>
          <DataTable
            rows={preview.rows}
            getRowId={(row) => row.row_number}
            columns={[
              { key: "row_number", header: "Row" },
              { key: "roll", header: "Roll No.", render: (row) => row.data?.roll_number || "-" },
              { key: "name", header: "Name", render: (row) => `${row.data?.first_name || "-"} ${row.data?.last_name || ""}` },
              { key: "email", header: "Email", render: (row) => row.data?.email || "-" },
              { key: "class", header: "Class", render: (row) => `${row.data?.course || "-"} Sem ${row.data?.semester || "-"} ${row.data?.section || ""}` },
              { key: "status", header: "Status", render: (row) => <Badge tone={row.is_valid ? "success" : "danger"}>{row.is_valid ? "Valid" : "Error"}</Badge> },
              { key: "errors", header: "Errors", render: (row) => row.errors?.join(", ") || "-" },
            ]}
          />
          <div className="form-actions">
            <Button icon={Upload} isLoading={isImporting} onClick={handleCommit}>Import Valid Rows</Button>
          </div>
        </Card>
      ) : null}

      {result ? (
        <Card className="mt-4">
          <div className="credential-panel">
            <CheckCircle2 size={24} aria-hidden="true" />
            <div>
              <h2>Import completed</h2>
              <p className="muted">Imported {result.imported} students. Skipped {result.skipped} rows.</p>
            </div>
          </div>
          <DataTable
            rows={result.items || []}
            getRowId={(row) => row.student_id}
            columns={[
              { key: "student_id", header: "Student ID" },
              { key: "roll_number", header: "Roll No." },
              { key: "email", header: "Email" },
              { key: "password", header: "Temporary Password", render: (row) => row.generated_credentials?.password || "-" },
            ]}
          />
        </Card>
      ) : null}
    </>
  );
}
