Function: float_to_ieee_754_decimal32

Description:
  Converts a given floating-point number into its IEEE 754 Decimal32 format representation. 
  The function handles special cases such as NaN (Not a Number), positive infinity, negative infinity, and zero. 
  It also normalizes the value, adjusts the exponent to fit the bias, applies rounding, and formats the result in both binary and hexadecimal.

Parameters:
  - 'value' (float): The floating-point number to be converted.
  - 'rounding_method' (str, optional): The method used for rounding the significand. Options are 'nearest', 'truncate', 'down', and 'up'. Default is 'nearest'.
    
Returns:
  - tuple: A tuple containing the binary string representation and the hexadecimal string representation of the IEEE 754 Decimal32 format.
  
Special Cases:
1. NaN (Not a Number):
  - Returns '011111 10000 0000000000000000000000' in binary and '7c000000' in hexadecimal.
2. Positive Infinity:
  - Returns '011110 00000 0000000000000000000000' in binary and '78000000' in hexadecimal.
3. Negative Infinity:
  - Returns '111110 00000 0000000000000000000000' in binary and 'f8000000' in hexadecimal.
4. Zero:
  - Returns '000000 00000 0000000000000000000000' in binary and '00000000' in hexadecimal.
    
Steps:
1. Sign Extraction:
  - Determines the sign bit (0 for positive and 1 for negative).
  - Converts the value to its absolute form.

2.Normalization:
  - Normalizes the number to have 7 whole digits.
  - Adjusts the exponent accordingly.
    
3. Exponent Biasing:
  - Adds the bias value (101) to the exponent to fit the Decimal32 format.
    
4. Combination Field Calculation:
  - Determines the most significant bits (MSB) of the value.
  - Forms the combination field based on the MSB and the biased exponent.
    
5. Rounding:
  - Applies the specified rounding method to the significand.
    
6. Binary Conversion:
  - Converts the sign bit, combination field, exponent, and significand into binary format.

7. Combining Parts:
  - Combines all parts (sign bit, combination field, exponent, and significand) into a single binary string.

8. Hexadecimal Conversion:
  - Converts the combined binary string into its hexadecimal representation.
