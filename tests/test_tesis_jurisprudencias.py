"""
Unit tests for tesis_jurisprudencias category
"""
import unittest

import requests

from tests.load_env import config


class TestTesisJurisprudencias(unittest.TestCase):
    """Tests for tesis_jurisprudencias category"""

    def test_get_epocas(self):
        """Test GET method for epocas"""
        response = requests.get(
            f"{config['host']}/v4/epocas",
            headers={"X-Api-Key": config["api_key"]},
            timeout=config["timeout"],
        )
        self.assertEqual(response.status_code, 200)

    def test_get_tesis_jurisprudencias(self):
        """Test GET method for tesis_jurisprudencias"""
        response = requests.get(
            f"{config['host']}/v4/tesis_jurisprudencias",
            headers={"X-Api-Key": config["api_key"]},
            timeout=config["timeout"],
        )
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
