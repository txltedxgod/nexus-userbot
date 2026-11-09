import unittest
from unittest.mock import MagicMock
from nexus.modules.downloader import DownloaderModule

class TestDownloaderModule(unittest.TestCase):
    def setUp(self):
        self.mock_client = MagicMock()
        self.mock_db = MagicMock()
        self.module = DownloaderModule(self.mock_client, self.mock_db)

    def test_commands_registration(self):
        self.assertTrue(hasattr(self.module.cmd_dem, "_cmd_meta"))
        self.assertTrue(hasattr(self.module.cmd_dl, "_cmd_meta"))

if __name__ == "__main__":
    unittest.main()
