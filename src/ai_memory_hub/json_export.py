"""Export local project memories to JSON."""
import json
import sqlite3
from pathlib import Path


def export_json(database_path, output_path, project=None):
    """Export memories from SQLite to a JSON file."""
    with sqlite3.connect(database_path) as db:
        db.row_factory = sqlite3.Row
        sql = (
            "SELECT id, project, content, source, created_at "
            "FROM memories"
        )
        params = []
        if project is not None:
            sql += " WHERE project = ?"
            params.append(project)
        sql += " ORDER BY id"
        records = [
            dict(row) for row in db.execute(sql, params)
        ]

    payload = {
        "format": "ai-memory-hub",
        "version": 1,
        "memories": records,
    }
    output = Path(output_path)
    if output.exists():
        raise FileExistsError(output)
    with output.open("x", encoding="utf-8") as file:
        json.dump(payload, file, ensure_ascii=False, indent=2)

    return len(records)
