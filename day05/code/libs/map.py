"""
Define a Map class

This will have the source name, destination and the list of mappings
"""
from libs import RangeMapping

class Map():
    """
    Define the map class. Objects will have source and destination names and the
    list of range mappings from source to destination
    """
    def __init__(self, source, destination):
        self._mappings = []
        self.source = source
        self.destination = destination

    def add_mapping(self, destination, source, mapping_range):
        """
        Add a mapping from the puzzle definition

        Args:
            destination (str): Name of the destination
            source (string): Name of the string
            mapping_range (RangeMapping): the mapping between the source and
                                          destination
        """
        self._mappings.append(RangeMapping.RangeMapping(destination, source, mapping_range))

    def get_mapping(self, source):
        """
        Args:
            source (integer): the given source value.

        Returns:
            integer: The destination value, given the source value
        """
        retval = source
        for mapping in self._mappings:
            if source in mapping.source:
                offset = source - mapping.source.start
                retval = mapping.destination.start + offset
        return retval

    @property
    def source(self):
        """
        return the source name

        Returns:
            string: source name
        """
        return self._source

    @source.setter
    def source(self, source):
        """
        set the source name

        Args:
            source (string): the new source name
        """
        self._source = source

    @property
    def destination(self):
        """
        return the destination name
        Returns:
            string: the new destination name
        """
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

    def check_for_overlap(self, downstream):
        print(f'{self.source}')
        print(f'{downstream.source}')
        #dest = self.destination
        #dest.sort(key=lambda a: a.start)
        #for r in dest:
        #    print(f'{r.start}')

    def __str__(self):
        retval = []
        retval.append(f'{self.source} {self.destination}')
        retval.append('------ -----------')
        for j in range(100):
            retval.append(f'{j:^6} {self.get_mapping(j):^11}')
        return '\n'.join(retval)
