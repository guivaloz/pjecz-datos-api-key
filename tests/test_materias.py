"""
Unit tests for materias category
"""
import unittest

import requests

from tests.load_env import config


class TestMaterias(unittest.TestCase):
    """Tests for materias category"""

    def test_get_materias(self):
        """Test GET method for materias"""
        response = requests.get(
            f"{config['api_base_url']}/materias",
            headers={"X-Api-Key": config["api_key"]},
            timeout=config["timeout"],
        )
        self.assertEqual(response.status_code, 200)

    def test_get_materias_tipos_juicios(self):
        """Test GET method for materias_tipos_juicios"""
        response = requests.get(
            f"{config['api_base_url']}/materias_tipos_juicios",
            headers={"X-Api-Key": config["api_key"]},
            timeout=config["timeout"],
        )
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
