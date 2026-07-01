# EduTrack Pro Database

The MVP database uses SQLite with SQLAlchemy ORM and Alembic migrations.

Tables:

- `users`
- `students`
- `subjects`
- `attendance`
- `marks`
- `assignments`
- `submissions`

Important constraints:

- Unique user email.
- One student profile per student user.
- Unique student roll number, enrollment number, and email.
- Unique subject code.
- One attendance record per student, subject, and date.
- One marks record per student, subject, assessment type, and examination date.
- One submission per student and assignment.

Run migrations from `backend/`:

```bash
alembic upgrade head
```
