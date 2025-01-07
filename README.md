# roman-numerals

This Python module provides functionality for handling and performing operations with Roman numerals up to 3999.
It allows for standard arithmetic and boolean operations between two `RomanNumeral` objects or a `RomanNumeral` object
and an integer. The module simplifies the conversion between Roman numerals and integers, allowing for easy 
manipulation and mathematical operations with Roman numerals.

## Features
- Conversion between Roman numerals and integers.
- Support for arithmetic operations (addition, subtraction, multiplication, and floor division) with Roman numerals.
- Comparison operations between Roman numeral instances and integers.
- Random Roman numeral generation within a specified range.
- Validation of Roman numeral strings.

## Installation
Simply copy the module into your project directory. No external dependencies are required beyond the Python standard
library.

## Usage

```python
from roman_numerals import RomanNumeral

# Creating a RomanNumeral object
numeral = RomanNumeral(1990)
print(numeral)  # Output: MCMXC

# Arithmetic operations
result = numeral + RomanNumeral('X')
print(result)  # Output: MCMXCIX

# Conversion to integer
print(int(result))  # Output: 1995

# Generate a random Roman numeral from 1 to 100, inclusive.
random_numeral = RomanNumeral.random_numeral(max_value=100)
```
## Limitations
* Does not support [large number variants](https://en.wikipedia.org/wiki/Roman_numerals#Large_numbers) and thus does 
not support numerals larger than 3999. Creating a `RomanNumeral` object over this amount will raise an error.
* Does not support negative numbers. Creating a `RomanNumeral` object over this amount will raise an error.
* Does not support creation or operations with non-integer values. Generally, an error is raised when attempting
to create a non-integer `RomanNumeral` object, and operation values are floored. It is recommended to 
convert the `RomanNumeral` object to an integer before attempting operations with non-integers. 
* Only supports floor division to avoid confusion and to align with the integer-only use of roman numerals.

```python
from roman_numerals import RomanNumeral

# Not allowed, will each raise InvalidRomanError:
RomanNumeral(4000)  
RomanNumeral(3999) + RomanNumeral('V')  
RomanNumeral(-10) 
-1 * RomanNumeral(10) 

# No error, but will floor floats before calculating:
RomanNumeral(10) - 1.9  # 9
RomanNumeral(10) + 5.9  # 16
RomanNumeral(10) * 0.9  # 0

# Some operations floor after calculation and are preferred:
RomanNumeral(10) // 1.5  # 6
RomanNumeral(10) % 2.5  # 0
```

## License
This module is open-source software distributed under the MIT License. See [LICENSE](/LICENSE) for more information.


Copyright © 2024 Luke McGinnis
