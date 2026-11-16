"""Import trusted JSON memory backups into SQLite."""
import json
from pathlib import Path

from .store import MemoryStore


def import_json(database_path, input_path):
    """Import validated records without duplicating existing content."""
    source = Path(input_path)
    payload = json.loads(source.read_text(encoding="utf-8"))

    if not isinstance(payload, dict):
        raise ValueError("Invalid JSON backup")
    if payload.get("format") != "ai-memory-hub":
        raise ValueError("Unsupported backup format")
    if payload.get("version") != 1:
        raise ValueError("Unsupported backup version")

    records = payload.get("memories")
    if not isinstance(records, list):
        raise ValueError("Invalid memories list")

    validated = []
    for record in records:
        if not isinstance(record, dict):
            raise ValueError("Invalid memory record")

        project = record.get("project")
        content = record.get("content")
        label = record.get("source", "")
        created_at = record.get("created_at")

        if not isinstance(created_at, str) or not created_at.strip():
            raise ValueError("Invalid creation timestamp")

        if not isinstance(project, str) or not project.strip():
            raise ValueError("Invalid project")
        if not isinstance(content, str) or not content.strip():
            raise ValueError("Invalid content")
        if not isinstance(label, str):
            raise ValueError("Invalid source")

        validated.append((project, content, label, created_at))

    store = MemoryStore(database_path)
    imported = 0

    with store._connect() as db:
        for project, content, label, created_at in validated:
            exists = db.execute(
                "SELECT 1 FROM memories "
                "WHERE project=? AND content=? AND source=? LIMIT 1",
                (project, content, label),
            ).fetchone()

            if not exists:
                db.execute(
                    "INSERT INTO memories(project, content, source, created_at) "
                    "VALUES (?, ?, ?, ?)",
                    (project, content, label, created_at),
                )
                imported += 1

    return imported
