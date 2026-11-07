import unittest
from unittest.mock import MagicMock
from nexus.modules.text import TextModule, RU_EN, EN_RU

class TestTextModule(unittest.TestCase):
    def setUp(self):
        self.mock_client = MagicMock()
        self.mock_db = MagicMock()
        self.module = TextModule(self.mock_client, self.mock_db)

    def test_transliteration_mapping(self):
        # Russian to English keyboard mapping test
        text_ru = "ghbdtn"  # 'привет' typed in English layout
        result = []
        for c in text_ru:
            result.append(EN_RU.get(c, c))
        self.assertEqual("".join(result), "привет")

    def test_commands_registration(self):
        self.assertTrue(hasattr(self.module.cmd_type, "_cmd_meta"))
        self.assertTrue(hasattr(self.module.cmd_paste, "_cmd_meta"))
        self.assertTrue(hasattr(self.module.cmd_hide, "_cmd_meta"))
        self.assertTrue(hasattr(self.module.cmd_translit, "_cmd_meta"))
        self.assertTrue(hasattr(self.module.cmd_quote, "_cmd_meta"))

if __name__ == "__main__":
    unittest.main()
