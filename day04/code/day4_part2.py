import sys
import re
import argparse

class Card():
    def __init__(self, winning_numbers=[], elfs_numbers=[]):
        self.winning_numbers = winning_numbers
        self.elfs_numbers = elfs_numbers
        self.winner_count = 0

    @property 
    def winning_numbers(self):
        return self._winning_numbers

    @winning_numbers.setter 
    def winning_numbers(self, winning_numbers):
        self._winning_numbers = winning_numbers

    @property 
    def elfs_numbers(self):
        return self._elfs_numbers

    @elfs_numbers.setter 
    def elfs_numbers(self, elfs_numbers):
        self._elfs_numbers = elfs_numbers

    @property 
    def value(self):
        if self.winner_count:
            return 2**(self.winner_count - 1)
        return 0

    @property 
    def winner_count(self):
        return self._winner_count

    @winner_count.setter 
    def winner_count(self, winner_count):
        self._winner_count = winner_count

    def check_for_winners(self):
        count = 0
        for winning_num in self.winning_numbers:
            if winning_num in self.elfs_numbers:
                count += 1
        self.winner_count = count

    def __str__(self):
        return f'{",".join(self.winning_numbers)}| {",".join(self.elfs_numbers)} for {self.winner_count} winner(s)'

class LotteryCheck():
    def __init__(self):
        self.sum = 0
        self.stack_count = 0
        self._card_stack = []

    @property 
    def sum(self):
        return self._sum

    @sum.setter 
    def sum(self, sum):
        self._sum = sum

    @property 
    def stack_count(self):
        return self._stack_count

    @stack_count.setter 
    def stack_count(self, stack_count):
        self._stack_count = stack_count

    def read_card_stack(self, filename, debug=0):
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
                    card = Card(winning_numbers, elfs_numbers)
                    self._card_stack.append(card)
        except IOError:
            print(f"Error: Could not open \'{filename}\'")
            sys.exit(0)
        self.stack_count = len(self._card_stack)

    def process_card_stack(self, debug=0):
        card_counts = []
        max_cards = len(self._card_stack)
        card_count = 0
        if debug:
            print (f'DEBUG: There are {max_cards} in the stack prior to winnings')
        for card in self._card_stack:
            card.check_for_winners()
            card_counts.append(1)

        stack_index = 0
        for card in self._card_stack:
            if debug:
                print (f'DEBUG: Card {stack_index + 1} has {card_counts[stack_index]} card in the stack.')
                print (f'DEBUG: Card is {card}')

            if card.winner_count > 0:

                if stack_index + card.winner_count + 1 > max_cards:
                    print ('ERROR: Not enough cards to copy. Something seems wrong.')
                    print (f'Index={stack_index}, Winner Count={card.winner_count}')
                    exit(0)

                for index in range(card.winner_count):
                    card_counts[stack_index + index+1] += card_counts[stack_index]

            card_count += card_counts[stack_index]
            if debug:
                print(f'DEBUG: Current card count {card_count}\n')
            stack_index += 1
        self.stack_count = card_count

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
    lottery_check.read_card_stack(args.puzzle)
    print (f'There are {lottery_check.stack_count} cards in the starting stack')
    lottery_check.process_card_stack(args.debug)
    
    print (f'There are {lottery_check.stack_count} cards in the final stack')

if __name__ == '__main__':
    main()