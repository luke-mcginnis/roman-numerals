"""Module for roman numeral processing and operations.

Does not support any typographical variants, including large number
variants.

See Also
--------
https://en.wikipedia.org/wiki/Roman_numerals
"""

from __future__ import annotations

from collections import namedtuple
import functools
import random
import re

ROMAN_NUMERAL_VALUES = {
    'I': 1,
    'IV': 4,
    'V': 5,
    'IX': 9,
    'X': 10,
    'XL': 40,
    'L': 50,
    'XC': 90,
    'C': 100,
    'CD': 400,
    'D': 500,
    'CM': 900,
    'M': 1000
}


class InvalidRomanError(ValueError):
    """The provided Roman Numeral or value was invalid.
    """
    pass


PlaceValueTuple = namedtuple('PlaceValueTuple', ('thousands', 'hundreds', 'tens', 'ones'))


@functools.total_ordering
class RomanNumeral:
    """Class for roman numeral handling and operation.

    Most standard aritmatic and boolean operations are allowed between
    two RomanNumeral objects, or a RomanNumeral and integer. Arithmetic
    operators return a new RomanNumeral object. This object must have an
    integer value.

    RomanNumeral object can represent values in the interval [0, 3999].

    Parameters
    ----------
    numeral : str or int or float
        Instantiating value. Can be a valid roman numeral string, or an
        integer that is the a range than can be represented with roman
        numerals.

    Raises
    ------
    InvalidRomanNumeralError
        Raised if `numeral` can't be represented with roman numerals.

    Examples
    --------
    >>> print(RomanNumeral(12))
    XII

    >>> print(RomanNumeral('MMC').value)
    2100

    >>> print(RomanNumeral('X') + 5)
    XV

    >>> print(RomanNumeral('X') == 10)
    True
    """

    MIN_VALUE = 0
    MAX_VALUE = 3999

    def __init__(self, numeral) -> None:
        if isinstance(numeral, str):
            self._string = numeral.upper()
            self._check_roman_numeral(self._string)
        elif isinstance(numeral, int):
            self._string = self._roman_from_int(numeral)
        elif isinstance(numeral, float):
            if numeral.is_integer():
                self._string = self._roman_from_int(int(numeral))
            else:
                raise InvalidRomanError('Value must be an int or a float with a integer value. ')

    def __str__(self) -> str:
        return self._string

    def __int__(self) -> int:
        return self.value

    def __float__(self) -> float:
        return float(self.value)

    def __bool__(self) -> bool:
        return bool(self.value)

    def __len__(self) -> int:
        return len(self._string)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}('{self}', value={self.value})"

    def __add__(self, other) -> RomanNumeral:
        return self.__class__(self.value + float(other))

    def __sub__(self, other) -> RomanNumeral:
        return self.__class__(self.value - float(other))

    def __mul__(self, other) -> RomanNumeral:
        return self.__class__(self.value * float(other))

    def __truediv__(self, other) -> RomanNumeral:
        return self.__class__(self.value / float(other))

    def __floordiv__(self, other) -> RomanNumeral:
        return self.__class__(self.value // float(other))

    def __mod__(self, other) -> RomanNumeral:
        return self.__class__(self.value % float(other))

    def __divmod__(self, other) -> tuple[RomanNumeral, RomanNumeral]:
        return self.__floordiv__(float(other)), self.__mod__(float(other))

    def __pow__(self, power, modulo=None) -> RomanNumeral:
        return self.__class__(pow(self.value, float(power), float(modulo)))

    def __lt__(self, other) -> bool:
        return self.value < float(other)

    def __eq__(self, other) -> bool:
        return self.value == float(other)

    @property
    def value(self) -> int:
        """Evaluates and returns the value of the numeral."""

        self._check_roman_numeral(self._string)

        total = 0
        characters = self._string
        while characters:
            for numeral, value in reversed(ROMAN_NUMERAL_VALUES.items()):
                if characters.startswith(numeral):
                    total += value
                    characters = characters.removeprefix(numeral)

        return total

    def by_place(self) -> PlaceValueTuple[RomanNumeral]:
        """Returns a NamedTuple of the numeral broken down into
         RomanNumeral objects by place.

         The format is PlaceValueTuple(thousands, hundreds, tens, ones).
         """

        place_values = {'thousands': 1000,
                        'hundreds': 100,
                        'tens': 10,
                        'ones': 1}

        results = []
        remainder = self.value

        for place_name, place_value in place_values.items():
            floor_quotient, remainder = divmod(remainder, place_value)
            value = floor_quotient * place_value
            results.append(RomanNumeral(value))

        return PlaceValueTuple(*results)

    @classmethod
    def random_numeral(cls, min_value=0, max_value=None) -> RomanNumeral:
        """Returns a RomanNumeral with a random valid value."""
        max_value = getattr(cls, 'MAX_VALUE', max_value)
        return cls(random.randint(min_value, max_value))

    @classmethod
    def _roman_from_int(cls, number: int) -> str:
        if number > cls.MAX_VALUE:
            raise InvalidRomanError(f'Value cannot be greater than {cls.MAX_VALUE}. ')
        elif number < cls.MIN_VALUE:
            raise InvalidRomanError(f'Value cannot be less than {cls.MIN_VALUE}. ')

        roman = ''
        while number:
            for numeral, value in reversed(ROMAN_NUMERAL_VALUES.items()):
                for _ in range(number // value):
                    roman += numeral
                    number -= value

        return roman

    @staticmethod
    def _check_roman_numeral(numeral) -> None:
        valid_roman_numeral_regex = re.compile(
                r'^'
                r'M{0,3}'  # Thousands
                r'(CM|CD|D?C{0,3})'  # Hundreds
                r'(XC|XL|L?X{0,3})'  # Tens
                r'(IX|IV|V?I{0,3})'  # Ones
                r'$')
        if not re.match(valid_roman_numeral_regex, numeral):
            raise InvalidRomanError(f'Invalid roman numeral: "{numeral}".')


if __name__ == '__main__':
    RN = RomanNumeral
    while True:
        print(eval(input('>>> ')))
