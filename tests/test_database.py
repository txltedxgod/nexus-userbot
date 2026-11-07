import unittest
import tempfile
import os
from pathlib import Path
from nexus.database import Database

class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = Path(self.temp_dir.name) / "test_data.sqlite"
        self.db = Database(self.db_path)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_set_and_get(self):
        self.db.set("test_mod", "key1", "hello_world")
        self.assertEqual(self.db.get("test_mod", "key1"), "hello_world")

    def test_json_structures(self):
        data = {"count": 42, "items": ["a", "b", "c"], "enabled": True}
        self.db.set("test_mod", "config", data)
        retrieved = self.db.get("test_mod", "config")
        self.assertEqual(retrieved, data)

    def test_default_fallback(self):
        self.assertEqual(self.db.get("non_existent", "missing", "default_val"), "default_val")

    def test_delete(self):
        self.db.set("test_mod", "to_delete", 123)
        self.assertTrue(self.db.delete("test_mod", "to_delete"))
        self.assertIsNone(self.db.get("test_mod", "to_delete"))
        self.assertFalse(self.db.delete("test_mod", "to_delete"))

    def test_get_all_and_clear(self):
        self.db.set("mod_a", "k1", 1)
        self.db.set("mod_a", "k2", 2)
        all_vals = self.db.get_all("mod_a")
        self.assertEqual(all_vals, {"k1": 1, "k2": 2})

        cleared = self.db.clear("mod_a")
        self.assertEqual(cleared, 2)
        self.assertEqual(self.db.get_all("mod_a"), {})

if __name__ == "__main__":
    unittest.main()
