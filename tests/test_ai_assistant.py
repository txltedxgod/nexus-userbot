import unittest
from unittest.mock import MagicMock
from nexus.modules.ai_assistant import AIAssistantModule

class TestAIAssistantModule(unittest.TestCase):
    def setUp(self):
        self.mock_client = MagicMock()
        self.mock_db = MagicMock()
        self.module = AIAssistantModule(self.mock_client, self.mock_db)

    def test_commands_registration(self):
        self.assertTrue(hasattr(self.module.cmd_ai, "_cmd_meta"))
        self.assertTrue(hasattr(self.module.cmd_summary, "_cmd_meta"))
        self.assertTrue(hasattr(self.module.cmd_pitch_ai, "_cmd_meta"))

if __name__ == "__main__":
    unittest.main()
