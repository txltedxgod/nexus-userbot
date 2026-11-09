import unittest
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, AsyncMock

from nexus.database import Database
from nexus.modules.profile import ProfileModule

class TestProfileModule(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = Path(self.temp_dir.name) / "test_profile.sqlite"
        self.db = Database(self.db_path)
        self.mock_client = MagicMock()
        self.module = ProfileModule(self.mock_client, self.db)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_afk_state_persistence(self):
        self.module.set_config("is_afk", True)
        self.module.set_config("afk_reason", "Coding userbot")
        self.assertTrue(self.module.get_config("is_afk"))
        self.assertEqual(self.module.get_config("afk_reason"), "Coding userbot")

    def test_revert_backup_cleanup(self):
        self.module.set_config("orig_first_name", "Original")
        self.module.set_config("orig_last_name", "User")
        self.assertEqual(self.module.get_config("orig_first_name"), "Original")
        self.module.del_config("orig_first_name")
        self.assertIsNone(self.module.get_config("orig_first_name"))

if __name__ == "__main__":
    unittest.main()
