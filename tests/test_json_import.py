import json
import sqlite3
import tempfile
import unittest
from pathlib import Path

from ai_memory_hub import MemoryStore
from ai_memory_hub.json_export import export_json
from ai_memory_hub.json_import import import_json


class TestJsonImport(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.folder = Path(self.temp.name)
        self.original = self.folder / "original.db"
        self.restored = self.folder / "restored.db"
        self.backup = self.folder / "backup.json"
        self.store = MemoryStore(self.original)

    def tearDown(self):
        self.temp.cleanup()

    def test_restore_and_no_duplicates(self):
        self.store.add("demo", "تصمیم آزمایشی", "manual")
        export_json(self.original, self.backup)

        self.assertEqual(import_json(self.restored, self.backup), 1)
        self.assertEqual(import_json(self.restored, self.backup), 0)

        restored = MemoryStore(self.restored)
        self.assertEqual(
            len(restored.search("تصمیم", project="demo")), 1
        )

    def test_preserve_timestamp(self):
        memory_id = self.store.add("demo", "Historical", "test")
        with sqlite3.connect(self.original) as db:
            db.execute(
                "UPDATE memories SET created_at=? WHERE id=?",
                ("2024-01-15 10:30:00", memory_id),
            )

        export_json(self.original, self.backup)
        import_json(self.restored, self.backup)

        with sqlite3.connect(self.restored) as db:
            timestamp = db.execute(
                "SELECT created_at FROM memories"
            ).fetchone()[0]

        self.assertEqual(timestamp, "2024-01-15 10:30:00")

    def test_reject_invalid_backup(self):
        self.backup.write_text(
            json.dumps({
                "format": "ai-memory-hub",
                "version": 1,
                "memories": [{"project": "", "content": "test"}],
            }),
            encoding="utf-8",
        )

        with self.assertRaises(ValueError):
            import_json(self.restored, self.backup)


if __name__ == "__main__":
    unittest.main()


class TestDuplicateRecordPreservation(unittest.TestCase):
    def test_distinct_identical_memories_are_preserved(self):
        with tempfile.TemporaryDirectory() as folder:
            folder = Path(folder)
            original = folder / "original.db"
            restored = folder / "restored.db"
            backup = folder / "backup.json"

            store = MemoryStore(original)
            store.add("demo", "Same decision", "manual")
            store.add("demo", "Same decision", "manual")

            export_json(original, backup)

            self.assertEqual(import_json(restored, backup), 2)
            self.assertEqual(import_json(restored, backup), 0)
            self.assertEqual(
                len(MemoryStore(restored).search("Same decision")),
                2,
            )


class TestDuplicateRecordPreservation(unittest.TestCase):
    def test_distinct_identical_memories_are_preserved(self):
        with tempfile.TemporaryDirectory() as folder:
            folder = Path(folder)
            original = folder / "original.db"
            restored = folder / "restored.db"
            backup = folder / "backup.json"

            store = MemoryStore(original)
            store.add("demo", "Same decision", "manual")
            store.add("demo", "Same decision", "manual")

            export_json(original, backup)

            self.assertEqual(import_json(restored, backup), 2)
            self.assertEqual(import_json(restored, backup), 0)
            self.assertEqual(
                len(MemoryStore(restored).search("Same decision")),
                2,
            )


class TestImportIdConflict(unittest.TestCase):
    def test_conflicting_id_raises_error(self):
        with tempfile.TemporaryDirectory() as folder:
            folder = Path(folder)
            source = folder / "source.db"
            target = folder / "target.db"
            backup = folder / "backup.json"

            MemoryStore(source).add("source", "Backup memory")
            MemoryStore(target).add("target", "Existing memory")

            export_json(source, backup)

            with self.assertRaises(ValueError):
                import_json(target, backup)

            self.assertEqual(
                len(MemoryStore(target).search("Existing memory")),
                1,
            )
