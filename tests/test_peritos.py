"""
Unit tests for peritos category
"""
import unittest

import requests

from tests.load_env import config


class TestPeritos(unittest.TestCase):
    """Tests for peritos category"""

    def test_get_tipos_de_peritos(self):
        """Test GET method for tipos de peritos"""
        response = requests.get(
            f"{config['api_base_url']}/peritos_tipos",
            headers={"X-Api-Key": config["api_key"]},
            timeout=config["timeout"],
        )
        self.assertEqual(response.status_code, 200)

    def test_get_peritos(self):
        """Test GET method for peritos"""
        response = requests.get(
            f"{config['api_base_url']}/peritos",
            headers={"X-Api-Key": config["api_key"]},
            timeout=config["timeout"],
        )
        self.assertEqual(response.status_code, 200)

    def test_get_peritos_by_tipo_de_perito(self):
        """Test GET method for peritos by tipo de perito 15 DACTILOSCOPIA"""
        response = requests.get(
            f"{config['api_base_url']}/peritos",
            headers={"X-Api-Key": config["api_key"]},
            params={"perito_tipo_id": 15},
            timeout=config["timeout"],
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["success"], True)
        for item in data["items"]:
            self.assertEqual(item["perito_tipo_id"], 15)

    def test_get_peritos_by_nombre(self):
        """Test GET method for peritos by nombre JUAN"""
        response = requests.get(
            f"{config['api_base_url']}/peritos",
            headers={"X-Api-Key": config["api_key"]},
            params={"nombre": "JUAN"},
            timeout=config["timeout"],
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["success"], True)
        for item in data["items"]:
            self.assertIn("JUAN", item["nombre"])

    def test_get_peritos_by_distrito_id(self):
        """Test GET method for peritos by distrito_id 6"""
        response = requests.get(
            f"{config['api_base_url']}/peritos",
            headers={"X-Api-Key": config["api_key"]},
            params={"distrito_id": 6},
            timeout=config["timeout"],
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["success"], True)
        for item in data["items"]:
            self.assertEqual(item["distrito_id"], 6)

    def test_get_peritos_by_distrito_id_by_tipo_de_perito(self):
        """Test GET method for peritos by distrito_id 6 by tipo de perito 15 DACTILOSCOPIA"""
        response = requests.get(
            f"{config['api_base_url']}/peritos",
            headers={"X-Api-Key": config["api_key"]},
            params={"distrito_id": 6, "perito_tipo_id": 15},
            timeout=config["timeout"],
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["success"], True)
        for item in data["items"]:
            self.assertEqual(item["distrito_id"], 6)
            self.assertEqual(item["perito_tipo_id"], 15)

    def test_get_peritos_by_distrito_id_by_nombre(self):
        """Test GET method for peritos by distrito_id 6 by nombre JUAN"""
        response = requests.get(
            f"{config['api_base_url']}/peritos",
            headers={"X-Api-Key": config["api_key"]},
            params={"distrito_id": 6, "nombre": "JUAN"},
            timeout=config["timeout"],
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["success"], True)
        for item in data["items"]:
            self.assertEqual(item["distrito_id"], 6)
            self.assertIn("JUAN", item["nombre"])

    def test_get_peritos_by_distrito_clave(self):
        """Test GET method for peritos by distrito_clave DTRC"""
        response = requests.get(
            f"{config['api_base_url']}/peritos",
            headers={"X-Api-Key": config["api_key"]},
            params={"distrito_clave": "DTRC"},
            timeout=config["timeout"],
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["success"], True)
        for item in data["items"]:
            self.assertEqual(item["distrito_clave"], "DTRC")

    def test_get_peritos_by_distrito_clave_by_tipo_de_perito(self):
        """Test GET method for peritos by distrito_clave DTRC by tipo de perito 15 DACTILOSCOPIA"""
        response = requests.get(
            f"{config['api_base_url']}/peritos",
            headers={"X-Api-Key": config["api_key"]},
            params={"distrito_clave": "DTRC", "perito_tipo_id": 15},
            timeout=config["timeout"],
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["success"], True)
        for item in data["items"]:
            self.assertEqual(item["distrito_clave"], "DTRC")
            self.assertEqual(item["perito_tipo_id"], 15)

    def test_get_peritos_by_distrito_clave_by_nombre(self):
        """Test GET method for peritos by distrito_clave DTRC by nombre JUAN"""
        response = requests.get(
            f"{config['api_base_url']}/peritos",
            headers={"X-Api-Key": config["api_key"]},
            params={"distrito_clave": "DTRC", "nombre": "JUAN"},
            timeout=config["timeout"],
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["success"], True)
        for item in data["items"]:
            self.assertEqual(item["distrito_clave"], "DTRC")
            self.assertIn("JUAN", item["nombre"])


if __name__ == "__main__":
    unittest.main()
