import sys
import re
import argparse

class CubeDraw():
    def __init__(self):
        self.blue = 0
        self.red = 0
        self.green = 0

    @property 
    def red(self):
        return self._red

    @red.setter 
    def red(self,red):
        self._red = red

    @property 
    def blue(self):
        return self._blue

    @blue.setter 
    def blue(self,blue):
        self._blue = blue

    @property 
    def green(self):
        return self._green

    @green.setter 
    def green(self,green):
        self._green = green

class Game():
    def __init__(self, id):
        self.id = id
        self._draws = []

    @property 
    def id(self):
        return self._id

    @id.setter 
    def id(self, id):
        self._id = id
        
    def add_draw(self, draw):
        self._draws.append(draw)

    def is_possible(self, red_limit, green_limit, blue_limit):
        possible = 1
        for draw in self._draws:
            if ((draw.red > red_limit) or
               (draw.green > green_limit) or
               (draw.blue > blue_limit)):
                    possible = 0
                    break
        return possible

class GameLog():   
    def __init__(self):
        self._games = []

    def read_game_log(self, filename, debug):
        try:
            with open(filename, 'r') as fptr:
                for line in fptr:
                    if debug:
                        print (line, end='')
                    game_id, results = line.split(':')
                    match = re.search(r'^Game\s+(\d+)', game_id)
                    if match:
                       game = Game(int(match.group(1)))
                       self._games.append(game)

                    for draw_data in results.split(';'):
                        draw = CubeDraw()
                        game.add_draw(draw)
                        match = re.search(r'(\d+)\s+red', draw_data)
                        if match:
                            draw.red = int(match.group(1))

                        match = re.search(r'(\d+)\s+blue', draw_data)
                        if match:
                            draw.blue = int(match.group(1))

                        match = re.search(r'(\d+)\s+green', draw_data)
                        if match:
                            draw.green = int(match.group(1))


        except IOError:
            print(f"Error: Could not open \'{filename}\'")
            sys.exit(0)

    def analyze_game_log(self, red_limit, green_limit, blue_limit):
        sum = 0
        for game in self._games:
            if game.is_possible(red_limit, green_limit, blue_limit):
                sum += game.id
        return sum
     

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
    game_log = GameLog()
    args = parse_commandline()
    game_log.read_game_log(args.puzzle, args.debug)
    sum = game_log.analyze_game_log(12, 13, 14)
    print(f'Sum of possible games IDs is: {sum}')

if __name__ == '__main__':
    main()