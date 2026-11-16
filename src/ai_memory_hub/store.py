"""SQLite-backed, project-scoped memory with full-text search."""
import sqlite3
from pathlib import Path

class MemoryStore:
    def __init__(self, path: str | Path):
        self.path = str(path)
        with self._connect() as db:
            db.execute('CREATE TABLE IF NOT EXISTS memories (id INTEGER PRIMARY KEY, project TEXT NOT NULL, content TEXT NOT NULL, source TEXT NOT NULL DEFAULT "", created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP)')
            db.execute('CREATE INDEX IF NOT EXISTS idx_memories_project ON memories(project)')

    def _connect(self):
        return sqlite3.connect(self.path)

    def add(self, project: str, content: str, source: str = "") -> int:
        if not project.strip() or not content.strip():
            raise ValueError("Project and content must be nonempty")
        with self._connect() as db:
            cursor = db.execute('INSERT INTO memories(project, content, source) VALUES (?, ?, ?)', (project, content, source))
            return cursor.lastrowid

    def search(self, query: str, project: str | None = None, limit: int = 20) -> list[dict]:
        if not query.strip():
            return []
        if not 1 <= limit <= 100:
            raise ValueError("limit must be between 1 and 100")
        sql = 'SELECT id, project, content, source, created_at FROM memories WHERE instr(lower(content), lower(?)) > 0'
        params = [query]
        if project is not None:
            sql += ' AND project = ?'
            params.append(project)
        sql += ' ORDER BY id DESC LIMIT ?'
        params.append(limit)
        with self._connect() as db:
            db.row_factory = sqlite3.Row
            return [dict(row) for row in db.execute(sql, params)]

    def delete(self, memory_id: int) -> bool:
        with self._connect() as db:
            return db.execute('DELETE FROM memories WHERE id = ?', (memory_id,)).rowcount > 0
