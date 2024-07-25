import struct
import math


def decimal_to_ieee(decimal_input, round_off_method):
    # Handle NaN input
    if decimal_input.lower() == 'nan':
        return 'NaN', 'NaN'
    
    # Convert input to float
    try: 
        float_value = float(decimal_input)
    except ValueError:
        return 'Invalid input', 'Invalid input'