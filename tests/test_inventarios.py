"""
Unit tests for inventarios category
"""
import unittest

import requests

from tests.load_env import config


class TestInventarios(unittest.TestCase):
    """Tests for inventarios category"""

    def test_get_inv_categorias(self):
        """Test GET method for inv_categorias"""
        response = requests.get(
            f"{config['host']}/v4/inv_categorias",
            headers={"X-Api-Key": config["api_key"]},
            timeout=config["timeout"],
        )
        self.assertEqual(response.status_code, 200)

    def test_get_inv_componentes(self):
        """Test GET method for inv_componentes"""
        response = requests.get(
            f"{config['host']}/v4/inv_componentes",
            headers={"X-Api-Key": config["api_key"]},
            timeout=config["timeout"],
        )
        self.assertEqual(response.status_code, 200)

    def test_get_inv_custodias(self):
        """Test GET method for inv_custodias"""
        response = requests.get(
            f"{config['host']}/v4/inv_custodias",
            headers={"X-Api-Key": config["api_key"]},
            timeout=config["timeout"],
        )
        self.assertEqual(response.status_code, 200)

    def test_get_inv_equipos(self):
        """Test GET method for inv_equipos"""
        response = requests.get(
            f"{config['host']}/v4/inv_equipos",
            headers={"X-Api-Key": config["api_key"]},
            timeout=config["timeout"],
        )
        self.assertEqual(response.status_code, 200)

    def test_get_inv_marcas(self):
        """Test GET method for inv_marcas"""
        response = requests.get(
            f"{config['host']}/v4/inv_marcas",
            headers={"X-Api-Key": config["api_key"]},
            timeout=config["timeout"],
        )
        self.assertEqual(response.status_code, 200)

    def test_get_inv_modelos(self):
        """Test GET method for inv_modelos"""
        response = requests.get(
            f"{config['host']}/v4/inv_modelos",
            headers={"X-Api-Key": config["api_key"]},
            timeout=config["timeout"],
        )
        self.assertEqual(response.status_code, 200)

    def test_get_inv_redes(self):
        """Test GET method for inv_redes"""
        response = requests.get(
            f"{config['host']}/v4/inv_redes",
            headers={"X-Api-Key": config["api_key"]},
            timeout=config["timeout"],
        )
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
