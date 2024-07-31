
# IEEE 754 Decimal32 Converter
This repository provides a Python program to convert floating-point numbers to IEEE 754 Decimal32 format. It supports different rounding methods and handles special cases such as NaN (Not a Number) and infinity.

## Notable Links:
#### Deployed Web Sim
- https://csarch2-project-32-ieee-decimal.onrender.com
#### Youtube Unlisted Link for Demo
- https://www.youtube.com/watch?v=RDygdXYcHd8
#### Google Drive Link for Write up, Test Cases, and Video Demo
- https://drive.google.com/drive/folders/1FMjwo4BJjRYNstsf27g0R7b2DOEI1ZUS?usp=drive_link

## Overview
The IEEE 754 Decimal32 format is a binary-coded decimal (BCD) representation of floating-point numbers. The converter in this repository converts a floating-point number into its IEEE 754 Decimal32 format and provides both binary and hexadecimal representations.

### Description:
  Converts a given floating-point number into its IEEE 754 Decimal32 format representation. 
  The function handles special cases such as NaN (Not a Number), positive infinity, negative infinity, and zero. 
  It also normalizes the value, adjusts the exponent to fit the bias, applies rounding, and formats the result in both binary and hexadecimal.
  
## Features

- **Conversion to IEEE 754 Decimal32 format**: Converts floating-point numbers to the IEEE 754 Decimal32 format.
- **Rounding methods**: Supports various rounding methods including 'nearest', 'truncate', 'down', 'up', 'nearestzero', and 'nearesteven'.
- **Handling special cases**: Handles NaN, positive infinity, and negative infinity.
- **Output**: Provides the binary and hexadecimal representation of the Decimal32 formatted number.

### How to start the Converter:
  Step 1: 
  Open in any Source Code Editor, or compiler.

  Step 2: 
  Open the terminal and input the command, "npm install" and then "npm start"

  Step 3:
  Once the server starts, you can open your browser and head to http://localhost:3000/, and you can use as you see fit.

### How to use the test script:
  Step 1: 
  Open in any Source Code Editor, or compiler.

  Step 2: 
  Open the terminal and input the command, "pip install pytest" and then "pytest test_decimal_ieee.py"

### Parameters:
- <decimal_input>: The floating-point number to be converted.
- <exponent_input>: The exponent to adjust the scale of the decimal number.
- <rounding_method>: The rounding method to apply. Options are 'nearest', 'truncate', 'down', 'up', 'nearestzero', 'nearesteven'.
    
### Returns:
The script will output a JSON object with the following fields:
- sign_bit: The sign bit of the IEEE 754 Decimal32 representation.
- combination_bit: The combination field of the IEEE 754 Decimal32 representation.
- exponent_bit: The exponent field of the IEEE 754 Decimal32 representation.
- first_significand_bit: The first half of the significand in binary.
- second_significand_bit: The second half of the significand in binary.
- significand_bit: The full significand in binary.
- binary_output: The complete binary representation of the Decimal32 formatted number.
- hex_output: The hexadecimal representation of the Decimal32 formatted number.
  
### Special Cases:
1. NaN (Not a Number):
  - Returns '011111 10000 0000000000000000000000' in binary and '7c000000' in hexadecimal.
2. Positive Infinity:
  - Returns '011110 00000 0000000000000000000000' in binary and '78000000' in hexadecimal.
3. Negative Infinity:
  - Returns '111110 00000 0000000000000000000000' in binary and 'f8000000' in hexadecimal.
4. Zero:
  - Returns '000000 00000 0000000000000000000000' in binary and '00000000' in hexadecimal.
    
### Steps:
1. Sign Extraction:
    - Determines the sign bit (0 for positive and 1 for negative).
    - Converts the value to its absolute form.

2. Normalization:
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
