import unittest
from unittest.mock import MagicMock
from nexus.modules.terminal import TerminalModule

class TestTerminalModule(unittest.TestCase):
    def setUp(self):
        self.mock_client = MagicMock()
        self.mock_db = MagicMock()
        self.module = TerminalModule(self.mock_client, self.mock_db)

    def test_commands_registration(self):
        self.assertTrue(hasattr(self.module.cmd_eval, "_cmd_meta"))
        self.assertTrue(hasattr(self.module.cmd_exec, "_cmd_meta"))
        self.assertTrue(hasattr(self.module.cmd_sh, "_cmd_meta"))
        self.assertTrue(hasattr(self.module.cmd_sys, "_cmd_meta"))

if __name__ == "__main__":
    unittest.main()
