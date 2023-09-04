"""
Unit tests for ubicaciones de expedientes category
"""
import unittest

import requests

from tests.load_env import config


class TestUbicacionesExpedientes(unittest.TestCase):
    """Tests for ubicaciones de expedientes category"""

    def test_get_ubicaciones_expedientes(self):
        """Test GET method for ubicaciones_expedientes"""
        response = requests.get(
            f"{config['api_base_url']}/ubicaciones_expedientes",
            headers={"X-Api-Key": config["api_key"]},
            timeout=config["timeout"],
        )
        self.assertEqual(response.status_code, 200)

    def test_get_ubicaciones_expedientes_by_autoridad_id_37(self):
        """Test GET method for ubicaciones_expedientes by autoridad_id 37"""
        response = requests.get(
            f"{config['api_base_url']}/ubicaciones_expedientes",
            headers={"X-Api-Key": config["api_key"]},
            params={"autoridad_id": 37},
            timeout=config["timeout"],
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["success"], True)
        for item in data["items"]:
            self.assertEqual(item["autoridad_id"], 37)

    def test_get_ubicaciones_expedientes_by_autoridad_id_37_and_expediente(self):
        """Test GET method for ubicaciones_expedientes by autoridad_id 37 and expediente 140/2023"""
        response = requests.get(
            f"{config['api_base_url']}/ubicaciones_expedientes",
            headers={"X-Api-Key": config["api_key"]},
            params={"autoridad_id": 37, "expediente": "140/2023"},
            timeout=config["timeout"],
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["success"], True)
        for item in data["items"]:
            self.assertEqual(item["autoridad_id"], 37)

    def test_get_ubicaciones_expedientes_by_autoridad_clave_stl_j2_civ(self):
        """Test GET method for ubicaciones_expedientes by autoridad_clave SLT-J2-CIV"""
        response = requests.get(
            f"{config['api_base_url']}/ubicaciones_expedientes",
            headers={"X-Api-Key": config["api_key"]},
            params={"autoridad_clave": "SLT-J2-CIV"},
            timeout=config["timeout"],
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["success"], True)
        for item in data["items"]:
            self.assertEqual(item["autoridad_clave"], "SLT-J2-CIV")

    def test_get_ubicaciones_expedientes_by_autoridad_clave_stl_j2_civ_and_expediente(self):
        """Test GET method for ubicaciones_expedientes by autoridad_clave SLT-J2-CIV and expediente 140/2023"""
        response = requests.get(
            f"{config['api_base_url']}/ubicaciones_expedientes",
            headers={"X-Api-Key": config["api_key"]},
            params={"autoridad_clave": "SLT-J2-CIV", "expediente": "140/2023"},
            timeout=config["timeout"],
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["success"], True)
        for item in data["items"]:
            self.assertEqual(item["autoridad_clave"], "SLT-J2-CIV")


if __name__ == "__main__":
    unittest.main()
