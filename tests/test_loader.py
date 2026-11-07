import unittest
import tempfile
from pathlib import Path
from unittest.mock import MagicMock

from nexus.database import Database
from nexus.loader import BaseModule, ModuleManager, module, command, watcher

@module(name="Dummy", description="Dummy test module", author="tester", version="2.0.0")
class DummyModule(BaseModule):
    @command(name="pingpong", description="test ping", aliases=["pp"])
    async def cmd_pingpong(self, message, args):
        pass

    @watcher(incoming=True)
    async def watch_test(self, message):
        pass

class TestLoader(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = Path(self.temp_dir.name) / "test_loader.sqlite"
        self.db = Database(self.db_path)
        self.mock_client = MagicMock()
        self.manager = ModuleManager(self.mock_client, self.db)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_register_module(self):
        mod = DummyModule(self.mock_client, self.db)
        self.manager.register_module(mod)

        self.assertIn("dummy", self.manager.modules)
        self.assertIn("pingpong", self.manager.commands)
        self.assertIn("pp", self.manager.commands)
        self.assertEqual(len(self.manager.watchers), 1)

    def test_unregister_module(self):
        mod = DummyModule(self.mock_client, self.db)
        self.manager.register_module(mod)
        self.assertTrue(self.manager.unregister_module("dummy"))

        self.assertNotIn("dummy", self.manager.modules)
        self.assertNotIn("pingpong", self.manager.commands)
        self.assertNotIn("pp", self.manager.commands)
        self.assertEqual(len(self.manager.watchers), 0)

    def test_module_config(self):
        mod = DummyModule(self.mock_client, self.db)
        mod.set_config("custom_setting", 999)
        self.assertEqual(mod.get_config("custom_setting"), 999)
        self.assertTrue(mod.del_config("custom_setting"))

if __name__ == "__main__":
    unittest.main()
