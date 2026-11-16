import tempfile
import unittest
from pathlib import Path
from ai_memory_hub import MemoryStore

class TestMemoryStore(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.store = MemoryStore(Path(self.temp.name) / 'test.db')

    def tearDown(self):
        self.temp.cleanup()

    def test_project_isolation(self):
        self.store.add('alpha', 'release checklist')
        self.store.add('beta', 'release planning')
        self.assertEqual(len(self.store.search('release', project='alpha')), 1)
        self.assertEqual(len(self.store.search('release')), 2)

    def test_delete(self):
        item = self.store.add('alpha', 'important decision')
        self.assertTrue(self.store.delete(item))
        self.assertFalse(self.store.delete(item))
        self.assertEqual(self.store.search('decision'), [])

    def test_validation(self):
        with self.assertRaises(ValueError):
            self.store.add('', 'something')
        with self.assertRaises(ValueError):
            self.store.search('x', limit=0)

if __name__ == '__main__':
    unittest.main()
