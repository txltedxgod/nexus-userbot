import unittest
import tempfile
from pathlib import Path
from unittest.mock import MagicMock

from nexus.database import Database
from nexus.modules.admin import AdminModule

class TestAdminModule(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = Path(self.temp_dir.name) / "test_admin.sqlite"
        self.db = Database(self.db_path)
        self.mock_client = MagicMock()
        self.module = AdminModule(self.mock_client, self.db)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_commands_registration(self):
        # Verify all methods have command metadata
        self.assertTrue(hasattr(self.module.cmd_purge, "_cmd_meta"))
        self.assertTrue(hasattr(self.module.cmd_del, "_cmd_meta"))
        self.assertTrue(hasattr(self.module.cmd_pin, "_cmd_meta"))
        self.assertTrue(hasattr(self.module.cmd_user, "_cmd_meta"))
        self.assertTrue(hasattr(self.module.cmd_id, "_cmd_meta"))

if __name__ == "__main__":
    unittest.main()
