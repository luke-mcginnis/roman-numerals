"""Module for roman numeral processing and operations.

Does not support large number variants (e.g. numbers over 3999),
negative roman numerals, or non-integer roman numerals.

See `RomanNumeral` documentation for more information and examples.

See Also
--------
https://en.wikipedia.org/wiki/Roman_numerals

"""

from __future__ import annotations

from typing import NamedTuple, NoReturn
import functools
import random
import re

LETTER_VALUES = {
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

PLACE_VALUES = {
    'thousands': 1000,
    'hundreds': 100,
    'tens': 10,
    'ones': 1
}

MIN_VALUE = 0
MAX_VALUE = 3999


class PlaceValueTuple(NamedTuple):
    thousands: RomanNumeral
    hundreds: RomanNumeral
    tens: RomanNumeral
    ones: RomanNumeral


class InvalidRomanError(ValueError):
    """The provided Roman Numeral or value was invalid.
    """
    pass


@functools.total_ordering
class RomanNumeral:
    """Class for roman numeral handling and operation.

    Most standard aritmatic and boolean operations are allowed between
    two RomanNumeral objects, or a RomanNumeral and integer. Arithmetic
    operators return a new RomanNumeral object.

    RomanNumeral object must have an integer value in the interval
    [0, 3999]. Aritmetic operations with non-integers are generally
    floored before computation. See Limitations section of README.md for
    more information and examples.

    Parameters
    ----------
    numeral : str or int or float
        Instantiating value. Can be a valid roman numeral string, or an
        integer that is in a range than can be represented with roman
        numerals.

    Attributes
    ----------
    value : int
        The numeric value of the roman numeral.

    Raises
    ------
    InvalidRomanNumeralError
        Raised if `numeral` can't be represented with roman numerals.
        This will happen if `numeral` is not an integer, or is ouside of
        the range [0, 3999].

    Examples
    --------
    >>> str(RomanNumeral(12))
    'XII'

    >>> print(RomanNumeral('MMC').value)
    2100

    >>> RomanNumeral(12) * 3
    RomanNumeral("XXXVI", value=36)

    """

    def __init__(self, numeral: str | int) -> None:
        if isinstance(numeral, str):
            self._string = numeral.upper()
            self.check_roman_numeral(self._string)
        elif isinstance(numeral, int):
            self._string = self._roman_from_int(numeral)
        elif isinstance(numeral, float):
            if numeral.is_integer():
                self._string = self._roman_from_int(int(numeral))
            else:
                raise InvalidRomanError('Value must be an int or a float with an integer value. ')
        self.value = self._get_value()

    def __str__(self) -> str:
        """Return the roman numeral string of the object."""
        return self._string

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}("{self._string}", value={self.value})'

    def __int__(self) -> int:
        return self.value

    def __bool__(self) -> bool:
        """Return True if the numeral value is more than zero."""
        return bool(self.value)

    def __float__(self) -> float:
        return float(self.value)

    def __len__(self) -> int:
        """Return the number of characters in the roman numeral string."""
        return len(self._string)

    def __hash__(self) -> int:
        return hash(self.value)

    def __add__(self, other: RomanNumeral | int) -> RomanNumeral:
        return self.__class__(self.value + int(other))

    def __radd__(self, other: RomanNumeral | int) -> RomanNumeral:
        return self.__class__(int(other) + self.value)

    def __sub__(self, other: RomanNumeral | int) -> RomanNumeral:
        return self.__class__(self.value - int(other))

    def __rsub__(self, other: RomanNumeral | int) -> RomanNumeral:
        return self.__class__(int(other) - self.value)

    def __mul__(self, other: RomanNumeral | int) -> RomanNumeral:
        return self.__class__(self.value * int(other))

    def __rmul__(self, other: RomanNumeral | int) -> RomanNumeral:
        return self.__class__(int(other) * self.value)

    def __truediv__(self, other) -> NoReturn:
        """True Division is not supported by `RomanNumeral` objects to avoid confusion and to avoid multiple implicit
        flooring operations.

        Use floor division (a // b) or convert to an int before dividing.
        """
        raise TypeError('True division is not supported for `RomanNumeral` objects. Use floor division or use '
                        '`object.value` for this operation.')

    def __rtruediv__(self, other) -> NoReturn:
        """See __truediv__."""
        raise TypeError('True division is not supported for `RomanNumeral` objects. Use floor division or use'
                        ' `object.value` for this operation.')

    def __floordiv__(self, other: RomanNumeral | float) -> RomanNumeral:
        return self.__class__(int(self.value // float(other)))

    def __rfloordiv__(self, other: RomanNumeral | float) -> RomanNumeral:
        return self.__class__(int(float(other) // self.value))

    def __mod__(self, other: RomanNumeral | float) -> RomanNumeral:
        return self.__class__(int(self.value % float(other)))

    def __rmod__(self, other: RomanNumeral | float) -> RomanNumeral:
        return self.__class__(int(float(other) % self.value))

    def __divmod__(self, other: RomanNumeral | float) -> tuple[RomanNumeral, RomanNumeral]:
        return self // other, self % other

    def __rdivmod__(self, other: RomanNumeral | int) -> tuple[RomanNumeral, RomanNumeral]:
        return other // self, other % self

    def __lt__(self, other: RomanNumeral | float) -> bool:
        return self.value < float(other)

    def __gt__(self, other: RomanNumeral | float) -> bool:
        return self.value > float(other)

    def __eq__(self, other: RomanNumeral | int) -> bool:
        return self.value == float(other)

    def __ne__(self, other: RomanNumeral | int) -> bool:
        return self.value != float(other)

    def __le__(self, other: RomanNumeral | float) -> bool:
        return self.value <= float(other)

    def __ge__(self, other: RomanNumeral | float) -> bool:
        return self.value >= float(other)

    def by_place_value(self) -> PlaceValueTuple[RomanNumeral]:
        """Returns a NamedTuple of the numeral broken down into
         individual RomanNumeral objects by place.

         The format is PlaceValueTuple(thousands, hundreds, tens, ones).

         Example
         -------
         >>> RomanNumeral('DLXVII').by_place_value()  # doctest: +NORMALIZE_WHITESPACE
         PlaceValueTuple(thousands=RomanNumeral("", value=0),
                         hundreds=RomanNumeral("D", value=500),
                         tens=RomanNumeral("LX", value=60),
                         ones=RomanNumeral("VII", value=7))

         >>> RomanNumeral('DLXVII').by_place_value().tens
         RomanNumeral("LX", value=60)

        """
        results = []
        remainder = self.value

        for place_value in PLACE_VALUES.values():
            floor_quotient, remainder = divmod(remainder, place_value)
            value = floor_quotient * place_value
            results.append(RomanNumeral(value))

        return PlaceValueTuple(*results)

    @classmethod
    def random_numeral(cls, min_value: int = 1, max_value: int = MAX_VALUE) -> RomanNumeral:
        """Return a RomanNumeral with a random valid value.

        The resulting value will be between min_value and max_value,
        inclusive.
        """
        if min_value < 0:
            raise ValueError('`min_value` must be greater than or equal to 0.')
        if max_value > MAX_VALUE:
            raise ValueError(f'`min_value` must be greater than or equal to {MAX_VALUE}.')

        return cls(random.randint(min_value, max_value))

    @staticmethod
    def check_roman_numeral(numeral: str) -> None:
        """Raise `InvalidRomanError` if a string is not a valid RomanNumeral."""
        valid_roman_numeral_regex = re.compile(
                r'^'
                r'M{0,3}'            # Thousands
                r'(CM|CD|D?C{0,3})'  # Hundreds
                r'(XC|XL|L?X{0,3})'  # Tens
                r'(IX|IV|V?I{0,3})'  # Ones
                r'$')
        if not re.match(valid_roman_numeral_regex, numeral):
            raise InvalidRomanError(f'Invalid roman numeral: "{numeral}". ')

    @classmethod
    def _roman_from_int(cls, number: int) -> str:
        if number > MAX_VALUE:
            raise InvalidRomanError(f'Value cannot be greater than {MAX_VALUE}. ')
        elif number < MIN_VALUE:
            raise InvalidRomanError(f'Value cannot be less than {MIN_VALUE}. ')

        roman = ''
        while number:
            # Find possible values - from high to low.
            for numeral, value in reversed(LETTER_VALUES.items()):
                # Add letters to the numeral, as found.
                for _ in range(number // value):
                    roman += numeral
                    number -= value

        return roman

    def _get_value(self) -> int:
        """Evaluate and return the value of the numeral."""

        self.check_roman_numeral(self._string)

        total = 0
        characters = self._string
        while characters:
            for numeral, value in reversed(LETTER_VALUES.items()):
                if characters.startswith(numeral):
                    total += value
                    characters = characters.removeprefix(numeral)

        return total


if __name__ == '__main__':
    help(RomanNumeral)
