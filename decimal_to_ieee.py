import math
import sys
import json

def float_to_ieee_754_decimal32(value, rounding_method):
    # Handle special cases
    if math.isnan(value):
        # print("Input is NaN")
        return '011111 10000 0000000000000000000000', '7c000000'
    elif math.isinf(value):
        if value > 0:
            # print("Input is positive infinity")
            return '011110 00000 0000000000000000000000', '78000000'
        else:
            # print("Input is negative infinity")
            return '111110 00000 0000000000000000000000', 'f8000000'
    elif value == 0:
        # print("Input is zero")
        return '000000 00000 0000000000000000000000', '00000000'
    
    # print(f"Initial value: {value}")

    # Step 1: Extract sign
    sign_bit = 0 if value >= 0 else 1
    value = abs(value)
    # print(f"Sign bit: {sign_bit}")
    # print(f"Absolute value: {value}")

    # Step 2: Normalize the number to 7 whole digits
    exponent = 0
    while value >= 10**7:
        value /= 10
        exponent += 1
    while value < 10**6 and value != 0:
        value *= 10
        exponent -= 1
    # print(f"Normalized value: {value}")
    # print(f"Exponent before biasing: {exponent}")

    # Adjust exponent to fit the bias of Decimal32 format
    exponent += 101
    # print(f"Exponent after biasing: {exponent}")
    
    # Step 3: Apply rounding
    if rounding_method == 'truncate':
        significand = int(value)
    elif rounding_method == 'down':
        significand = math.floor(value)
    elif rounding_method == 'up':
        significand = math.ceil(value)
    elif rounding_method == 'nearest':
        significand = round(value)
    # print(f"Significand after rounding ({rounding_method}): {significand}")

    # Step 4: Convert to binary
    sign_bin = f"{sign_bit:01b}"
    exponent_bin = f"{exponent:05b}"[1:]
    significand_bin = f"{significand:023b}"[1:24].ljust(26, '0')
    
    # print(f"Binary sign bit: {sign_bin}")
    # print(f"Binary exponent: {exponent_bin}")
    # print(f"Binary significand: {significand_bin}")

    # Step 5: Combine all parts
    ieee_754_bin = sign_bin + exponent_bin + significand_bin
    
    # Step 6: Convert to hexadecimal
    ieee_754_hex = f"{int(ieee_754_bin, 2):08x}"
    
    return f"{sign_bin} {exponent_bin} {significand_bin[:23]}", ieee_754_hex

# Example Usage
if __name__ == "__main__":
    decimal = sys.argv[1]
    exponent = sys.argv[2]
    rnd_mthd = sys.argv[3]

    #value = -1.234567 * 10**15
    value = float(decimal) * 10 ** int(exponent)
    rounding_method = 'nearest'
    binary_output, hex_output = float_to_ieee_754_decimal32(value, rounding_method)
    output = {
        'binary_output': str(binary_output),
        'hex_output': str(hex_output)
    }
    print(json.dumps(output))
    # print("Binary Output:", binary_output)
    # print("Hexadecimal Output:", hex_output)
