import sys
import re
import argparse


class Token():
    def __init__(self, start = 0, stop = 0, line = 0):
        self.start = start
        self.stop = stop
        self.line = line

    @property 
    def start(self):
        return self._start

    @start.setter 
    def start(self, start):
        self._start = start

    @property 
    def stop(self):
        return self._stop

    @stop.setter 
    def stop(self, stop):
        self._stop = stop
    
    @property 
    def line(self):
        return self._line

    @line.setter 
    def line(self, line):
        self._line = line

    def __str__(self):
        return f'Start={self.start} Stop={self.stop} Line={self.line}'
    
    def __eq__(self, other):
        if (self.start == other.start and
            self.stop == other.stop and
            self.line == other.line):
            return True
        else:
            return False

    def is_adjacent(self, other):
        if (((self.start - 1 <= other.start <= self.stop + 1) or
            (self.start - 1 <= other.stop <= self.stop + 1)) and
            (self.line -1 <= other.line <= self.line + 1)):
            return True
        else:
            return False


class SymbolToken(Token):
    def __init__(self, symbol, start, stop, line):
        super().__init__(start, stop, line)
        self.symbol = symbol

    @property 
    def symbol(self):
        return self._symbol

    @symbol.setter 
    def symbol(self, symbol):
        self._symbol = symbol
        
    def __str__(self):
        return f'SymbolToken: {super().__str__()} {self.symbol}'

class GearToken(SymbolToken):
    def __init__(self, start, stop, line):
        super().__init__('*', start, stop, line)
        self.ratio = 0

    @property 
    def ratio(self):
        return self._ratio

    @ratio.setter 
    def ratio(self, ratio):
        self._ratio = ratio
    
    def __str__(self):
        return f'SymbolToken: {super().__str__()} {self.symbol}'


class NumberToken(Token):
    def __init__(self, value, start, stop, line):
        super().__init__(start, stop, line)
        self.value = value
        self.is_part_number = False

    @property 
    def value(self):
        return self._value

    @value.setter 
    def value(self, value):
        self._value = value
        
    @property 
    def is_part_number(self):
        return self._is_part_number

    @is_part_number.setter 
    def is_part_number(self, value):
        self._is_part_number = value

    @property 
    def value(self):
        return self._value

    @value.setter 
    def value(self, value):
        self._value = value

    def __str__(self):
        return f'NumberToken: {super().__str__()} Value={self.value} PartNumber:{self.is_part_number}'


class Schematic():   
    def __init__(self):
        self.sum = 0
        self.gear_ratio = 0
        self._tokens = []

    def read_schematic(self, filename, debug=0):
        line_count = 0
        try:
            with open(filename, 'r') as fptr:
                for line in fptr:
                    line_count += 1
                    if debug:
                        print (line, end='')
                    for match in re.finditer(r'(\d+|[^\.])', line.rstrip()):
                        self.process_tokens(match.group(0),
                                            match.start(), 
                                            match.end() - 1, 
                                            line_count)
                        if debug:
                            print(f'process_tokens string="{match.group(0)}"')

        except IOError:
            print(f"Error: Could not open \'{filename}\'")
            sys.exit(0)

    def process_tokens(self, matched_string, start, stop, line_count ):
        if matched_string.isdigit():
            token = NumberToken(int(matched_string), 
                                    start,
                                    stop,
                                    line_count)
            
        else:
            if matched_string == '*':
                token = GearToken(start,
                                  stop,
                                  line_count)
            else:
                token = SymbolToken(matched_string,
                                    start,
                                    stop,
                                    line_count)
        self._tokens.append(token)

    def validate_token_as_part_number(self, token, debug=0):
        if isinstance(token, NumberToken):
            for other_token in self._tokens:
               if ((not token == other_token)
                   and (isinstance(other_token, SymbolToken))
                   and (token.is_adjacent(other_token))):
                    token.is_part_number = True
                    if debug:
                        print (f'  {other_token} Adjacent: {token.is_adjacent(other_token)} ')
                    return

    def check_gear_ratio(self, token, debug):
        factors = []
        if isinstance(token, GearToken):
            for other_token in self._tokens:
                if ((not token == other_token)
                   and (isinstance(other_token, NumberToken))
                   and (token.is_adjacent(other_token))):
                    factors.append(token)
            if len(factors) == 2:
                token.ratio = factors[0] * factors [1]

    def analyze_schematic(self, debug):
        for token in self._tokens:
            if debug:
                print(f'Token: {token}')
            self.validate_token_as_part_number(token, 0)
            self.check_gear_ratio(token, debug)

        sum = 0
        gear_ratio = 0
        for token in self._tokens:
            if (isinstance(token, NumberToken) and
                token.is_part_number):
                sum += token.value

            if isinstance(token, GearToken):
                gear_ratio += token.ratio

        self.sum = sum
        self.gear_ratio = gear_ratio

    def print_part_numbers(self):
        for token in self._tokens:
            if (isinstance(token, NumberToken) and
                token.is_part_number):
                print (f'{token.value}')

    @property 
    def sum(self):
        return self._sum

    @sum.setter 
    def sum(self, sum):
        self._sum = sum

    @property 
    def gear_ratio(self):
        return self._gear_ratio

    @gear_ratio.setter 
    def gear_ratio(self, gear_ratio):
        self._gear_ratio = gear_ratio


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
    schematic = Schematic()
    args = parse_commandline()
    schematic.read_schematic(args.puzzle)
    schematic.analyze_schematic(args.debug)
    if args.debug:
        print ('Part Number List')
        schematic.print_part_numbers()
        print ('Part Number List')
        schematic.print_gears()

    print(f'Part Number sum = {schematic.sum}')
    print(f'Part Number gear_ratio = {schematic.gear_ratio}')

if __name__ == '__main__':
    main()