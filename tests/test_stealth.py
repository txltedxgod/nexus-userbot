import unittest
from unittest.mock import MagicMock, AsyncMock
from nexus.modules.stealth import StealthModule

class TestStealthModule(unittest.TestCase):
    def setUp(self):
        self.mock_client = MagicMock()
        self.mock_db = MagicMock()
        self.mock_db.get.return_value = []
        self.module = StealthModule(self.mock_client, self.mock_db)

    def test_commands_registration(self):
        self.assertTrue(hasattr(self.module.cmd_dmmute, "_cmd_meta"))
        self.assertTrue(hasattr(self.module.cmd_undmmute, "_cmd_meta"))
        self.assertTrue(hasattr(self.module.cmd_dmmuted, "_cmd_meta"))
        self.assertTrue(hasattr(self.module.cmd_antidel, "_cmd_meta"))
        self.assertTrue(hasattr(self.module.dm_mute_and_cache_watcher, "_watcher_meta"))

    def test_message_cache_limit(self):
        # Fill cache with 1005 items
        for i in range(1005):
            self.module.message_cache[i] = {"text": f"msg {i}"}
            if len(self.module.message_cache) > 1000:
                oldest = next(iter(self.module.message_cache))
                del self.module.message_cache[oldest]
        
        self.assertEqual(len(self.module.message_cache), 1000)
        self.assertNotIn(0, self.module.message_cache)
        self.assertIn(1004, self.module.message_cache)

if __name__ == "__main__":
    unittest.main()
