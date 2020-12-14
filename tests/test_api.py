from unittest import TestCase
from splitting import split_amount

# python3 -m unittest test_splitting.py


class TestSplitting(TestCase):
    def test_split_amount(self):
        # self.assertEqual(expected, actual)
        self.assertEqual([1], split_amount(1, 1))
