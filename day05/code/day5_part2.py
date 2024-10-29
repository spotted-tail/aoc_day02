import sys
import re
import argparse

class Range():
    def __init__(self, start, range):
        self.start = start
        self.stop = start + range

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

    def __contains__(self, value):
        retval = False
        if value in range(self.start, self.stop):
            retval = True
        return retval

    def overlaps(self, other_range):
        retval = False
        if (self.start < other_range.stop and other_range.start < self.stop): 
            retval = True
        return retval

    def completely_contains(self, range):
        retval = False
        if (self.start <= range.start < self.stop and
            self.start <= range.stop < self.stop):
            retval = True
        return retval

    def __str__(self):
        retval = []
        retval.append(f'start: {self.start} stop: {self.stop}')
        return '\n'.join(retval)


class RangeMapping():
    def __init__(self, destination, source, range):
        self.destination = Range(destination, range)
        self.source = Range(source, range)

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
        retval.append(f'source {self.source}')
        retval.append(f'destination {self.destination}')
        return '\n'.join(retval)


class Map():
    def __init__(self, source, destination):
        self._mappings = []
        self.source = source
        self.destination = destination

    def add_mapping(self, destination, source, mapping_range):
        self._mappings.append(RangeMapping(destination, source, mapping_range))

    def get_mapping(self, source):
        retval = source
        for mapping in self._mappings:
            if source in mapping.source:
                offset = source - mapping.source.start
                retval = mapping.destination.start + offset
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

    def has_range_overlaps(self, debug = 0):
        retval = False
        for j in range(len(self._mappings) - 1):
            for k in range(j+1, len(self._mappings)):
                if self._mappings[j].source.overlaps(self._mappings[k].source):
                    if debug:
                        print(f'{self._mappings[j].source} overlaps '
                              f'{self._mappings[k].source}')
                    retval = True
                    break
        return retval

    def __str__(self):
        retval = []
        retval.append(f'{self.source} {self.destination}')
        retval.append(f'------ -----------')
        for j in range(100):
            retval.append(f'{j:^6} {self.get_mapping(j):^11}')
        return '\n'.join(retval)


class Almanac():
    def __init__(self):
        self.seeds = []
        self._maps = {}

    @property 
    def ranges(self):
        return self._ranges

    @ranges.setter 
    def ranges(self, ranges):
        self._ranges = ranges

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
                        self.seeds = []
                        seed_input = match.group(1).split(' ')
                        for j in range(int(len(seed_input)/2)):
                            seed_range = Range(int(seed_input[j*2]), 
                                               int(seed_input[j*2 + 1]))
                            self.seeds.append(seed_range)

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
                            map.add_mapping(int(match.group(1)), 
                                            int(match.group(2)), 
                                            int(match.group(3)))

        except IOError:
            print(f"Error: Could not open \'{filename}\'")
            sys.exit(0)
        self.check_almanac()

    def check_almanac(self):
        errors = 0
        for map in self._maps.values():
            if map.has_range_overlaps():
                errors += 1
                print (f'ERROR: map {map.source}_to_{map.destination} '
                       f'has overlapping ranges')
        if not errors:
            print (f'Almanac passed consistency checking')
          
    def print_map(self, map_name):
        print (f'{self._maps[map_name]}')
        
    def traverse_maps(self):
        source_maps = self.create_list_of_source_maps()
        for source in source_maps:
            map = self._maps[source]
            print (f'Have a map from {map.source} to {map.destination}')

    def create_list_of_source_maps(self):
        source_maps = ['seed']
        done = False
        while not done:
            map = self._maps[source_maps[-1]]
            if map.destination in self._maps:
                source_maps.append(map.destination)
            else:
                done = True
        return source_maps
    
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

    # def find_location(self, seed):
    #     source = 'seed'
    #     value = seed
    #     while True:
    #         map = self._maps[source]
    #         destination = map.destination
    #         value = map.get_mapping(value)
    #         if destination in self._maps:
    #             source = destination
    #         else:
    #             return value

    # def fracture_ranges(self, debug=0):
    #     source_maps = self.create_list_of_source_maps()
    #     source_maps.reverse()
    #     map_count = len(source_maps)
    #     for k in range(map_count):
    #         if debug:
    #             print (f'Fracturing ranges in {map.source} based on {map.destination}')
    #         if k == map_count:
    #             print("Fracture seeds")
    #         else:
    #             source_map = self._maps[source_maps[k+1]]
    #             target_map = self._maps[source_maps[k]]
    #             source_map.fracture_ranges(target_map)

    # def find_min_location_in_range(self, start, range):
    #     map = self._maps['seed']
    #     values = map.get_min_value_in_range(start, range)
    #     return min(values)

    def print_seeds(self):
        print('Seed Ranges')
        for j in range(len(self.seeds)):
            print(f'{self.seeds[j]}')

    # def check_seed_overlap(self):
    #     seed = self.seeds[1]
    #     range = self.ranges[1]+50
    #     seed_map = self._maps['seed']
    #     is_contained = seed_map.soley_contained(seed, range)
    #     if is_contained: 
    #         print(f'{seed} {range} is completely contained in seed to soil map')
    #     else:
    #         print(f'{seed} {range} is completely NOT contained in seed to soil map')

    # def find_min_location(self):
    #     self.print_seeds()
    #     self.check_seed_overlap()

        # min_location = None
        # for j in range(len(self.seeds)):
        #     value = self.find_min_location_in_range(self.seeds[j], self.ranges[j])
        #     if min_location:
        #         min_location = min(min_location, value)
        #     else:
        #         min_location = value
        # print(f'The lowest location number in this example is {min_location}.')


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
        almanac.print_map('seed')
        # almanac.print_seeds()
        # almanac.traverse_maps()
        # almanac.resolve_mapping()
    #almanac.find_min_location()
 
if __name__ == '__main__':
    main()