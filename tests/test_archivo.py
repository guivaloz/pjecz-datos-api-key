"""
Unit tests for the archivo category
"""
import unittest

import requests

from tests.load_env import config


class TestArchivo(unittest.TestCase):
    """Tests for the archivo category"""

    def test_get_arc_documentos(self):
        """Test GET method for arc_documentos"""
        response = requests.get(
            f"{config['host']}/v4/arc_documentos",
            headers={"X-Api-Key": config["api_key"]},
            timeout=config["timeout"],
        )
        self.assertEqual(response.status_code, 200)

    def test_get_arc_documentos_with_distrito_clave(self):
        """Test GET method for arc_documentos with distrito_clave"""
        response = requests.get(
            f"{config['host']}/v4/arc_documentos",
            headers={"X-Api-Key": config["api_key"]},
            params={"distrito_clave": "DSLT"},
            timeout=config["timeout"],
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["success"], True)
        for item in data["items"]:
            self.assertEqual(item["distrito_clave"], "DSLT")

    def test_get_arc_documentos_with_ubicacion(self):
        """Test GET method for arc_documentos with ubicacion"""
        response = requests.get(
            f"{config['host']}/v4/arc_documentos",
            headers={"X-Api-Key": config["api_key"]},
            params={"ubicacion": "ARCHIVO"},
            timeout=config["timeout"],
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["success"], True)
        for item in data["items"]:
            self.assertEqual(item["ubicacion"], "ARCHIVO")

    def test_get_arc_juzgados_extintos(self):
        """Test GET method for arc_juzgados_extintos"""
        response = requests.get(
            f"{config['host']}/v4/arc_juzgados_extintos",
            headers={"X-Api-Key": config["api_key"]},
            timeout=config["timeout"],
        )
        self.assertEqual(response.status_code, 200)

    def test_get_arc_remesas(self):
        """Test GET method for arc_remesas"""
        response = requests.get(
            f"{config['host']}/v4/arc_remesas",
            headers={"X-Api-Key": config["api_key"]},
            timeout=config["timeout"],
        )
        self.assertEqual(response.status_code, 200)

    def test_get_arc_remesas_documentos(self):
        """Test GET method for arc_remesas_documentos"""
        response = requests.get(
            f"{config['host']}/v4/arc_remesas_documentos",
            headers={"X-Api-Key": config["api_key"]},
            timeout=config["timeout"],
        )
        self.assertEqual(response.status_code, 200)

    def test_get_arc_solicitudes(self):
        """Test GET method for arc_solicitudes"""
        response = requests.get(
            f"{config['host']}/v4/arc_solicitudes",
            headers={"X-Api-Key": config["api_key"]},
            timeout=config["timeout"],
        )
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
