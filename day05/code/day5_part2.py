"""
Script to solve AOX 2023/Day 5/part 2
"""
import sys
import re
import argparse
from libs import range
from libs import map


class Almanac():
    """
    A class to define the puzzle Almanca
    """
    def __init__(self):
        self.seeds = []
        self._maps = {}

    # @property
    # def ranges(self):
    #     """
    #     retrun
    #     Returns:
    #         _type_: _description_
    #     """
    #     return self._ranges

    # @ranges.setter
    # def ranges(self, ranges):
    #     self._ranges = ranges

    @property
    def seeds(self):
        """
        return the list of seed ranges

        Returns:
            list of ranges: the list of seeds in the range
        """
        return self._seeds

    @seeds.setter
    def seeds(self, seeds):
        """
        Set the list of seed ranges

        Args:
            seeds (_type_): _description_
        """
        self._seeds = seeds

    def read_almanac(self, filename, debug=0):
        """
        Read the puzzle input

        Args:
            filename (string): puzzle input filename
            debug (int, optional): Set to 1 to get verbose output while reading.
                                   Defaults to 0.
        """
        have_map = 0
        try:
            with open(filename, 'r', encoding='utf8') as fptr:
                for line in fptr:
                    # Parse the seeds
                    match = re.search(r'^seeds:\s+(.+)$', line)
                    if match:
                        self.seeds = []
                        seed_input = match.group(1).split(' ')
                        for j in range(int(len(seed_input)/2)):
                            seed_range = range.Range(int(seed_input[j*2]),
                                                     int(seed_input[j*2 + 1]))
                            self.seeds.append(seed_range)

                    # Parse the maps
                    match = re.search(r'^(\S+?)\-to\-(\S+)\s+map:', line)
                    if match:
                        source = match.group(1)
                        destination = match.group(2)
                        map = map.Map(source, destination)
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
        """
        Perform a sanity check on the puzzle input
        """
        errors = 0
        for map in self._maps.values():
            if map.has_range_overlaps():
                errors += 1
                print (f'ERROR: map {map.source}_to_{map.destination} '
                       f'has overlapping ranges')
        if not errors:
            print ('Almanac passed consistency checking')

    def print_map(self, map_name):
        """
        print the given map name
        Args:
            map_name (_type_): _description_
        """
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

    def trial_fracture(self, debug=0):
        source_maps = self.create_list_of_source_maps()
        source_maps.reverse()
        source_map = self._maps[source_maps[1]]
        target_map = self._maps[source_maps[0]]
        source_map.check_for_overlap(target_map)


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
        """
        Print the seed ranges
        """
        print('Seed Ranges')
        for seed in enumerate(self.seeds):
            print(f'{seed}')

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
    """
    provide command line arguments

    Returns:
        Namespace: Command line args
    """
    # Instantiate the parser
    parser = argparse.ArgumentParser(description='Optional app description')

    parser.add_argument('-p', '--puzzle', type=str,
                        help='Filename for the puzzle')

    parser.add_argument('-d', '--debug',
                        action="store_true",
                        help='Turn on verbosity')

    return parser.parse_args()


def main():
    """
    main program to solve the day5 puzzle. Read the almanac and print the
    answer
    """
    almanac = Almanac()
    args = parse_commandline()
    almanac.read_almanac(args.puzzle)
    if args.debug:
        # almanac.print_map('seed')
        # almanac.print_seeds()
        almanac.traverse_maps()
        # almanac.resolve_mapping()
        almanac.trial_fracture(debug=0)

    #almanac.find_min_location()

if __name__ == '__main__':
    main()
