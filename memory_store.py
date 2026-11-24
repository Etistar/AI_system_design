"""Session memory for research runs. This is the prototype's run log."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

MEMORY_PATH = Path(__file__).resolve().parent / "data" / "session_memory.json"


def remember(record: dict) -> None:
    MEMORY_PATH.parent.mkdir(parents=True, exist_ok=True)
    records = []
    if MEMORY_PATH.exists():
        records = json.loads(MEMORY_PATH.read_text(encoding="utf-8"))
    record = {"saved_at": datetime.now().isoformat(timespec="seconds"), **record}
    records.append(record)
    MEMORY_PATH.write_text(json.dumps(records, indent=2), encoding="utf-8")
