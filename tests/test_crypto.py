import unittest
from unittest.mock import MagicMock
from nexus.modules.crypto import CryptoModule, COIN_MAP

class TestCryptoModule(unittest.TestCase):
    def setUp(self):
        self.mock_client = MagicMock()
        self.mock_db = MagicMock()
        self.module = CryptoModule(self.mock_client, self.mock_db)

    def test_coin_map(self):
        self.assertEqual(COIN_MAP["ton"], "the-open-network")
        self.assertEqual(COIN_MAP["btc"], "bitcoin")
        self.assertEqual(COIN_MAP["sol"], "solana")

    def test_commands_registration(self):
        self.assertTrue(hasattr(self.module.cmd_price, "_cmd_meta"))
        self.assertTrue(hasattr(self.module.cmd_qr, "_cmd_meta"))
        self.assertTrue(hasattr(self.module.cmd_gas, "_cmd_meta"))

if __name__ == "__main__":
    unittest.main()
