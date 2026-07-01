import { Plus } from "lucide-react";
import { Link } from "react-router-dom";
import { ErrorState } from "../../components/feedback/ErrorState";
import { LoadingState } from "../../components/feedback/LoadingState";
import { PageHeader } from "../../components/layout/PageHeader";
import { DataTable } from "../../components/tables/DataTable";
import { Badge } from "../../components/ui/Badge";
import { useAuth } from "../../hooks/useAuth";
import { useApi } from "../../hooks/useApi";
import { attendanceService } from "../../services/attendanceService";
import { ROLES } from "../../utils/constants";
import { formatDate } from "../../utils/dateUtils";

export default function AttendanceList() {
  const { user } = useAuth();
  const attendance = useApi(() => attendanceService.list({ page_size: 100 }), []);
  if (attendance.isLoading) return <LoadingState label="Loading attendance" />;
  if (attendance.error) return <ErrorState message={attendance.error.message} />;

  return (
    <>
      <PageHeader
        title="Attendance"
        description="Daily attendance records and corrections."
        actions={user?.role === ROLES.TEACHER ? <Link className="btn btn-primary btn-md" to="/attendance/mark"><Plus size={18} aria-hidden="true" /><span>Mark Attendance</span></Link> : null}
      />
      <DataTable
        rows={attendance.data?.items || []}
        columns={[
          { key: "attendance_date", header: "Date", render: (row) => formatDate(row.attendance_date) },
          { key: "student_id", header: "Student ID" },
          { key: "subject_id", header: "Subject ID" },
          { key: "status", header: "Status", render: (row) => <Badge tone={row.status === "Present" ? "success" : row.status === "Late" ? "warning" : "danger"}>{row.status}</Badge> },
          { key: "remarks", header: "Remarks" },
        ]}
      />
    </>
  );
}
