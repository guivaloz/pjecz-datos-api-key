"""
Unit tests for redam category
"""
import unittest

import requests

from tests.load_env import config


class TestREDAM(unittest.TestCase):
    """Tests for redam category"""

    def test_get_redam(self):
        """Test GET method for redam"""
        response = requests.get(
            f"{config['host']}/v4/redam",
            headers={"X-Api-Key": config["api_key"]},
            timeout=config["timeout"],
        )
        self.assertEqual(response.status_code, 200)

    def test_get_redam_by_distrito_id_6(self):
        """Test GET method for redam by distrito_id 6"""
        response = requests.get(
            f"{config['host']}/v4/redam",
            headers={"X-Api-Key": config["api_key"]},
            params={"distrito_id": 6},
            timeout=config["timeout"],
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["success"], True)
        for item in data["items"]:
            self.assertEqual(item["distrito_id"], 6)

    def test_get_redam_by_distrito_id_6_by_nombre(self):
        """Test GET method for redam by distrito_id 6 by nombre LUIS"""
        response = requests.get(
            f"{config['host']}/v4/redam",
            headers={"X-Api-Key": config["api_key"]},
            params={"distrito_id": 6, "nombre": "LUIS"},
            timeout=config["timeout"],
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["success"], True)
        for item in data["items"]:
            self.assertEqual(item["distrito_id"], 6)
            self.assertIn("LUIS", item["nombre"])

    def test_get_redam_by_distrito_clave_dtrc(self):
        """Test GET method for redam by distrito_clave DTRC"""
        response = requests.get(
            f"{config['host']}/v4/redam",
            headers={"X-Api-Key": config["api_key"]},
            params={"distrito_clave": "DTRC"},
            timeout=config["timeout"],
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["success"], True)
        for item in data["items"]:
            self.assertEqual(item["distrito_clave"], "DTRC")

    def test_get_redam_by_distrito_clave_dtrc_by_nombre(self):
        """Test GET method for redam by distrito_clave DTRC by nombre LUIS"""
        response = requests.get(
            f"{config['host']}/v4/redam",
            headers={"X-Api-Key": config["api_key"]},
            params={"distrito_clave": "DTRC", "nombre": "LUIS"},
            timeout=config["timeout"],
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["success"], True)
        for item in data["items"]:
            self.assertEqual(item["distrito_clave"], "DTRC")
            self.assertIn("LUIS", item["nombre"])


if __name__ == "__main__":
    unittest.main()
