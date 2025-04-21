import unittest
from Root import sqroots


class TestRoot(unittest.TestCase):

    def test_1_root(self):
        self.assertEqual(sqroots("1 2 1"), "-1.0")

    def test_0_root(self):
        self.assertEqual(sqroots("1 2 5"), "")

    def test_2_root(self):
        self.assertEqual(sqroots("1 3 2"), "-2.0 -1.0")

    def test_exception_root(self):
        with self.assertRaises(ZeroDivisionError):
            sqroots("0 0 0")
