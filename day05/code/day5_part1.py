import sys
import re
import argparse

class Range():
    def __init__(self, destination, source, range):
        self.destination = destination
        self.source = source
        self.range = range

    @property 
    def range(self):
        return self._range

    @range.setter 
    def range(self, range):
        self._range = range

    @property 
    def source(self):
        return self._source

    @source.setter 
    def source(self, source):
        self._source = source

    @property 
    def destination(self):
        return self._destination

    @destination.setter 
    def destination(self, destination):
        self._destination = destination


class Map():
    def __init__(self, source, destination):
        self._ranges = []
        self.source = source
        self.destination = destination

    def add_range(self, destination, source, mapping_range):
        self._ranges.append(Range(destination, source, mapping_range))

    def get_mapping(self, source):
        retval = source
        for range in self._ranges:
            if range.source <= source < range.source + range.range:
                retval = range.destination + (source - range.source)
        return retval

    @property 
    def source(self):
        return self._source

    @source.setter 
    def source(self, source):
        self._source = source

    @property 
    def destination(self):
        return self._destination

    @destination.setter 
    def destination(self, destination):
        self._destination = destination
    
    def __str__(self):
        retval = []
        retval.append(f'{self.source} {self.destination}')
        retval.append(f'------ -----------')
        for j in range(100):
            retval.append(f'{j:^6} {self.get_mapping(j):^11}')
        return '\n'.join(retval)
                          
class Almanac():
    def __init__(self):
        self.sum = 0
        self.seeds = []
        self._maps = {}

    @property 
    def sum(self):
        return self._sum

    @sum.setter 
    def sum(self, sum):
        self._sum = sum

    @property 
    def seeds(self):
        return self._seeds

    @seeds.setter 
    def seeds(self, seeds):
        self._seeds = seeds

    def read_almanac(self, filename, debug=0):
        have_map = 0
        try:
            with open(filename, 'r') as fptr:
                for line in fptr:
                    # Parse the seeds
                    match = re.search(r'^seeds:\s+(.+)$', line)
                    if match:
                        seeds = []
                        for seed in match.group(1).split(' '):
                            seeds.append(int(seed))
                        self.seeds = seeds
                    # Parse the maps
                    match = re.search(r'^(\S+?)\-to\-(\S+)\s+map:', line)
                    if match:
                        source = match.group(1)
                        destination = match.group(2)
                        map = Map(source, destination)
                        self._maps[source] = map
                        have_map = 1
                        if debug:
                            print (f'Source={source}, Destination={destination}')

                    if have_map == 1:
                        match = re.search(r'^\s*$', line)
                        if match:
                            have_map = 0

                        match = re.search(r'^(\d+)\s+(\d+)\s+(\d+)', line)
                        if match:
                            map.add_range(int(match.group(1)), 
                                          int(match.group(2)), 
                                          int(match.group(3)))

        except IOError:
            print(f"Error: Could not open \'{filename}\'")
            sys.exit(0)

    def print_map(self, map_name):
        print (f'{self._maps[map_name]}')
        
    def print_soil_numbers(self):
        map = self._maps['seed']
        for seed in self.seeds:
            print (f'- Seed number {seed} corrresponds '
                   f'to soil number {map.get_mapping(seed)}')

    def traverse_maps(self):
        done = False
        source = 'seed'
        while not done:
            map = self._maps[source]
            destination = map.destination
            print (f'Have a map from {source} to {destination}')
            if destination in self._maps:
                source = destination
            else:
                done = True

    def resolve_mapping(self):
        for seed in self.seeds:
            done = False
            source = 'seed'
            value = seed
            print(f'- Seed {seed}', end='')
            while not done:
                map = self._maps[source]
                destination = map.destination
                print(f', {destination} {map.get_mapping(value)}', end='')
                value = map.get_mapping(value)
                if destination in self._maps:
                    source = destination
                else:
                    done = True
            print('.')

    def find_min_location(self):
        min_location = None
        for seed in self.seeds:
            done = False
            source = 'seed'
            value = seed
            while not done:
                map = self._maps[source]
                destination = map.destination
                value = map.get_mapping(value)
                if destination in self._maps:
                    source = destination
                else:
                    if min_location:
                        min_location = min(min_location, value)
                    else:
                        min_location = value
                    done = True
        print(f'The lowest location number in this example is {min_location}.')

    def print_seeds(self):
        for seed in self.seeds:
            print(seed)

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
    almanac = Almanac()
    args = parse_commandline()
    almanac.read_almanac(args.puzzle)
    if args.debug:
        #almanac.print_map('seed')
        almanac.print_seeds()
        #almanac.print_soil_numbers()
        #almanac.traverse_maps()
    almanac.resolve_mapping()
    almanac.find_min_location()
 
if __name__ == '__main__':
    main()