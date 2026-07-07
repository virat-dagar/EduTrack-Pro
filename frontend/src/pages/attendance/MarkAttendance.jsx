import { CheckCheck, RefreshCcw, Save, UsersRound, X } from "lucide-react";
import { useEffect, useState } from "react";
import { toast } from "react-toastify";
import { Button } from "../../components/common/Button";
import { Card } from "../../components/common/Card";
import { Input } from "../../components/common/Input";
import { ErrorState } from "../../components/feedback/ErrorState";
import { LoadingState } from "../../components/feedback/LoadingState";
import { PageHeader } from "../../components/layout/PageHeader";
import { DataTable } from "../../components/tables/DataTable";
import { attendanceService } from "../../services/attendanceService";
import { classroomService } from "../../services/classroomService";
import { subjectService } from "../../services/subjectService";
import { ATTENDANCE_STATUSES } from "../../utils/constants";
import { todayISO } from "../../utils/dateUtils";

export default function MarkAttendance() {
  const [classrooms, setClassrooms] = useState([]);
  const [subjects, setSubjects] = useState([]);
  const [filters, setFilters] = useState({
    classroom_id: "",
    subject_id: "",
    attendance_date: todayISO(),
  });
  const [rows, setRows] = useState([]);
  const [isLoadingOptions, setIsLoadingOptions] = useState(true);
  const [isLoadingSheet, setIsLoadingSheet] = useState(false);
  const [isSaving, setIsSaving] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function loadOptions() {
      setIsLoadingOptions(true);
      try {
        const [classroomResponse, subjectResponse] = await Promise.all([
          classroomService.list({ page_size: 100 }),
          subjectService.list({ page_size: 100 }),
        ]);
        setClassrooms(classroomResponse.data.items || []);
        setSubjects(subjectResponse.data.items || []);
      } catch (apiError) {
        setError(apiError);
      } finally {
        setIsLoadingOptions(false);
      }
    }
    loadOptions();
  }, []);

  const updateFilter = (field, value) => setFilters((current) => ({ ...current, [field]: value }));

  const loadSheet = async (event) => {
    event.preventDefault();
    if (!filters.classroom_id || !filters.subject_id) {
      toast.error("Choose classroom and subject first.");
      return;
    }
    setIsLoadingSheet(true);
    try {
      const response = await attendanceService.sheet(filters.classroom_id, {
        subject_id: Number(filters.subject_id),
        attendance_date: filters.attendance_date,
      });
      setRows(response.data.students || []);
    } catch (apiError) {
      toast.error(apiError.message || "Unable to load attendance sheet.");
    } finally {
      setIsLoadingSheet(false);
    }
  };

  const updateRow = (studentId, status) => {
    setRows((current) =>
      current.map((row) => (row.student_id === studentId ? { ...row, status } : row)),
    );
  };

  const markAll = (status) => {
    setRows((current) => current.map((row) => ({ ...row, status })));
  };

  const invertSelection = () => {
    setRows((current) =>
      current.map((row) => ({
        ...row,
        status: row.status === "Present" ? "Absent" : "Present",
      })),
    );
  };

  const saveAttendance = async () => {
    setIsSaving(true);
    try {
      const response = await attendanceService.bulk({
        classroom_id: Number(filters.classroom_id),
        subject_id: Number(filters.subject_id),
        attendance_date: filters.attendance_date,
        records: rows.map((row) => ({
          student_id: row.student_id,
          status: row.status,
          remarks: row.remarks || null,
        })),
      });
      toast.success(`Saved ${response.data.saved} and updated ${response.data.updated} attendance records.`);
    } catch (apiError) {
      toast.error(apiError.message || "Unable to save attendance.");
    } finally {
      setIsSaving(false);
    }
  };

  if (isLoadingOptions) return <LoadingState label="Loading classrooms" />;
  if (error) return <ErrorState message={error.message} />;

  return (
    <>
      <PageHeader title="Mark Attendance" description="Load a classroom and mark the full attendance sheet in one pass." />
      <Card>
        <form className="form-grid" onSubmit={loadSheet}>
          <label className="field" htmlFor="classroom_id">
            <span className="field-label">Classroom</span>
            <select id="classroom_id" className="input" value={filters.classroom_id} onChange={(event) => updateFilter("classroom_id", event.target.value)} required>
              <option value="">Select classroom</option>
              {classrooms.map((classroom) => (
                <option key={classroom.id} value={classroom.id}>
                  {classroom.classroom_name}
                </option>
              ))}
            </select>
          </label>
          <label className="field" htmlFor="subject_id">
            <span className="field-label">Subject</span>
            <select id="subject_id" className="input" value={filters.subject_id} onChange={(event) => updateFilter("subject_id", event.target.value)} required>
              <option value="">Select subject</option>
              {subjects.map((subject) => (
                <option key={subject.id} value={subject.id}>
                  {subject.subject_code} - {subject.subject_name}
                </option>
              ))}
            </select>
          </label>
          <Input label="Date" name="attendance_date" type="date" value={filters.attendance_date} onChange={(event) => updateFilter("attendance_date", event.target.value)} required />
          <div className="form-actions">
            <Button type="submit" icon={UsersRound} isLoading={isLoadingSheet}>Load Students</Button>
          </div>
        </form>
      </Card>

      {rows.length ? (
        <Card className="mt-4">
          <div className="toolbar">
            <Button variant="secondary" icon={CheckCheck} onClick={() => markAll("Present")}>Mark All Present</Button>
            <Button variant="secondary" icon={X} onClick={() => markAll("Absent")}>Mark All Absent</Button>
            <Button variant="secondary" icon={RefreshCcw} onClick={invertSelection}>Invert Selection</Button>
            <Button icon={Save} isLoading={isSaving} onClick={saveAttendance}>Save Attendance</Button>
          </div>
          <DataTable
            rows={rows}
            getRowId={(row) => row.student_id}
            columns={[
              { key: "roll_number", header: "Roll No." },
              { key: "name", header: "Name" },
              {
                key: "status",
                header: "Attendance",
                render: (row) => (
                  <select className="input input-compact" value={row.status} onChange={(event) => updateRow(row.student_id, event.target.value)}>
                    {ATTENDANCE_STATUSES.map((status) => <option key={status}>{status}</option>)}
                  </select>
                ),
              },
            ]}
          />
        </Card>
      ) : null}
    </>
  );
}
