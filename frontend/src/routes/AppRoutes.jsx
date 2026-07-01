import { lazy, Suspense } from "react";
import { Navigate, Route, Routes } from "react-router-dom";
import { LoadingState } from "../components/feedback/LoadingState";
import { AuthLayout } from "../layouts/AuthLayout";
import { BlankLayout } from "../layouts/BlankLayout";
import { DashboardLayout } from "../layouts/DashboardLayout";
import { ProtectedRoute } from "./ProtectedRoute";
import { PublicRoute } from "./PublicRoute";
import { ROLES } from "../utils/constants";

const LoginPage = lazy(() => import("../pages/auth/LoginPage"));
const TeacherDashboard = lazy(() => import("../pages/dashboard/TeacherDashboard"));
const StudentDashboard = lazy(() => import("../pages/dashboard/StudentDashboard"));
const StudentsList = lazy(() => import("../pages/students/StudentsList"));
const StudentForm = lazy(() => import("../pages/students/StudentForm"));
const StudentDetail = lazy(() => import("../pages/students/StudentDetail"));
const SubjectsList = lazy(() => import("../pages/subjects/SubjectsList"));
const SubjectForm = lazy(() => import("../pages/subjects/SubjectForm"));
const SubjectDetail = lazy(() => import("../pages/subjects/SubjectDetail"));
const AttendanceList = lazy(() => import("../pages/attendance/AttendanceList"));
const MarkAttendance = lazy(() => import("../pages/attendance/MarkAttendance"));
const AttendanceSummary = lazy(() => import("../pages/attendance/AttendanceSummary"));
const AttendanceHistory = lazy(() => import("../pages/attendance/AttendanceHistory"));
const MarksList = lazy(() => import("../pages/marks/MarksList"));
const MarksForm = lazy(() => import("../pages/marks/MarksForm"));
const PerformancePage = lazy(() => import("../pages/marks/PerformancePage"));
const AssignmentsList = lazy(() => import("../pages/assignments/AssignmentsList"));
const AssignmentForm = lazy(() => import("../pages/assignments/AssignmentForm"));
const AssignmentDetail = lazy(() => import("../pages/assignments/AssignmentDetail"));
const ReportsPage = lazy(() => import("../pages/reports/ReportsPage"));
const ProfilePage = lazy(() => import("../pages/profile/ProfilePage"));
const SettingsPage = lazy(() => import("../pages/settings/SettingsPage"));
const ForbiddenPage = lazy(() => import("../pages/errors/ForbiddenPage"));
const NotFoundPage = lazy(() => import("../pages/errors/NotFoundPage"));

export function AppRoutes() {
  return (
    <Suspense fallback={<LoadingState label="Loading page" />}>
      <Routes>
        <Route path="/" element={<Navigate to="/login" replace />} />
        <Route
          path="/login"
          element={
            <PublicRoute>
              <AuthLayout>
                <LoginPage />
              </AuthLayout>
            </PublicRoute>
          }
        />
        <Route
          element={
            <ProtectedRoute>
              <DashboardLayout />
            </ProtectedRoute>
          }
        >
          <Route path="/dashboard/teacher" element={<ProtectedRoute roles={[ROLES.TEACHER]}><TeacherDashboard /></ProtectedRoute>} />
          <Route path="/dashboard/student" element={<ProtectedRoute roles={[ROLES.STUDENT]}><StudentDashboard /></ProtectedRoute>} />
          <Route path="/students/list" element={<ProtectedRoute roles={[ROLES.TEACHER]}><StudentsList /></ProtectedRoute>} />
          <Route path="/students/create" element={<ProtectedRoute roles={[ROLES.TEACHER]}><StudentForm /></ProtectedRoute>} />
          <Route path="/students/:id" element={<StudentDetail />} />
          <Route path="/students/edit/:id" element={<ProtectedRoute roles={[ROLES.TEACHER]}><StudentForm /></ProtectedRoute>} />
          <Route path="/subjects/list" element={<SubjectsList />} />
          <Route path="/subjects/create" element={<ProtectedRoute roles={[ROLES.TEACHER]}><SubjectForm /></ProtectedRoute>} />
          <Route path="/subjects/:id" element={<SubjectDetail />} />
          <Route path="/subjects/edit/:id" element={<ProtectedRoute roles={[ROLES.TEACHER]}><SubjectForm /></ProtectedRoute>} />
          <Route path="/attendance/list" element={<AttendanceList />} />
          <Route path="/attendance/mark" element={<ProtectedRoute roles={[ROLES.TEACHER]}><MarkAttendance /></ProtectedRoute>} />
          <Route path="/attendance/summary" element={<ProtectedRoute roles={[ROLES.TEACHER]}><AttendanceSummary /></ProtectedRoute>} />
          <Route path="/attendance/history" element={<AttendanceHistory />} />
          <Route path="/marks/list" element={<MarksList />} />
          <Route path="/marks/create" element={<ProtectedRoute roles={[ROLES.TEACHER]}><MarksForm /></ProtectedRoute>} />
          <Route path="/marks/performance" element={<PerformancePage />} />
          <Route path="/marks/edit/:id" element={<ProtectedRoute roles={[ROLES.TEACHER]}><MarksForm /></ProtectedRoute>} />
          <Route path="/assignments/list" element={<AssignmentsList />} />
          <Route path="/assignments/create" element={<ProtectedRoute roles={[ROLES.TEACHER]}><AssignmentForm /></ProtectedRoute>} />
          <Route path="/assignments/:id" element={<AssignmentDetail />} />
          <Route path="/assignments/edit/:id" element={<ProtectedRoute roles={[ROLES.TEACHER]}><AssignmentForm /></ProtectedRoute>} />
          <Route path="/reports/students" element={<ReportsPage type="students" />} />
          <Route path="/reports/attendance" element={<ProtectedRoute roles={[ROLES.TEACHER]}><ReportsPage type="attendance" /></ProtectedRoute>} />
          <Route path="/reports/marks" element={<ProtectedRoute roles={[ROLES.TEACHER]}><ReportsPage type="marks" /></ProtectedRoute>} />
          <Route path="/reports/institution" element={<ProtectedRoute roles={[ROLES.TEACHER]}><ReportsPage type="institution" /></ProtectedRoute>} />
          <Route path="/profile" element={<ProfilePage />} />
          <Route path="/settings" element={<SettingsPage />} />
        </Route>
        <Route path="/forbidden" element={<BlankLayout><ForbiddenPage /></BlankLayout>} />
        <Route path="*" element={<BlankLayout><NotFoundPage /></BlankLayout>} />
      </Routes>
    </Suspense>
  );
}
