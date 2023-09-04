"""
Unit tests for abogados category
"""
import unittest

import requests

from tests.load_env import config


class TestAbogados(unittest.TestCase):
    """Tests for abogados category"""

    def test_get_abogados(self):
        """Test GET method for abogados"""
        response = requests.get(
            f"{config['api_base_url']}/abogados",
            headers={"X-Api-Key": config["api_key"]},
            timeout=config["timeout"],
        )
        self.assertEqual(response.status_code, 200)

    def test_get_abogados_by_nombre(self):
        """Test GET method for abogados by nombre GARZA"""
        response = requests.get(
            f"{config['api_base_url']}/abogados",
            headers={"X-Api-Key": config["api_key"]},
            params={"nombre": "GARZA"},
            timeout=config["timeout"],
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["success"], True)
        for item in data["items"]:
            self.assertIn("GARZA", item["nombre"])

    def test_get_abogados_by_nombre_by_anio(self):
        """Test GET method for abogados by nombre GARZA anio_desde 2020 anio_hasta 2021"""
        response = requests.get(
            f"{config['api_base_url']}/abogados",
            headers={"X-Api-Key": config["api_key"]},
            params={"nombre": "GARZA", "anio_desde": 2020, "anio_hasta": 2021},
            timeout=config["timeout"],
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["success"], True)
        for item in data["items"]:
            self.assertIn("GARZA", item["nombre"])
            self.assertGreaterEqual(item["fecha"].split("-")[0], "2020")
            self.assertLessEqual(item["fecha"].split("-")[0], "2021")


if __name__ == "__main__":
    unittest.main()
