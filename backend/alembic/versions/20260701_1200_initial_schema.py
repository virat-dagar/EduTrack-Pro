"""Initial EduTrack Pro schema."""

from alembic import op
import sqlalchemy as sa

revision = "20260701_1200"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Create all EduTrack Pro MVP tables."""

    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("full_name", sa.String(length=100), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("role", sa.String(length=20), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )
    op.create_index(op.f("ix_users_id"), "users", ["id"], unique=False)
    op.create_index(op.f("ix_users_email"), "users", ["email"], unique=False)
    op.create_index(op.f("ix_users_role"), "users", ["role"], unique=False)
    op.create_index(op.f("ix_users_is_active"), "users", ["is_active"], unique=False)

    op.create_table(
        "subjects",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("subject_code", sa.String(length=20), nullable=False),
        sa.Column("subject_name", sa.String(length=100), nullable=False),
        sa.Column("course", sa.String(length=100), nullable=False),
        sa.Column("department", sa.String(length=100), nullable=False),
        sa.Column("semester", sa.Integer(), nullable=False),
        sa.Column("credits", sa.Integer(), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("subject_code"),
    )
    op.create_index(op.f("ix_subjects_id"), "subjects", ["id"], unique=False)
    op.create_index(op.f("ix_subjects_subject_code"), "subjects", ["subject_code"], unique=False)
    op.create_index(op.f("ix_subjects_subject_name"), "subjects", ["subject_name"], unique=False)
    op.create_index(op.f("ix_subjects_course"), "subjects", ["course"], unique=False)
    op.create_index(op.f("ix_subjects_department"), "subjects", ["department"], unique=False)
    op.create_index(op.f("ix_subjects_semester"), "subjects", ["semester"], unique=False)
    op.create_index(op.f("ix_subjects_is_active"), "subjects", ["is_active"], unique=False)

    op.create_table(
        "students",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("roll_number", sa.String(length=30), nullable=False),
        sa.Column("enrollment_number", sa.String(length=50), nullable=False),
        sa.Column("first_name", sa.String(length=50), nullable=False),
        sa.Column("last_name", sa.String(length=50), nullable=False),
        sa.Column("date_of_birth", sa.Date(), nullable=False),
        sa.Column("gender", sa.String(length=20), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("phone", sa.String(length=20), nullable=False),
        sa.Column("course", sa.String(length=100), nullable=False),
        sa.Column("department", sa.String(length=100), nullable=False),
        sa.Column("semester", sa.Integer(), nullable=False),
        sa.Column("section", sa.String(length=10), nullable=True),
        sa.Column("academic_year", sa.String(length=20), nullable=False),
        sa.Column("admission_date", sa.Date(), nullable=False),
        sa.Column("profile_photo", sa.String(length=255), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
        sa.UniqueConstraint("enrollment_number"),
        sa.UniqueConstraint("roll_number"),
        sa.UniqueConstraint("user_id"),
    )
    for column in [
        "id",
        "user_id",
        "roll_number",
        "enrollment_number",
        "email",
        "course",
        "department",
        "semester",
        "section",
        "academic_year",
        "is_active",
    ]:
        op.create_index(op.f(f"ix_students_{column}"), "students", [column], unique=False)

    op.create_table(
        "assignments",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("subject_id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=150), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("total_marks", sa.Float(), nullable=False),
        sa.Column("assigned_date", sa.Date(), nullable=False),
        sa.Column("due_date", sa.Date(), nullable=False),
        sa.Column("created_by", sa.Integer(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["created_by"], ["users.id"]),
        sa.ForeignKeyConstraint(["subject_id"], ["subjects.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    for column in ["id", "subject_id", "title", "assigned_date", "due_date", "created_by", "is_active"]:
        op.create_index(op.f(f"ix_assignments_{column}"), "assignments", [column], unique=False)

    op.create_table(
        "attendance",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("student_id", sa.Integer(), nullable=False),
        sa.Column("subject_id", sa.Integer(), nullable=False),
        sa.Column("attendance_date", sa.Date(), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.Column("remarks", sa.Text(), nullable=True),
        sa.Column("marked_by", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["marked_by"], ["users.id"]),
        sa.ForeignKeyConstraint(["student_id"], ["students.id"]),
        sa.ForeignKeyConstraint(["subject_id"], ["subjects.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "student_id",
            "subject_id",
            "attendance_date",
            name="uq_attendance_student_subject_date",
        ),
    )
    for column in ["id", "student_id", "subject_id", "attendance_date", "status", "marked_by"]:
        op.create_index(op.f(f"ix_attendance_{column}"), "attendance", [column], unique=False)

    op.create_table(
        "marks",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("student_id", sa.Integer(), nullable=False),
        sa.Column("subject_id", sa.Integer(), nullable=False),
        sa.Column("assessment_type", sa.String(length=50), nullable=False),
        sa.Column("marks_obtained", sa.Float(), nullable=False),
        sa.Column("maximum_marks", sa.Float(), nullable=False),
        sa.Column("examination_date", sa.Date(), nullable=False),
        sa.Column("remarks", sa.Text(), nullable=True),
        sa.Column("entered_by", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["entered_by"], ["users.id"]),
        sa.ForeignKeyConstraint(["student_id"], ["students.id"]),
        sa.ForeignKeyConstraint(["subject_id"], ["subjects.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "student_id",
            "subject_id",
            "assessment_type",
            "examination_date",
            name="uq_marks_student_subject_assessment_date",
        ),
    )
    for column in ["id", "student_id", "subject_id", "assessment_type", "examination_date", "entered_by"]:
        op.create_index(op.f(f"ix_marks_{column}"), "marks", [column], unique=False)

    op.create_table(
        "submissions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("assignment_id", sa.Integer(), nullable=False),
        sa.Column("student_id", sa.Integer(), nullable=False),
        sa.Column("submission_date", sa.DateTime(timezone=True), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.Column("submission_notes", sa.Text(), nullable=True),
        sa.Column("attachment_path", sa.String(length=255), nullable=True),
        sa.Column("reviewed_by", sa.Integer(), nullable=True),
        sa.Column("reviewed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("feedback", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["assignment_id"], ["assignments.id"]),
        sa.ForeignKeyConstraint(["reviewed_by"], ["users.id"]),
        sa.ForeignKeyConstraint(["student_id"], ["students.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("assignment_id", "student_id", name="uq_submission_assignment_student"),
    )
    for column in ["id", "assignment_id", "student_id", "submission_date", "status", "reviewed_by"]:
        op.create_index(op.f(f"ix_submissions_{column}"), "submissions", [column], unique=False)


def downgrade() -> None:
    """Drop all EduTrack Pro MVP tables."""

    for column in ["id", "assignment_id", "student_id", "submission_date", "status", "reviewed_by"]:
        op.drop_index(op.f(f"ix_submissions_{column}"), table_name="submissions")
    op.drop_table("submissions")

    for column in ["id", "student_id", "subject_id", "assessment_type", "examination_date", "entered_by"]:
        op.drop_index(op.f(f"ix_marks_{column}"), table_name="marks")
    op.drop_table("marks")

    for column in ["id", "student_id", "subject_id", "attendance_date", "status", "marked_by"]:
        op.drop_index(op.f(f"ix_attendance_{column}"), table_name="attendance")
    op.drop_table("attendance")

    for column in ["id", "subject_id", "title", "assigned_date", "due_date", "created_by", "is_active"]:
        op.drop_index(op.f(f"ix_assignments_{column}"), table_name="assignments")
    op.drop_table("assignments")

    for column in [
        "id",
        "user_id",
        "roll_number",
        "enrollment_number",
        "email",
        "course",
        "department",
        "semester",
        "section",
        "academic_year",
        "is_active",
    ]:
        op.drop_index(op.f(f"ix_students_{column}"), table_name="students")
    op.drop_table("students")

    for column in ["id", "subject_code", "subject_name", "course", "department", "semester", "is_active"]:
        op.drop_index(op.f(f"ix_subjects_{column}"), table_name="subjects")
    op.drop_table("subjects")

    for column in ["id", "email", "role", "is_active"]:
        op.drop_index(op.f(f"ix_users_{column}"), table_name="users")
    op.drop_table("users")
