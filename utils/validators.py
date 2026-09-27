"""
utils/validators.py
────────────────────
Validaciones reutilizadas por los controladores.

No dependen de Tkinter ni de la BD.
Solo validan y transforman datos.
"""

from datetime import datetime
import re


def validate_required(value: str) -> bool:
    return bool(value and value.strip())


def validate_numeric(value: str):
    if not value or not value.strip():
        return True, None

    try:
        value = value.strip()

        if '.' in value:
            return True, float(value)

        return True, int(value)

    except ValueError:
        return False, None


def validate_text(value: str) -> bool:

    if not value or not value.strip():
        return True

    pattern = r"^[A-Za-zÁÉÍÓÚáéíóúÑñÜü\s]+$"

    return bool(re.fullmatch(pattern, value.strip()))


def validate_email(value: str) -> bool:

    if not value or not value.strip():
        return True

    pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"

    return bool(re.fullmatch(pattern, value.strip()))


def validate_date(value: str):
    if not value or not value.strip():
        return True, None

    try:
        return True, datetime.strptime(
            value.strip(),
            "%Y-%m-%d"
        )

    except ValueError:
        return False, None