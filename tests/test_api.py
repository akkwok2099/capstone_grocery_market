from unittest import TestCase
from api import ge

# python3 -m unittest test_splitting.py


class TestSplitting(TestCase):
    def test_get_aisles(self):
        # self.assertEqual(expected, actual)
        self.assertEqual([1], split_amount(1, 1))
