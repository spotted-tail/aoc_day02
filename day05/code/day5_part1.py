import sys
import re
import argparse
class Map():
    def __init__(self, source, destination):
        self._map = []
        self._map_size = 100
        self.source = source
        self.destination = destination
        for j in range (self._map_size):
            self._map.append(j) 

    def update_mapping(self, destination, source, mapping_range):
        #print(f'Source {source}, Destination {destination}, Range {mapping_range}')
        for j in range(mapping_range):
            #print(f'J {j} Source {source+j}, Destination {destination+j}')
            self._map[source + j] = destination + j

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

    def get_mapping(self, source):
        return self._map[source]
    
    def __str__(self):
        retval = []
        retval.append(f'{self.source} {self.destination}')
        retval.append(f'------ -----------')
        for j in range (self._map_size):
            retval.append(f'{j:^6} {self._map[j]:^11}')
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

                # if debug:
                #     print (line, end='')

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
                            map.update_mapping(int(match.group(1)), 
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
        min_location = 200
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
                    min_location = min(min_location, value)
                    done = True
        print(f'The lowest location number in this example is {value}.')


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
    almanac.read_almanac(args.puzzle, args.debug)
    # almanac.print_map('seed')
    # almanac.print_soil_numbers()
    #almanac.resolve_mapping()
    #almanac.traverse_maps()
    almanac.find_min_location()
 
if __name__ == '__main__':
    main()