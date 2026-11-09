import unittest
from unittest.mock import MagicMock
from nexus.modules.media import MediaModule

class TestMediaModule(unittest.TestCase):
    def setUp(self):
        self.mock_client = MagicMock()
        self.mock_db = MagicMock()
        self.module = MediaModule(self.mock_client, self.mock_db)

    def test_commands_registration(self):
        self.assertTrue(hasattr(self.module.cmd_circle, "_cmd_meta"))
        self.assertTrue(hasattr(self.module.cmd_voice, "_cmd_meta"))
        self.assertTrue(hasattr(self.module.cmd_mediainfo, "_cmd_meta"))

if __name__ == "__main__":
    unittest.main()
