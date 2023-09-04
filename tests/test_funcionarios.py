"""
Unit tests for funcionarios category
"""
import unittest

import requests

from tests.load_env import config


class TestFuncionarios(unittest.TestCase):
    """Tests for funcionarios category"""

    def test_get_centros_trabajos(self):
        """Test GET method for centros_trabajos"""
        response = requests.get(
            f"{config['host']}/v4/centros_trabajos",
            headers={"X-Api-Key": config["api_key"]},
            timeout=config["timeout"],
        )
        self.assertEqual(response.status_code, 200)

    def test_get_funcionarios(self):
        """Test GET method for funcionarios"""
        response = requests.get(
            f"{config['host']}/v4/funcionarios",
            headers={"X-Api-Key": config["api_key"]},
            timeout=config["timeout"],
        )
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
