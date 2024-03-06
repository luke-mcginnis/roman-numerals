import unittest

from roman_numerals import *


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
            RomanNumeral(5.5)

        with self.assertRaises(InvalidRomanError):
            RomanNumeral(4000)

    def test_adding(self):
        pass  # todo: implement

    def test_subtracting(self):
        pass  # todo: implement

    def test_multiplying(self):
        pass  # todo: implement

    def test_dividing(self):
        pass  # todo: implement

    def test_floor_dividing(self):
        pass  # todo: implement

    def test_divmod(self):
        pass  # todo: implement

    def test_pow(self):
        pass  # todo: implement

    def test_logic(self):
        pass  # todo: implement

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
