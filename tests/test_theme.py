import unittest
from unittest.mock import MagicMock
from nexus.modules.theme import ThemeModule, EXTRA_THEMES

class TestThemeModule(unittest.TestCase):
    def setUp(self):
        self.mock_client = MagicMock()
        self.mock_db = MagicMock()
        self.mock_db.get.return_value = {}
        self.module = ThemeModule(self.mock_client, self.mock_db)

    def test_theme_presets(self):
        self.assertIn("dracula_dark", EXTRA_THEMES)
        self.assertIn("emerald_matrix", EXTRA_THEMES)
        self.assertIn("minimal_clean", EXTRA_THEMES)

    def test_commands_registration(self):
        self.assertTrue(hasattr(self.module.cmd_settheme, "_cmd_meta"))
        self.assertTrue(hasattr(self.module.cmd_setemoji, "_cmd_meta"))
        self.assertTrue(hasattr(self.module.cmd_emojipack, "_cmd_meta"))
        self.assertTrue(hasattr(self.module.cmd_carddemo, "_cmd_meta"))

if __name__ == "__main__":
    unittest.main()
