import unittest
from nexus.utils import parse_args, format_duration, format_bytes, progress_bar

class TestUtils(unittest.TestCase):
    def test_parse_args(self):
        cmd = 'arg1 "second arg with spaces" --flag'
        parsed = parse_args(cmd)
        self.assertEqual(parsed, ['arg1', 'second arg with spaces', '--flag'])

    def test_format_duration(self):
        self.assertEqual(format_duration(45), "45s")
        self.assertEqual(format_duration(125), "2m 5s")
        self.assertEqual(format_duration(3665), "1h 1m 5s")
        self.assertEqual(format_duration(90061), "1d 1h 1m 1s")

    def test_format_bytes(self):
        self.assertEqual(format_bytes(500), "500.0 B")
        self.assertEqual(format_bytes(1024), "1.0 KB")
        self.assertEqual(format_bytes(1048576), "1.0 MB")

    def test_progress_bar(self):
        bar = progress_bar(50, 100, length=10)
        self.assertIn("50%", bar)
        self.assertIn("▰", bar)
        self.assertIn("▱", bar)

if __name__ == "__main__":
    unittest.main()
