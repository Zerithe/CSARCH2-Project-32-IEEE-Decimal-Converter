import math

def float_to_ieee_754_decimal32(value, rounding_method='nearest'):
    """
    Converts a floating-point number to IEEE 754 Decimal32 format.
    
    Parameters:
    - value (float): The floating-point number to convert.
    - rounding_method (str): The rounding method to apply. Options are 'nearest', 'truncate', 'down', 'up'.
    
    Returns:
    - tuple: Binary and hexadecimal representation of the Decimal32 formatted number.
    """
    
    # Handle special cases
    if math.isnan(value):
        print("Input is NaN")
        return '011111 10000 0000000000000000000000', '7c000000'
    elif math.isinf(value):
        if value > 0:
            print("Input is positive infinity")
            return '011110 00000 0000000000000000000000', '78000000'
        else:
            print("Input is negative infinity")
            return '111110 00000 0000000000000000000000', 'f8000000'
    elif value == 0:
        print("Input is zero")
        return '000000 00000 0000000000000000000000', '00000000'
    
    print(f"Initial value: {value}")

    # Step 1: Extract sign
    sign_bit = 0 if value >= 0 else 1
    value = abs(value)
    print(f"Sign bit: {sign_bit}")
    print(f"Absolute value: {value}")

    # Step 2: Normalize the number to 7 whole digits
    exponent = 0
    while value >= 10**7:
        value /= 10
        exponent += 1
    while value < 10**6 and value != 0:
        value *= 10
        exponent -= 1
    print(f"Normalized value: {value}")
    print(f"Exponent before biasing: {exponent}")

    # Adjust exponent to fit the bias of Decimal32 format
    exponent += 101
    print(f"Exponent after biasing: {exponent}")
    
    # Step 3: Get the Combination Field
    # Step CF1: Get the MSB of the value
    while value >= 10:
        value //= 10
    MSB_value = int(value)
    
    # Step CF2: Turn the MSB to binary
    bin_MSB_value = format(MSB_value, '04b')
    
    if MSB_value >= 0 and MSB_value < 8:
        # Change the exponent into binary
        bin_exponent = format(exponent, '08b')
        # Get the 2 MSB in the exponent
        A = bin_exponent[:2]
        B = bin_MSB_value[-3:]
        combination_field = str(A) + str(B)
    elif MSB_value == 8:
        A = "11"
        bin_exponent = format(exponent, '08b')
        B = bin_exponent[:2]
        C = "0"
        combination_field = str(A) + str(B) + str(C)
    elif MSB_value == 9:
        A = "11"
        bin_exponent = format(exponent, '08b')
        B = bin_exponent[:2]
        C = "1"
        combination_field = str(A) + str(B) + str(C)
    
    # Step 4: Apply rounding
    if rounding_method == 'truncate':
        significand = int(value)
    elif rounding_method == 'down':
        significand = math.floor(value)
    elif rounding_method == 'up':
        significand = math.ceil(value)
    elif rounding_method == 'nearest':
        significand = round(value)
    print(f"Significand after rounding ({rounding_method}): {significand}")

    # Step 5: Convert to binary
    sign_bin = f"{sign_bit:01b}"
    exponent_bin = f"{exponent:05b}"[1:]
    significand_bin = f"{significand:023b}"[1:24].ljust(26, '0')
    
    print(f"Binary sign bit: {sign_bin}")
    print(f"Binary combination field: {combination_field}")
    print(f"Binary exponent: {exponent_bin}")
    print(f"Binary significand: {significand_bin}")

    # Step 6: Combine all parts
    ieee_754_bin = sign_bin + combination_field + exponent_bin + significand_bin
    
    # Step 7: Convert to hexadecimal
    ieee_754_hex = f"{int(ieee_754_bin, 2):08x}"
    
    return f"{sign_bin} {combination_field} {exponent_bin} {significand_bin[:23]}", ieee_754_hex

# Example Usage
value = -9.234567 * 10**15
rounding_method = 'nearest'
binary_output, hex_output = float_to_ieee_754_decimal32(value, rounding_method)
print("Binary Output:", binary_output)
print("Hexadecimal Output:", hex_output)
