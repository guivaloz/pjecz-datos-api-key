"""
Unit tests for usuarios category
"""
import unittest

import requests

from tests.load_env import config


class TestUsuarios(unittest.TestCase):
    """Tests for usuarios category"""

    def test_get_bitacoras(self):
        """Test GET method for bitacoras"""
        response = requests.get(
            f"{config['host']}/v4/bitacoras",
            headers={"X-Api-Key": config["api_key"]},
            timeout=config["timeout"],
        )
        self.assertEqual(response.status_code, 200)

    def test_get_bitacoras_with_modulo_clave(self):
        """Test GET method for bitacoras with modulo_clave USUARIOS"""
        response = requests.get(
            f"{config['host']}/v4/bitacoras",
            params={"modulo_clave": "USUARIOS"},
            headers={"X-Api-Key": config["api_key"]},
            timeout=config["timeout"],
        )
        self.assertEqual(response.status_code, 200)

    def test_get_entradas_salidas(self):
        """Test GET method for entradas_salidas"""
        response = requests.get(
            f"{config['host']}/v4/entradas_salidas",
            headers={"X-Api-Key": config["api_key"]},
            timeout=config["timeout"],
        )
        self.assertEqual(response.status_code, 200)

    def test_get_modulos(self):
        """Test GET method for modulos"""
        response = requests.get(
            f"{config['host']}/v4/modulos",
            headers={"X-Api-Key": config["api_key"]},
            timeout=config["timeout"],
        )
        self.assertEqual(response.status_code, 200)

    def test_get_permisos(self):
        """Test GET method for permisos"""
        response = requests.get(
            f"{config['host']}/v4/permisos",
            headers={"X-Api-Key": config["api_key"]},
            timeout=config["timeout"],
        )
        self.assertEqual(response.status_code, 200)

    def test_get_roles(self):
        """Test GET method for roles"""
        response = requests.get(
            f"{config['host']}/v4/roles",
            headers={"X-Api-Key": config["api_key"]},
            timeout=config["timeout"],
        )
        self.assertEqual(response.status_code, 200)

    def test_get_usuarios(self):
        """Test GET method for usuarios"""
        response = requests.get(
            f"{config['host']}/v4/usuarios",
            headers={"X-Api-Key": config["api_key"]},
            timeout=config["timeout"],
        )
        self.assertEqual(response.status_code, 200)

    def test_get_usuarios_roles(self):
        """Test GET method for usuarios_roles"""
        response = requests.get(
            f"{config['host']}/v4/usuarios_roles",
            headers={"X-Api-Key": config["api_key"]},
            timeout=config["timeout"],
        )
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
