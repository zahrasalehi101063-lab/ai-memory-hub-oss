import json
import tempfile
import unittest
from pathlib import Path

from ai_memory_hub import MemoryStore
from ai_memory_hub.json_export import export_json


class TestJsonExport(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.folder = Path(self.temp.name)
        self.db = self.folder / "test.db"
        self.store = MemoryStore(self.db)

    def tearDown(self):
        self.temp.cleanup()

    def test_persian_export(self):
        self.store.add("demo", "تصمیم آزمایشی", "test")
        output = self.folder / "export.json"

        count = export_json(self.db, output, project="demo")
        data = json.loads(output.read_text(encoding="utf-8"))

        self.assertEqual(count, 1)
        self.assertEqual(data["version"], 1)
        self.assertEqual(
            data["memories"][0]["content"],
            "تصمیم آزمایشی"
        )

    def test_project_filter(self):
        self.store.add("alpha", "first")
        self.store.add("beta", "second")
        output = self.folder / "filtered.json"

        count = export_json(self.db, output, project="alpha")
        data = json.loads(output.read_text(encoding="utf-8"))

        self.assertEqual(count, 1)
        self.assertEqual(data["memories"][0]["project"], "alpha")

    def test_no_overwrite(self):
        output = self.folder / "existing.json"
        output.write_text("original", encoding="utf-8")

        with self.assertRaises(FileExistsError):
            export_json(self.db, output)

        self.assertEqual(
            output.read_text(encoding="utf-8"),
            "original"
        )


if __name__ == "__main__":
    unittest.main()
