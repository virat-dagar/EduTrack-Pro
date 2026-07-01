# EduTrack Pro API

Base URL:

```text
http://localhost:8000/api/v1
```

All successful responses use:

```json
{
  "success": true,
  "message": "",
  "data": {}
}
```

All protected endpoints require:

```text
Authorization: Bearer <JWT>
```

## Authentication

- `POST /auth/login`
- `GET /auth/me`

## Academic APIs

- Users: `/users`
- Students: `/students`
- Subjects: `/subjects`
- Attendance: `/attendance`
- Marks: `/marks`
- Assignments: `/assignments`
- Submissions: `/submissions`
- Dashboards: `/dashboard/teacher`, `/dashboard/student`
- Reports: `/reports/student/{student_id}`, `/reports/institution`

Teachers can manage institutional records. Students can view their own academic records and submit assignments.
