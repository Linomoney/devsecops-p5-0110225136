"""Model data untuk TaskTracker."""
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone

VALID_STATUSES = ("todo", "in_progress", "done")
VALID_PRIORITIES = ("low", "medium", "high")


@dataclass
class Task:
    """Representasi satu tugas."""

    task_id: int
    code: str
    title: str
    description: str = ""
    status: str = "todo"
    priority: str = "medium"
    created_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    def to_dict(self) -> dict:
        """Ubah objek Task menjadi dictionary (siap di-JSON-kan)."""
        return asdict(self)

    def is_finished(self) -> bool:
        """Kembalikan True jika tugas sudah selesai."""
        return self.status == "done"
