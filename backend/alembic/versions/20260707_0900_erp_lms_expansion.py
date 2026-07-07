"""ERP/LMS classroom, import, attendance, and grading expansion."""

from alembic import op
import sqlalchemy as sa

revision = "20260707_0900"
down_revision = "20260701_1200"
branch_labels = None
depends_on = None


def _table_exists(table_name: str) -> bool:
    """Return whether a table exists."""

    return table_name in set(sa.inspect(op.get_bind()).get_table_names())


def _column_exists(table_name: str, column_name: str) -> bool:
    """Return whether a column exists."""

    if not _table_exists(table_name):
        return False
    return column_name in {column["name"] for column in sa.inspect(op.get_bind()).get_columns(table_name)}


def _index_exists(table_name: str, index_name: str) -> bool:
    """Return whether an index exists."""

    if not _table_exists(table_name):
        return False
    return index_name in {index["name"] for index in sa.inspect(op.get_bind()).get_indexes(table_name)}


def _create_index_if_missing(table_name: str, column_name: str) -> None:
    """Create a conventional Alembic index when it does not exist."""

    index_name = op.f(f"ix_{table_name}_{column_name}")
    if not _index_exists(table_name, index_name):
        op.create_index(index_name, table_name, [column_name], unique=False)


def _add_column_if_missing(table_name: str, column: sa.Column) -> None:
    """Add a column when it does not exist."""

    if not _column_exists(table_name, column.name):
        with op.batch_alter_table(table_name) as batch_op:
            batch_op.add_column(column)
    _create_index_if_missing(table_name, column.name)


def upgrade() -> None:
    """Add classroom-centered ERP/LMS tables and columns."""

    if not _table_exists("classrooms"):
        op.create_table(
            "classrooms",
            sa.Column("id", sa.Integer(), nullable=False),
            sa.Column("classroom_code", sa.String(length=80), nullable=False),
            sa.Column("classroom_name", sa.String(length=150), nullable=False),
            sa.Column("department", sa.String(length=100), nullable=False),
            sa.Column("course", sa.String(length=100), nullable=False),
            sa.Column("semester", sa.Integer(), nullable=False),
            sa.Column("section", sa.String(length=10), nullable=False),
            sa.Column("academic_year", sa.String(length=20), nullable=False),
            sa.Column("is_active", sa.Boolean(), nullable=False),
            sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
            sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
            sa.PrimaryKeyConstraint("id"),
            sa.UniqueConstraint("classroom_code"),
            sa.UniqueConstraint(
                "department",
                "course",
                "semester",
                "section",
                "academic_year",
                name="uq_classroom_academic_group",
            ),
        )
    for column in [
        "id",
        "classroom_code",
        "department",
        "course",
        "semester",
        "section",
        "academic_year",
        "is_active",
    ]:
        _create_index_if_missing("classrooms", column)

    _add_column_if_missing("students", sa.Column("classroom_id", sa.Integer(), nullable=True))
    _add_column_if_missing("subjects", sa.Column("classroom_id", sa.Integer(), nullable=True))
    _add_column_if_missing("attendance", sa.Column("classroom_id", sa.Integer(), nullable=True))
    _add_column_if_missing("marks", sa.Column("classroom_id", sa.Integer(), nullable=True))

    assignment_columns = [
        sa.Column("classroom_id", sa.Integer(), nullable=True),
        sa.Column("pdf_file", sa.String(length=255), nullable=True),
        sa.Column("is_published", sa.Boolean(), server_default=sa.true(), nullable=False),
        sa.Column("published_at", sa.DateTime(timezone=True), nullable=True),
    ]
    for column in assignment_columns:
        _add_column_if_missing("assignments", column)

    submission_columns = [
        sa.Column("submitted_file", sa.String(length=255), nullable=True),
        sa.Column("total_marks", sa.Float(), nullable=True),
        sa.Column("percentage", sa.Float(), nullable=True),
        sa.Column("grade", sa.String(length=5), nullable=True),
    ]
    for column in submission_columns:
        _add_column_if_missing("submissions", column)

    if not _table_exists("assignment_questions"):
        op.create_table(
            "assignment_questions",
            sa.Column("id", sa.Integer(), nullable=False),
            sa.Column("assignment_id", sa.Integer(), nullable=False),
            sa.Column("question_no", sa.Integer(), nullable=False),
            sa.Column("title", sa.String(length=150), nullable=True),
            sa.Column("description", sa.Text(), nullable=True),
            sa.Column("max_marks", sa.Float(), nullable=False),
            sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
            sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
            sa.ForeignKeyConstraint(["assignment_id"], ["assignments.id"]),
            sa.PrimaryKeyConstraint("id"),
            sa.UniqueConstraint("assignment_id", "question_no", name="uq_assignment_question_no"),
        )
    for column in ["id", "assignment_id", "question_no"]:
        _create_index_if_missing("assignment_questions", column)

    if not _table_exists("submission_grades"):
        op.create_table(
            "submission_grades",
            sa.Column("id", sa.Integer(), nullable=False),
            sa.Column("submission_id", sa.Integer(), nullable=False),
            sa.Column("question_id", sa.Integer(), nullable=False),
            sa.Column("obtained_marks", sa.Float(), nullable=False),
            sa.Column("feedback", sa.Text(), nullable=True),
            sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
            sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
            sa.ForeignKeyConstraint(["question_id"], ["assignment_questions.id"]),
            sa.ForeignKeyConstraint(["submission_id"], ["submissions.id"]),
            sa.PrimaryKeyConstraint("id"),
            sa.UniqueConstraint("submission_id", "question_id", name="uq_submission_grade_question"),
        )
    for column in ["id", "submission_id", "question_id"]:
        _create_index_if_missing("submission_grades", column)


def downgrade() -> None:
    """Remove ERP/LMS expansion tables and columns."""

    if _table_exists("submission_grades"):
        op.drop_table("submission_grades")
    if _table_exists("assignment_questions"):
        op.drop_table("assignment_questions")

    for table_name, columns in {
        "submissions": ["grade", "percentage", "total_marks", "submitted_file"],
        "assignments": ["published_at", "is_published", "pdf_file", "classroom_id"],
        "marks": ["classroom_id"],
        "attendance": ["classroom_id"],
        "subjects": ["classroom_id"],
        "students": ["classroom_id"],
    }.items():
        if not _table_exists(table_name):
            continue
        with op.batch_alter_table(table_name) as batch_op:
            for column_name in columns:
                if _column_exists(table_name, column_name):
                    batch_op.drop_column(column_name)

    if _table_exists("classrooms"):
        op.drop_table("classrooms")
