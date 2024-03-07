"""
Tests for functionality of roman_numerals.RomanNumeral

"""

import unittest

from roman_numerals import *


# noinspection SpellCheckingInspection
class TestRomanNumeral(unittest.TestCase):
    def test_construction_from_numeral_string(self):
        self.assertEqual(RomanNumeral('I').value, 1)
        self.assertEqual(RomanNumeral('dLvI').value, 556)
        self.assertEqual(RomanNumeral('XVIII').value, 18)
        self.assertEqual(RomanNumeral('MMMCMXCIX').value, 3999)

        with self.assertRaises(InvalidRomanError):
            RomanNumeral(' ')

        with self.assertRaises(InvalidRomanError):
            RomanNumeral('XXXX')

        with self.assertRaises(InvalidRomanError):
            RomanNumeral('XXE')

    def test_construction_from_number(self):
        self.assertEqual(str(RomanNumeral(1)), 'I')
        self.assertEqual(str(RomanNumeral(3999)), 'MMMCMXCIX')
        self.assertEqual(str(RomanNumeral(58)), 'LVIII')

        with self.assertRaises(InvalidRomanError):
            RomanNumeral(-1)

        with self.assertRaises(InvalidRomanError):
            # noinspection PyTypeChecker
            RomanNumeral(5.5)

        with self.assertRaises(InvalidRomanError):
            RomanNumeral(4000)

    def test_adding(self):
        self.assertEqual(RomanNumeral(5) + RomanNumeral(10), RomanNumeral(15))
        self.assertEqual(RomanNumeral(5) + 100, RomanNumeral(105))
        self.assertEqual(100 + RomanNumeral(5), RomanNumeral(105))
        self.assertEqual(RomanNumeral(0) + 0, RomanNumeral(0))

        with self.assertRaises(InvalidRomanError):
            RomanNumeral(3999) + 1

    def test_subtracting(self):
        self.assertEqual(RomanNumeral(15) - RomanNumeral(10), RomanNumeral(5))
        self.assertEqual(15 - RomanNumeral(10), RomanNumeral(5))
        self.assertEqual(RomanNumeral(100) - 5, RomanNumeral(95))
        self.assertEqual(RomanNumeral(0) + 0, RomanNumeral(0))

        with self.assertRaises(InvalidRomanError):
            RomanNumeral(1) - 5

    # noinspection PyTypeChecker
    def test_multiplying(self):
        self.assertEqual(RomanNumeral(2) * RomanNumeral(5), RomanNumeral(10))
        self.assertEqual(RomanNumeral(0) * RomanNumeral(5), RomanNumeral(0))
        self.assertEqual(RomanNumeral(10) * 5, RomanNumeral(50))
        self.assertEqual(10 * RomanNumeral(5), RomanNumeral(50))

        self.assertEqual(RomanNumeral(1) * 0.4, RomanNumeral(0))
        self.assertEqual(1.9 * RomanNumeral(1), RomanNumeral(1))

        with self.assertRaises(InvalidRomanError):
            RomanNumeral(1) * -1

    def test_dividing(self):
        with self.assertRaises(TypeError):
            RomanNumeral(1) / 1

        with self.assertRaises(TypeError):
            1 / RomanNumeral(1)

    def test_modulo(self):
        self.assertEqual(RomanNumeral(5) % 2, RomanNumeral(1))
        self.assertEqual(5 % RomanNumeral(2), RomanNumeral(1))
        self.assertEqual(RomanNumeral(4) % RomanNumeral(1), RomanNumeral(0))
        self.assertEqual(RomanNumeral(4) % RomanNumeral(1), RomanNumeral(0))
        with self.assertRaises(InvalidRomanError):
            RomanNumeral(10) % -3

    def test_floor_dividing(self):
        self.assertEqual(RomanNumeral(10) // 2, RomanNumeral(5))
        self.assertEqual(5 // RomanNumeral(2), RomanNumeral(2))
        self.assertEqual(RomanNumeral(1) // RomanNumeral(2), RomanNumeral(0))

    def test_divmod(self):
        self.assertEqual(divmod(RomanNumeral(5), 2), (RomanNumeral(2), RomanNumeral(1)))
        self.assertEqual(divmod(10, RomanNumeral(3)), (RomanNumeral(3), RomanNumeral(1)))

    def test_equals(self):
        # __eq__
        self.assertTrue(RomanNumeral(1) == 1)
        self.assertTrue(RomanNumeral(1) == 1.0)
        self.assertTrue(10 == RomanNumeral(10))
        self.assertFalse(RomanNumeral(1) == 2)
        self.assertTrue(RomanNumeral(2) + RomanNumeral(3) == 5)
        # __ne__
        self.assertTrue(RomanNumeral(1) != 2)
        self.assertFalse(RomanNumeral(1) != 1)

    def test_less(self):
        # __lt__
        self.assertTrue(RomanNumeral(2) < 5)
        self.assertTrue(RomanNumeral(2) < RomanNumeral(5))
        self.assertTrue(RomanNumeral(2) < 5.0)
        self.assertFalse(RomanNumeral(2) < 2)
        self.assertFalse(RomanNumeral(2) < 1)

    def test_less_equal(self):
        self.assertTrue(RomanNumeral(1) <= RomanNumeral(2))
        self.assertTrue(RomanNumeral(1) <= RomanNumeral(1))

    def test_greater(self):
        self.assertTrue(RomanNumeral(5) > 2)
        self.assertTrue(RomanNumeral(5) > RomanNumeral(2))

    def test_greater_equal(self):
        self.assertTrue(RomanNumeral(2) >= RomanNumeral(1))
        self.assertTrue(RomanNumeral(1) >= RomanNumeral(1))

    def test_by_place_value(self):
        places = RomanNumeral(1234).by_place_value()
        self.assertEqual(places.ones, RomanNumeral(4))
        self.assertEqual(places.tens, RomanNumeral(30))
        self.assertEqual(places.hundreds, RomanNumeral(200))
        self.assertEqual(places.thousands, RomanNumeral(1000))

        # Indexed backwards for future additions of more places.
        self.assertEqual(places[-1], RomanNumeral(4))
        self.assertEqual(places[-2], RomanNumeral(30))
        self.assertEqual(places[-3], RomanNumeral(200))
        self.assertEqual(places[-4], RomanNumeral(1000))


if __name__ == '__main__':
    unittest.main()
