import unittest
from unittest.mock import MagicMock
from nexus.modules.reactions import ReactionsModule

class TestReactionsModule(unittest.TestCase):
    def setUp(self):
        self.mock_client = MagicMock()
        self.mock_db = MagicMock()
        self.mock_db.get.return_value = {}
        self.module = ReactionsModule(self.mock_client, self.mock_db)

    def test_commands_registration(self):
        self.assertTrue(hasattr(self.module.cmd_autoreact, "_cmd_meta"))
        self.assertTrue(hasattr(self.module.cmd_delreact, "_cmd_meta"))
        self.assertTrue(hasattr(self.module.cmd_reacts, "_cmd_meta"))
        self.assertTrue(hasattr(self.module.cmd_flex, "_cmd_meta"))
        self.assertTrue(hasattr(self.module.auto_reaction_watcher, "_watcher_meta"))

if __name__ == "__main__":
    unittest.main()
