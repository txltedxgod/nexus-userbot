import unittest
from nexus.ui import LuxuryUI

class TestLuxuryUI(unittest.TestCase):
    def setUp(self):
        self.ui = LuxuryUI(theme="neon_cyber")

    def test_header(self):
        rendered = self.ui.header("Test Title", subtitle="sub", icon="sparkles")
        self.assertIn("TEST TITLE", rendered)
        self.assertIn("`sub`", rendered)
        self.assertIn("✨", rendered)

    def test_card(self):
        rendered = self.ui.card(
            title="Card Title",
            fields={"Field1": "Val1", "Field2": 100},
            footer="Footer note"
        )
        self.assertIn("CARD TITLE", rendered)
        self.assertIn("**Field1:** `Val1`", rendered)
        self.assertIn("**Field2:** `100`", rendered)
        self.assertIn("_Footer note_", rendered)

    def test_theme_switch(self):
        self.assertTrue(self.ui.set_theme("luxury_gold"))
        self.assertEqual(self.ui.theme_name, "luxury_gold")
        self.assertFalse(self.ui.set_theme("invalid_theme"))

    def test_status_helpers(self):
        succ = self.ui.success("Operation completed")
        self.assertIn("SUCCESS", succ)
        self.assertIn("✅", succ)

        err = self.ui.error("Something went wrong")
        self.assertIn("ERROR", err)
        self.assertIn("❌", err)

if __name__ == "__main__":
    unittest.main()
