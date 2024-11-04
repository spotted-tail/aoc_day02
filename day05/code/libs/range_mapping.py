"""
Define a range mapping class
"""
from libs import range

class RangeMapping():
    """
    Define a range mapping object. This will basically create a link between
    two range objects
    """
    def __init__(self, destination, source, span):
        self.destination = Range(destination, span)
        self.source = Range(source, span)

    @property
    def source(self):
        """
        return the source range

        Returns:
            Range: The source range
        """
        return self._source

    @source.setter
    def source(self, source):
        """
        Set the source range

        Args:
            source (Range): the new source range
        """
        self._source = source

    @property
    def destination(self):
        """
        return the destination range

        Returns:
            Range: the destination range
        """
        return self._destination

    @destination.setter
    def destination(self, destination):
        """
        set the destination range

        Args:
            destination (Range): the new destination range
        """
        self._destination = destination

    def __str__(self):
        """
        string operator for the RangeMapping class

        Returns:
            string: String representation of RangeMapping
        """
        retval = []
        retval.append(f'source {self.source}')
        retval.append(f'destination {self.destination}')
        return '\n'.join(retval)


def main():
    """
    provides self-test for the object
    """
    mappings = []
    mappings.append(RangeMapping(55, 95, 2))
    print(f'{mappings[0]}')

if __name__ == '__main__':
    main()
