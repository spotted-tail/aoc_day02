import sys
import re
import argparse


class LotteryCheck():
    def __init__(self):
        self.sum = 0

    @property 
    def sum(self):
        return self._sum

    @sum.setter 
    def sum(self, sum):
        self._sum = sum

    def read_card_stack(self, filename, debug=0):
        sum = 0
        try:
            with open(filename, 'r') as fptr:
                for line in fptr:
                    if debug:
                        print (line, end='')
                    line = re.sub(r'^Card\s+\d+\s*:', '', line.rstrip())
                    line = re.sub(r'^\s*', '', line)
                    line = re.sub(r'\s+', ' ', line)
                    line = re.sub(r'\s*\|\s*', '|', line)
                    winning_numbers_str, elfs_numbers_str = line.split('|')
                    winning_numbers = winning_numbers_str.split(' ')
                    elfs_numbers = elfs_numbers_str.split(' ')
                    if debug:
                        print(f'Winning Numbers: {winning_numbers}')
                        print(f'Elfs Numbers: {elfs_numbers}')
                    count = 0
                    for winning_num in winning_numbers:
                        if winning_num in elfs_numbers:
                            if debug:
                                print(f'  {winning_num} is a winner')
                            count += 1
                    if count:
                        value = 2**(count-1)
                    else:
                        value = 0

                    if debug:
                        print(f'  This card is worth {value} points')
                    if count:
                        sum += value
            self.sum = sum

        except IOError:
            print(f"Error: Could not open \'{filename}\'")
            sys.exit(0)


def parse_commandline():
    # Instantiate the parser
    parser = argparse.ArgumentParser(description='Optional app description')

    parser.add_argument('-p', '--puzzle', type=str,
                        help='Filename for the puzzle')

    parser.add_argument('-d', '--debug', 
                        action="store_true",
                        help='Turn on verbosity')
    
    return parser.parse_args()


def main():
    lottery_check = LotteryCheck()
    args = parse_commandline()
    lottery_check.read_card_stack(args.puzzle, args.debug)
    print (f'Scratch card pile is worth {lottery_check.sum} points')

if __name__ == '__main__':
    main()