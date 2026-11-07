import unittest
from unittest.mock import MagicMock
from nexus.modules.leads import LeadsModule, BLACK_LIST

class TestLeadsModule(unittest.TestCase):
    def setUp(self):
        self.mock_client = MagicMock()
        self.mock_db = MagicMock()
        self.module = LeadsModule(self.mock_client, self.mock_db)

    def test_blacklist_integrity(self):
        self.assertIn("казино", BLACK_LIST)
        self.assertIn("1win", BLACK_LIST)
        self.assertIn("дроп", BLACK_LIST)

    def test_commands_registration(self):
        self.assertTrue(hasattr(self.module.cmd_scanleads, "_cmd_meta"))
        self.assertTrue(hasattr(self.module.cmd_addkeyword, "_cmd_meta"))
        self.assertTrue(hasattr(self.module.cmd_delkeyword, "_cmd_meta"))
        self.assertTrue(hasattr(self.module.cmd_keywords, "_cmd_meta"))
        self.assertTrue(hasattr(self.module.cmd_setalert, "_cmd_meta"))
        self.assertTrue(hasattr(self.module.lead_watcher, "_watcher_meta"))

if __name__ == "__main__":
    unittest.main()
