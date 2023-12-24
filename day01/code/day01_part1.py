import sys
import math
import re
import argparse

class CalibrationDoc():
    def __init__(self):
        self.calibration_values = 0

    def extract_values_from_doc(self, filename, debug):
        sum = 0
        try:
            with open(filename, 'r') as fptr:
                for line in fptr:
                    if debug:
                        print (line, end='')
                    match = re.search(r'^\D*(\d)', line)
                    if match:
                       tens_digit = int(match.group(1))

                    match = re.search(r'^.*(\d)\D*$', line)
                    if match:
                       ones_digit = int(match.group(1))

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