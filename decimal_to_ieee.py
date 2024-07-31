import math
import sys
import json
from decimal import Decimal, ROUND_HALF_UP, getcontext

def bcd(binary):
    """
    Convert a binary string to its Binary-Coded Decimal (BCD) representation.

    Parameters:
    - binary (str): The binary string to convert.

    Returns:
    - str: The BCD representation of the input binary string.
    """
    bcd_string = ''
    if binary[0] == '0' and binary[4] == '0' and binary[8] == '0':
        bcd_string = binary[1] + binary[2] + binary[3] + binary[5] + binary[6] + binary[7] + '0' + binary[9] + binary[10] + binary[11]
    elif binary[0] == '0' and binary[4] == '0' and binary[8] == '1':
        bcd_string = binary[1] + binary[2] + binary[3] + binary[5] + binary[6] + binary[7] + '1' + '0' + '0' + binary[11]
    elif binary[0] == '0' and binary[4] == '1' and binary[8] == '0':
        bcd_string = binary[1] + binary[2] + binary[3] + binary[9] + binary[10] + binary[7] + '1' + '0' + '1' + binary[11]
    elif binary[0] == '0' and binary[4] == '1' and binary[8] == '1':
        bcd_string = binary[1] + binary[2] + binary[3] + '1' + '0' + binary[7] + '1' + '1' + '1' + binary[11]
    elif binary[0] == '1' and binary[4] == '0' and binary[8] == '0':
        bcd_string = binary[9] + binary[10] + binary[3] + binary[5] + binary[6] + binary[7] + '1' + '1' + '0' + binary[11]
    elif binary[0] == '1' and binary[4] == '0' and binary[8] == '1':
        bcd_string = binary[5] + binary[6] + binary[3] + '0' + '1' + binary[7] + '1' + '1' + '1' + binary[11]
    elif binary[0] == '1' and binary[4] == '1' and binary[8] == '0':
        bcd_string = binary[9] + binary[10] + binary[3] + '0' + '0' + binary[7] + '1' + '1' + '1' + binary[11]
    elif binary[0] == '1' and binary[4] == '1' and binary[8] == '1':
        bcd_string = '0' + '0' + binary[3] + '1' + '1' + binary[7] + '1' + '1' + '1' + binary[11]
    return bcd_string

def str_to_binary(half):
    """
    Convert a string of digits to its binary representation.

    Parameters:
    - half (str): The string of digits to convert.

    Returns:
    - str: The binary representation of the input string.
    """
    binary_list = [format(int(char), 'b').zfill(4) for char in half]
    return ''.join(binary_list)

def round_half_away_from_zero(value):
    """
    Round a Decimal number away from zero.

    Parameters:
    - value (Decimal): The value to round.

    Returns:
    - Decimal: The rounded value.
    """
    if value > 0:
        return math.floor(value + 0.5)
    else:
        return math.ceil(value - 0.5)
    
def float_to_ieee_754_decimal32(value, rounding_method='nearest'):
    """
    Convert a floating-point number to IEEE 754 Decimal32 format.

    Parameters:
    - value (float): The floating-point number to convert.
    - rounding_method (str): The rounding method to apply. Options are 'nearest', 'truncate', 'down', 'up', 'nearestzero', 'nearesteven'.

    Returns:
    - tuple: Contains binary and hexadecimal representation of the Decimal32 formatted number, including:
        - Sign bit
        - Combination field
        - Exponent field
        - First half of the significand
        - Second half of the significand
        - Full significand
        - Full binary representation
        - Hexadecimal representation
    """
    getcontext().prec = 50
    
    # Handle special cases
    if math.isnan(value):
        return '0', '11111', '000000', '0000000000', '0000000000', '00000000000000000000', '0 11111 000000 0000000000 0000000000', '7c000000'
    elif math.isinf(value):
        if value > 0:
            return '0', '11110', '000000', '0000000000', '0000000000', '00000000000000000000', '0 11110 000000 0000000000 0000000000', '78000000'
        else:
            return '1', '11110', '000000', '0000000000', '0000000000', '00000000000000000000', '1 11110 000000 0000000000 0000000000', 'f8000000'
    elif value == 0:
        return '0', '00000', '000000', '0000000000', '0000000000', '00000000000000000000', '0 00000 000000 0000000000 0000000000', '00000000'
    
    # Extract sign bit
    sign_bit = 0 if value >= 0 else 1
    value = abs(value)
    
    # Normalize the number to 7 whole digits
    exponent = 0
    while value >= 10**7:
        value /= 10
        exponent += 1
    while value < 10**6 and value != 0:
        value *= 10
        exponent -= 1
    
    # Handle extreme exponents
    if exponent >= 90:
        return '0', '11110', '000000', '0000000000', '0000000000', '00000000000000000000', '0 11110 000000 0000000000 0000000000', '78000000'
    elif exponent <= -101:
        return '1', '11110', '000000', '0000000000', '0000000000', '00000000000000000000', '1 11110 000000 0000000000 0000000000', 'f8000000'
    
    # Adjust exponent to fit the Decimal32 format
    exponent += 101
    value_temp = value
    
    # Get the most significant bit (MSB) of the value
    while value_temp >= 10:
        value_temp //= 10
    MSB_value = int(value_temp)
    
    # Convert MSB to binary
    bin_MSB_value = format(MSB_value, '04b')
    
    # Determine the combination field based on MSB
    if MSB_value >= 0 and MSB_value < 8:
        bin_exponent = format(exponent, '08b')
        A = bin_exponent[:2]
        B = bin_MSB_value[-3:]
        combination_field = A + B
    elif MSB_value == 8:
        A = "11"
        bin_exponent = format(exponent, '08b')
        B = bin_exponent[:2]
        C = "0"
        combination_field = A + B + C
    elif MSB_value == 9:
        A = "11"
        bin_exponent = format(exponent, '08b')
        B = bin_exponent[:2]
        C = "1"
        combination_field = A + B + C

    # Apply rounding method
    if rounding_method == 'truncate':
        significand = int(value)
    elif rounding_method == 'down':
        significand = math.floor(value)
    elif rounding_method == 'up':
        significand = math.ceil(value)
    elif rounding_method == 'nearestzero':
        significand = round_half_away_from_zero(value)
    elif rounding_method == 'nearesteven':
        significand = round(value)
    
    # Convert significand to Dense BCD
    base = str(significand)[1:]
    first_half, second_half = str(base)[:len(str(base))//2], str(base)[len(str(base))//2:]
    first_half_bin = str_to_binary(first_half)
    second_half_bin = str_to_binary(second_half)
    first_significand = bcd(first_half_bin)
    second_significand = bcd(second_half_bin)

    # Convert to binary and hexadecimal
    sign_bin = f"{sign_bit:01b}"
    exponent_bin = f"{exponent:05b}"[1:]
    significand_bin = first_significand + second_significand

    ieee_754_bin = sign_bin + combination_field + exponent_bin + significand_bin
    ieee_754_hex = f"{int(ieee_754_bin, 2):08x}"
    
    return f"{sign_bin}", f"{combination_field}", f"{exponent_bin}", f"{first_significand}", f"{second_significand}", f"{significand_bin}", f"{sign_bin} {combination_field} {exponent_bin} {first_significand} {second_significand}", ieee_754_hex

if __name__ == "__main__":
    decimal_input = sys.argv[1]
    exponent_input = sys.argv[2]
    rnd_mthd = sys.argv[3]

    try:
        decimal = float(decimal_input)
        exponent = int(exponent_input)
        value = decimal * 10 ** int(exponent)
        results = float_to_ieee_754_decimal32(value, rnd_mthd)
    except ValueError:
        value = float('nan')
        results = float_to_ieee_754_decimal32(value, rnd_mthd)

    output = {
        'sign_bit': str(results[0]),
        'combination_bit': str(results[1]),
        'exponent_bit': str(results[2]),
        'first_significand_bit': str(results[3]),
        'second_significand_bit': str(results[4]),
        'significand_bit': str(results[5]),
        'binary_output': str(results[6]),
        'hex_output': str(results[7])
    }
    print(json.dumps(output))
