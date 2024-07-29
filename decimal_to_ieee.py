import math
import sys
import json
from decimal import Decimal, ROUND_HALF_UP

def bcd(binary):
    
    bcd_string = ''

    if binary[0] == '0' and binary[4] == '0' and binary[8] == '0':
        bcd_string = binary[1] + binary[2] + binary[3] + binary[5] + binary[6] + binary[7] + '0' + binary[9] + binary[10] + binary[11] 

    elif binary[0] == '0' and binary[4] == '0' and binary[8] == '1':
        bcd_string = binary[1] + binary[2] + binary[3] + binary[5] + binary[6] + binary[7] + '1' + '0' + '0' + binary[11] 

    elif binary[0] == '0' and binary[4] == '1' and binary[8] == '0':
        bcd_string = binary[1] + binary[2] + binary[3] + binary[9] + binary[10] + binary[7] + '1' + '0'+ '1' + binary[11] 

    elif binary[0] == '0' and binary[4] == '1' and binary[8] == '1':
        bcd_string = binary[1] + binary[2] + binary[3] + '1' + '0' + binary[7] + '1' + '1' + '1' + binary[11] 

    elif binary[0] == '1' and binary[4] == '0' and binary[8] == '0':
        bcd_string = binary[9] + binary[10] + binary[3] + binary[5] + binary[6] + binary[7] + '1' + '1'+ '0' + binary[11] 

    elif binary[0] == '1' and binary[4] == '0' and binary[8] == '1':
        bcd_string = binary[5] + binary[6] + binary[3] + '0'+ '1' + binary[7] + '1' + '1' + '1' + binary[11] 

    elif binary[0] == '1' and binary[4] == '1' and binary[8] == '0':
        bcd_string = binary[9] + binary[10] + binary[3] + '0' + '0' + binary[7] + '1' + '1' + '1' + binary[11] 

    elif binary[0] == '1' and binary[4] == '1' and binary[8] == '1':
        bcd_string = '0' + '0' + binary[3] + '1'+ '1' + binary[7] + '1' + '1' + '1' + binary[11] 
    
    return bcd_string

def str_to_binary(half):
    binary_list = []

    for char in half:
        integer = int(char)
        binary = format(integer, 'b').zfill(4)
        binary_list.append(binary)

    return ''.join(binary_list)


def round_half_away_from_zero(value):
    if value > 0:
        return math.floor(value + 0.5)
    else:
        return math.ceil(value - 0.5)



def float_to_ieee_754_decimal32(value, rounding_method):
    # Handle special cases
    if math.isnan(value):
        # print("Input is NaN")
        return '0', '11111', '00000', '0000000000000000000000', '0 11111 00000 0000000000000000000000', '7c000000'
    elif value == 0:
        # print("Input is zero")
        return '0', '00000', '00000', '0000000000000000000000','0 00000 00000 0000000000000000000000', '00000000'
    
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
    if exponent >= 90:
        # print("Input is positive infinity")
        return '0', '11110', '00000', '0000000000000000000000','0 11110 00000 0000000000000000000000', '78000000'
    elif exponent <= -101:
        # print("Input is negative infinity")
        return '0', '11110', '00000', '0000000000000000000000', '1 11110 00000 0000000000000000000000', 'f8000000'
    # Adjust exponent to fit the bias of Decimal32 format
    exponent += 101
    # print(f"Exponent after biasing: {exponent}")
    value_temp = value
    # Get the Combination Field
    # Step CF1: Get the MSB of the value
    while value_temp >= 10:
        value_temp //= 10
    MSB_value = int(value_temp)
    #print(f"MSB value: {MSB_value}")                            # Get rid of this
    # Step CF2: Turn the MSB to binary
    bin_MSB_value = format(MSB_value, '04b')
    #print(f"Binary: {bin_MSB_value}")                           # Get rid of this
    
    if MSB_value >= 0 and MSB_value < 8:
        # Change the exponent into binary 
        #print(f"Exponent Binary: {exponent}")                   # Get rid of this
        bin_exponent = format(exponent, '08b')
        #print(f"Binary Exponent: {bin_exponent}")               # Get rid of this
        # Get the 2 MSB in the exponent
        A = bin_exponent[:2]
        #print (f"A: {A}")                                       # Get rid of this
        B = bin_MSB_value[-3:]
        #print (f"B: {B}")                                       # Get rid of this
        combination_field = str(A) + str(B)
        #print (f"Combination Field: {combination_field}")       #Get rid of this
    elif MSB_value == 8:
        A = "11"
        # Get the 2 MSB in the experiment
        bin_exponent = format(exponent, '08b')
        B = bin_exponent[:2]
        #print(f"Binary exponent: {bin_exponent}")
        #print(f"B: {B}")
        # Get the LSB of the value
        C = "0"
        combination_field = str(A) + str(B) + str(C)
    elif MSB_value == 9:
        A = "11"
        # Get the 2 MSB in the experiment
        bin_exponent = format(exponent, '08b')
        B = bin_exponent[:2]
        #print(f"Binary exponent: {bin_exponent}")
        #print(f"B: {B}")
        # Get the LSB of the value
        C = "1"
        combination_field = str(A) + str(B) + str(C)
    
    # Step 3: Apply rounding
    if rounding_method == 'truncate':
        significand = int(value)
    elif rounding_method == 'down':
        significand = math.floor(value)
    elif rounding_method == 'up':
        significand = math.ceil(value)
    elif rounding_method == 'nearestzero':
        significand = round_half_away_from_zero(value)
        #testing other methods below, not sure if right

        # decimals = 0
        # multiplier = 10 ** decimals
        # rounded = math.ceil(value*multiplier - 0.5) / multiplier
        # significand = rounded
        
        # significand = Decimal(value).quantize(Decimal('1'), rounding=ROUND_HALF_UP) * 1.0
        
        # if value.is_integer():
        #     significand = round(value)
        # else:
        #     lasttwo = float(str(value)[-3:]) if '.' in str(value)[-2:] else int(str(value)[-2:])


        # if value > 0:
        #     significand = math.floor(value + 0.5)
        # else:
        #     significand = math.ceil(value - 0.5)
    elif rounding_method == 'nearesteven':
        significand = round(value)
    # print(f"Significand after rounding ({rounding_method}): {significand}")

    # convert to Dense BCD
    base = str(significand)[1:]
    first_half, second_half = str(base)[:len(str(base))//2], str(base)[len(str(base))//2:]
    first_half_bin = str_to_binary(first_half)
    second_half_bin = str_to_binary(second_half)
    first_significand = bcd(first_half_bin)
    second_significand = bcd(second_half_bin)

    
    # Step 4: Convert to binary
    sign_bin = f"{sign_bit:01b}"
    exponent_bin = f"{exponent:05b}"[1:]
    significand_bin = first_significand + second_significand
    # print(f"Binary sign bit: {sign_bin}")
    # print(f"Binary exponent: {exponent_bin}")
    # print(f"Binary significand: {significand_bin}")

    # Step 5: Combine all parts
    ieee_754_bin = sign_bin + combination_field + exponent_bin + significand_bin
    
    # Step 6: Convert to hexadecimal
    ieee_754_hex = f"{int(ieee_754_bin, 2):08x}"
    
    return f"{sign_bin}", f"{combination_field}", f"{exponent_bin}", f"{first_significand}", f"{second_significand}", f"{significand_bin}", f"{sign_bin} {combination_field} {exponent_bin} {first_significand} {second_significand}", ieee_754_hex


if __name__ == "__main__":
    decimal_input = sys.argv[1]
    exponent_input = sys.argv[2]
    rnd_mthd = sys.argv[3]

    #value = -1.234567 * 10**15
    try:
        decimal = float(decimal_input)
        exponent = int(exponent_input)
        value = decimal * 10 ** int(exponent)
        sign_bit, combination_bit, exponent_bit, first_significand, second_significand, significand_bit, binary_output, hex_output = float_to_ieee_754_decimal32(value, rnd_mthd)
    except ValueError:
        value = float('nan')
        sign_bit, combination_bit, exponent_bit, first_significand, second_significand, significand_bit, binary_output, hex_output = float_to_ieee_754_decimal32(value, rnd_mthd)
    output = {
        'sign_bit': str(sign_bit),
        'combination_bit': str(combination_bit),
        'exponent_bit': str(exponent_bit),
        'first_significand_bit': str(first_significand),
        'second_significand_bit': str(second_significand),
        'significand_bit': str(significand_bit),
        'binary_output': str(binary_output),
        'hex_output': str(hex_output)
    }
    print(json.dumps(output))
    # print("Binary Output:", binary_output)
    # print("Hexadecimal Output:", hex_output)
