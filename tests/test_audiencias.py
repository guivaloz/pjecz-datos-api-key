"""
Unit tests for audiencias category
"""
import unittest

import requests

from tests.load_env import config


class TestAudiencias(unittest.TestCase):
    """Tests for audiencias category"""

    def test_get_audiencias(self):
        """Test GET method for audiencias"""
        response = requests.get(
            f"{config['host']}/v4/audiencias",
            headers={"X-Api-Key": config["api_key"]},
            timeout=config["timeout"],
        )
        self.assertEqual(response.status_code, 200)

    def test_get_audiencias_by_autoridad_id_35(self):
        """Test GET method for audiencias by autoridad_id 35"""
        response = requests.get(
            f"{config['host']}/v4/audiencias",
            headers={"X-Api-Key": config["api_key"]},
            params={"autoridad_id": 35},
            timeout=config["timeout"],
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["success"], True)
        for item in data["items"]:
            self.assertEqual(item["autoridad_id"], 35)

    def test_get_audiencias_by_autoridad_id_35_by_fecha(self):
        """Test GET method for audiencias by autoridad_id 35 and fecha 2023-05-11"""
        response = requests.get(
            f"{config['host']}/v4/audiencias",
            headers={"X-Api-Key": config["api_key"]},
            params={"autoridad_id": 35, "fecha": "2023-05-11"},
            timeout=config["timeout"],
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["success"], True)
        for item in data["items"]:
            self.assertEqual(item["autoridad_id"], 35)
            self.assertEqual(item["tiempo"].split("T")[0], "2023-05-11")

    def test_get_audiencias_by_autoridad_clave_35(self):
        """Test GET method for audiencias by autoridad_id 35"""
        response = requests.get(
            f"{config['host']}/v4/audiencias",
            headers={"X-Api-Key": config["api_key"]},
            params={"autoridad_clave": "SLT-J1-FAM"},
            timeout=config["timeout"],
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["success"], True)
        for item in data["items"]:
            self.assertEqual(item["autoridad_id"], 35)

    def test_get_audiencias_by_autoridad_clave_35_by_fecha(self):
        """Test GET method for audiencias by autoridad_id 35 and fecha 2023-05-11"""
        response = requests.get(
            f"{config['host']}/v4/audiencias",
            headers={"X-Api-Key": config["api_key"]},
            params={"autoridad_clave": "SLT-J1-FAM", "fecha": "2023-05-11"},
            timeout=config["timeout"],
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["success"], True)
        for item in data["items"]:
            self.assertEqual(item["autoridad_id"], 35)
            self.assertEqual(item["tiempo"].split("T")[0], "2023-05-11")


if __name__ == "__main__":
    unittest.main()
