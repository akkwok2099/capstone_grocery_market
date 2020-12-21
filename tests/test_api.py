from unittest import TestCase
from api import aisles

# python3 -m unittest test_splitting.py


class TestApiMethods(TestCase):
    def test_get_aisles(self):
        # self.assertEqual(expected, actual)
        self.assertEqual([1], aisles())
