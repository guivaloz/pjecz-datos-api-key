"""
Unit tests for siga category
"""
import unittest

import requests

from tests.load_env import config


class TestSiga(unittest.TestCase):
    """Tests for siga category"""

    def test_get_siga_salas(self):
        """Test GET method for siga_salas"""
        response = requests.get(
            f"{config['host']}/v4/siga_salas",
            headers={"X-Api-Key": config["api_key"]},
            timeout=config["timeout"],
        )
        self.assertEqual(response.status_code, 200)

    def test_get_siga_grabaciones(self):
        """Test GET method for siga_grabaciones"""
        response = requests.get(
            f"{config['host']}/v4/siga_grabaciones",
            headers={"X-Api-Key": config["api_key"]},
            timeout=config["timeout"],
        )
        self.assertEqual(response.status_code, 200)

    def test_get_siga_bitacoras(self):
        """Test GET method for siga_bitacoras"""
        response = requests.get(
            f"{config['host']}/v4/siga_bitacoras",
            headers={"X-Api-Key": config["api_key"]},
            timeout=config["timeout"],
        )
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
