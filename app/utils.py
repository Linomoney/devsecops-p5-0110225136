"""Fungsi bantu (helper) untuk TaskTracker."""
import random
import string


def generate_task_code(length: int = 6) -> str:
    """Buat kode tugas acak berupa huruf kapital dan angka, contoh: 'TK-A7X2PQ'.

    Kode ini hanya label tampilan, bukan token keamanan.
    """
    alphabet = string.ascii_uppercase + string.digits
    suffix = "".join(random.choice(alphabet) for _ in range(length))
    return f"TK-{suffix}"


def summarize(tasks: list) -> dict:
    """Hitung ringkasan jumlah tugas per status."""
    summary = {"total": len(tasks), "todo": 0, "in_progress": 0, "done": 0}
    for task in tasks:
        summary[task.status] += 1
    return summary
