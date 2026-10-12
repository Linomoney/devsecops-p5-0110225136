"""Validasi input untuk TaskTracker."""
from .models import VALID_PRIORITIES, VALID_STATUSES

MAX_TITLE_LENGTH = 100
MAX_DESCRIPTION_LENGTH = 500


class ValidationError(ValueError):
    """Dilempar ketika input pengguna tidak valid."""


def validate_task_payload(payload, partial: bool = False) -> dict:
    """Validasi payload JSON untuk membuat/mengubah tugas.

    Jika ``partial`` True (update), semua field bersifat opsional.
    Mengembalikan dictionary bersih berisi field yang diizinkan saja.
    """
    if not isinstance(payload, dict):
        raise ValidationError("Payload harus berupa objek JSON.")

    clean = {}

    if "title" in payload or not partial:
        title = payload.get("title")
        if not isinstance(title, str) or not title.strip():
            raise ValidationError("Field 'title' wajib diisi.")
        if len(title.strip()) > MAX_TITLE_LENGTH:
            raise ValidationError(
                f"Field 'title' maksimal {MAX_TITLE_LENGTH} karakter."
            )
        clean["title"] = title.strip()

    if "description" in payload:
        description = payload["description"]
        if not isinstance(description, str):
            raise ValidationError("Field 'description' harus berupa teks.")
        if len(description) > MAX_DESCRIPTION_LENGTH:
            raise ValidationError(
                f"Field 'description' maksimal {MAX_DESCRIPTION_LENGTH} karakter."
            )
        clean["description"] = description

    if "status" in payload:
        if payload["status"] not in VALID_STATUSES:
            raise ValidationError(f"Status harus salah satu dari {VALID_STATUSES}.")
        clean["status"] = payload["status"]

    if "priority" in payload:
        if payload["priority"] not in VALID_PRIORITIES:
            raise ValidationError(
                f"Priority harus salah satu dari {VALID_PRIORITIES}."
            )
        clean["priority"] = payload["priority"]

    return clean
