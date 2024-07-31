import subprocess
import json

def run_test(decimal, exponent, rounding_method, expected):
    # Construct the command to run the script
    cmd = ['python', 'decimal_to_ieee.py', str(decimal), str(exponent), rounding_method]
    
    # Run the script and capture the output
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    # Print the standard output and standard error for debugging
    print("STDOUT:", result.stdout)
    print("STDERR:", result.stderr)
    
    # Check if there was an error in running the script
    if result.returncode != 0:
        raise RuntimeError(f"Command failed with return code {result.returncode}")
    
    # Parse the JSON output
    try:
        output = json.loads(result.stdout)
    except json.JSONDecodeError as e:
        raise RuntimeError(f"Failed to parse JSON: {e}")
    
    # Assert that the output matches the expected values
    assert output['sign_bit'] == expected['sign_bit']
    assert output['combination_bit'] == expected['combination_bit']
    assert output['exponent_bit'] == expected['exponent_bit']
    assert output['first_significand_bit'] == expected['first_significand_bit']
    assert output['second_significand_bit'] == expected['second_significand_bit']
    assert output['significand_bit'] == expected['significand_bit']
    assert output['binary_output'] == expected['binary_output']
    assert output['hex_output'] == expected['hex_output']

def test_decimal_to_ieee():
    # Test cases
    test_cases = [
        {
            # positive decimal 
            'decimal': '1234567.55', 
            'exponent': 15, 
            'rounding_method': 'nearesteven', 
            'expected': {
                'sign_bit': '0',
                'combination_bit': '01001',
                'exponent_bit': '110100',
                'first_significand_bit': '0100110100',
                'second_significand_bit': '1011101000',
                'significand_bit': '01001101001011101000',
                'binary_output': '0 01001 110100 0100110100 1011101000',
                'hex_output': '2744d2e8'
            }
        }, 
        {
            # negative decimal
            'decimal': '-1234567.55', 
            'exponent': 15, 
            'rounding_method': 'nearesteven', 
            'expected': {
                'sign_bit': '1',
                'combination_bit': '01001',
                'exponent_bit': '110100',
                'first_significand_bit': '0100110100',
                'second_significand_bit': '1011101000',
                'significand_bit': '01001101001011101000',
                'binary_output': '1 01001 110100 0100110100 1011101000',
                'hex_output': 'a744d2e8'
            }
        }, 
          {
            # negative exponent - also nearest even
            'decimal': '-8765432', 
            'exponent': -20, 
            'rounding_method': 'nearesteven', 
            'expected': {
                'sign_bit': '1',
                'combination_bit': '11010',
                'exponent_bit': '010001',
                'first_significand_bit': '1111100101',
                'second_significand_bit': '1000110010',
                'significand_bit': '11111001011000110010',
                'binary_output': '1 11010 010001 1111100101 1000110010',
                'hex_output': 'e91f9632'
            }
        }, 
          {
            # negative exponent - truncation
            'decimal': '-8765432', 
            'exponent': -20, 
            'rounding_method': 'truncate', 
            'expected': {
                'sign_bit': '1',
                'combination_bit': '11010',
                'exponent_bit': '010001',
                'first_significand_bit': '1111100101',
                'second_significand_bit': '1000110001',
                'significand_bit': '11111001011000110001',
                'binary_output': '1 11010 010001 1111100101 1000110001',
                'hex_output': 'e91f9631'
            }
        }, 
          {
            # negative exponent - Round up
            'decimal': '-8765432', 
            'exponent': -20, 
            'rounding_method': 'up', 
            'expected': {
                'sign_bit': '1',
                'combination_bit': '11010',
                'exponent_bit': '010001',
                'first_significand_bit': '1111100101',
                'second_significand_bit': '1000110010',
                'significand_bit': '11111001011000110010',
                'binary_output': '1 11010 010001 1111100101 1000110010',
                'hex_output': 'e91f9632'
            }
        }, 
          {
            # negative exponent - Round down
            'decimal': '-8765432', 
            'exponent': -20, 
            'rounding_method': 'down', 
            'expected': {
                'sign_bit': '1',
                'combination_bit': '11010',
                'exponent_bit': '010001',
                'first_significand_bit': '1111100101',
                'second_significand_bit': '1000110001',
                'significand_bit': '11111001011000110001',
                'binary_output': '1 11010 010001 1111100101 1000110001',
                'hex_output': 'e91f9631'
            }
        },
          {
            # negative exponent - Nearest Zero
            'decimal': '-8765432', 
            'exponent': -20, 
            'rounding_method': 'nearestzero', 
            'expected': {
                'sign_bit': '1',
                'combination_bit': '11010',
                'exponent_bit': '010001',
                'first_significand_bit': '1111100101',
                'second_significand_bit': '1000110010',
                'significand_bit': '11111001011000110010',
                'binary_output': '1 11010 010001 1111100101 1000110010',
                'hex_output': 'e91f9632'
            }
        },  
          
        {
            # zero
            'decimal': '0', 
            'exponent': 0, 
            'rounding_method': 'truncate', 
            'expected': {
                'sign_bit': '0',
                'combination_bit': '00000',
                'exponent_bit': '000000',
                'first_significand_bit': '0000000000',
                'second_significand_bit': '0000000000',
                'significand_bit': '00000000000000000000',
                'binary_output': '0 00000 000000 0000000000 0000000000',
                'hex_output': '00000000'
            }
        }, 
        {
            # special cases - NaN
            'decimal': 'NaN', 
            'exponent': 0, 
            'rounding_method': 'nearesteven', 
            'expected': {
                'sign_bit': '0',
                'combination_bit': '11111',
                'exponent_bit': '000000',
                'first_significand_bit': '0000000000',
                'second_significand_bit': '0000000000',
                'significand_bit': '00000000000000000000',
                'binary_output': '0 11111 000000 0000000000 0000000000',
                'hex_output': '7c000000'
            }
        }, {
           #special cases - +Infinity
            'decimal': '-8765432', 
            'exponent': 91, 
            'rounding_method': 'nearesteven', 
            'expected': {
                'sign_bit': '0',
                'combination_bit': '11110',
                'exponent_bit': '000000',
                'first_significand_bit': '0000000000',
                'second_significand_bit': '0000000000',
                'significand_bit': '00000000000000000000',
                'binary_output': '0 11110 000000 0000000000 0000000000',
                'hex_output': '78000000'
            }
         } ,
         {
            # special cases - -Infinity
             'decimal': '-8765432', 
             'exponent': -101, 
             'rounding_method': 'truncate', 
             'expected': {
             'sign_bit': '1',
             'combination_bit': '11110',
             'exponent_bit': '000000',
             'first_significand_bit': '0000000000',
             'second_significand_bit': '0000000000',
             'significand_bit': '00000000000000000000',
             'binary_output': '1 11110 000000 0000000000 0000000000',
             'hex_output': 'f8000000'
             }
         }   
    ]
    
    for case in test_cases:
        run_test(case['decimal'], case['exponent'], case['rounding_method'], case['expected'])

if __name__ == '__main__':
    test_decimal_to_ieee()
