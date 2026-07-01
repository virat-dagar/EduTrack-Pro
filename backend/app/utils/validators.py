"""Reusable validation helpers."""

from datetime import date
import re


def normalize_email(email: str) -> str:
    """Normalize an email address for storage and comparison."""

    return email.strip().lower()


def normalize_text(value: str) -> str:
    """Trim surrounding whitespace."""

    return value.strip()


def ensure_not_future(value: date, field_name: str) -> None:
    """Raise ValueError when a date is in the future."""

    if value > date.today():
        raise ValueError(f"{field_name} cannot be in the future.")


def validate_phone(value: str) -> str:
    """Validate a simple digit-only phone number."""

    cleaned = value.strip()
    if not re.fullmatch(r"\d{7,15}", cleaned):
        raise ValueError("Phone number must contain 7 to 15 digits.")
    return cleaned
