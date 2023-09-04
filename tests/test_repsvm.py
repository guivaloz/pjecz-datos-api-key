"""
Unit tests for repsvm category
"""
import unittest

import requests

from tests.load_env import config


class TestREPSVM(unittest.TestCase):
    """Tests for repsvm category"""

    def test_get_repsvm(self):
        """Test GET method for repsvm_agresores"""
        response = requests.get(
            f"{config['api_base_url']}/repsvm_agresores",
            headers={"X-Api-Key": config["api_key"]},
            timeout=config["timeout"],
        )
        self.assertEqual(response.status_code, 200)

    def test_get_repsvm_by_distrito_id_6(self):
        """Test GET method for repsvm_agresores by distrito_id 6"""
        response = requests.get(
            f"{config['api_base_url']}/repsvm_agresores",
            headers={"X-Api-Key": config["api_key"]},
            params={"distrito_id": 6},
            timeout=config["timeout"],
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["success"], True)
        for item in data["items"]:
            self.assertEqual(item["distrito_id"], 6)

    def test_get_repsvm_by_distrito_id_6_by_nombre(self):
        """Test GET method for repsvm_agresores by distrito_id 6 by nombre PEDRO"""
        response = requests.get(
            f"{config['api_base_url']}/repsvm_agresores",
            headers={"X-Api-Key": config["api_key"]},
            params={"distrito_id": 6, "nombre": "PEDRO"},
            timeout=config["timeout"],
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["success"], True)
        for item in data["items"]:
            self.assertEqual(item["distrito_id"], 6)
            self.assertIn("PEDRO", item["nombre"])

    def test_get_repsvm_by_distrito_clave_dtrc(self):
        """Test GET method for repsvm_agresores by distrito_clave DTRC"""
        response = requests.get(
            f"{config['api_base_url']}/repsvm_agresores",
            headers={"X-Api-Key": config["api_key"]},
            params={"distrito_clave": "DTRC"},
            timeout=config["timeout"],
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["success"], True)
        for item in data["items"]:
            self.assertEqual(item["distrito_clave"], "DTRC")

    def test_get_repsvm_by_distrito_clave_dtrc_by_nombre(self):
        """Test GET method for repsvm_agresores by distrito_clave DTRC by nombre PEDRO"""
        response = requests.get(
            f"{config['api_base_url']}/repsvm_agresores",
            headers={"X-Api-Key": config["api_key"]},
            params={"distrito_clave": "DTRC", "nombre": "PEDRO"},
            timeout=config["timeout"],
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["success"], True)
        for item in data["items"]:
            self.assertEqual(item["distrito_clave"], "DTRC")
            self.assertIn("PEDRO", item["nombre"])


if __name__ == "__main__":
    unittest.main()
