import sys
import math
import regex as re
import argparse

class CalibrationDoc():
    def __init__(self):
        self.calibration_values = 0

    def extract_values_from_doc(self, filename, debug):
        sum = 0
        text_digits = {}
        text_digits['one']   = 1
        text_digits['two']   = 2
        text_digits['three'] = 3
        text_digits['four']  = 4
        text_digits['five']  = 5
        text_digits['six']   = 6
        text_digits['seven'] = 7
        text_digits['eight'] = 8
        text_digits['nine']  = 9
        try:
            with open(filename, 'r') as fptr:
                for line in fptr:
                    if debug:
                        print (line, end='')
                    match = re.findall(r'(one|two|three|four|five|six|seven|eight|nine|\d)', line)
                    if match:
                        digit = match[0]
                        if len(digit) > 1:
                            tens_digit = text_digits[digit]
                        else:
                            tens_digit = int(digit)
                    else:
                        print(f'Error: RE failed on tens digit for {line.rstrip()}')
                        exit()

                    match = re.findall(r'(one|two|three|four|five|six|seven|eight|nine|\d)', line, overlapped=True)
                    if match:
                        digit = match[-1]
                        if len(digit) > 1:
                            ones_digit = text_digits[digit]
                        else:
                            ones_digit = int(digit)
                    else:
                        print(f'Error: RE failed on ones digit for {line.rstrip()}')
                        exit()

                    value = tens_digit * 10 + ones_digit
                    if debug:
                        print(f'Value = {value}\n')
                    sum += value

        except IOError:
            print(f"Error: Could not open \'{filename}\'")
            sys.exit(0)

        self.calibration_values = sum

    def print_cal_values(self):
        print (f'Calibration Value = {self.calibration_values}')


def parse_commandline():
    # Instantiate the parser
    parser = argparse.ArgumentParser(description='Optional app description')

    parser.add_argument('-v', '--values', type=str,
                        help='Filename for the calibration values')

    parser.add_argument('-d', '--debug', 
                        action="store_true",
                        help='Turn on verbosity')
    
    return parser.parse_args()


def main():
    cal_doc = CalibrationDoc()
    args = parse_commandline()
    cal_doc.extract_values_from_doc(args.values, args.debug)
    cal_doc.print_cal_values()

if __name__ == '__main__':
    main()