"""SQLAlchemy declarative base and model registration."""

from sqlalchemy.orm import declarative_base

Base = declarative_base()


def import_models() -> None:
    """Import all model modules so SQLAlchemy metadata is populated."""

    from app.models import assignment  # noqa: F401
    from app.models import attendance  # noqa: F401
    from app.models import marks  # noqa: F401
    from app.models import student  # noqa: F401
    from app.models import subject  # noqa: F401
    from app.models import submission  # noqa: F401
    from app.models import user  # noqa: F401
