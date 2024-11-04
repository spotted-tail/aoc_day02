"""
Define the Range class
"""
class Range():
    """
    Define the range class. A range object will have a start and a stop integer,
    inclusive.
    """
    def __init__(self, start, range):
        self.start = start
        self.stop = start + range

    @property
    def start(self):
        """
        return the start value

        Returns:
            integer: the start value
        """
        return self._start

    @start.setter
    def start(self, start):
        """
        set the start value

        Args:
            start (integer): new start value
        """
        self._start = start

    @property
    def stop(self):
        """
        return the stop value

        Returns:
            integer: the stop value
        """
        return self._stop

    @stop.setter
    def stop(self, stop):
        """
        set the stop value

        Args:
            stop (integer): new stop value
        """
        self._stop = stop

    def __contains__(self, value):
        """
        override the in operator

        Args:
            value (_type_): _description_

        Returns:
            _type_: _description_
        """
        retval = False
        if value in range(self.start, self.stop):
            retval = True
        return retval

    def overlaps(self, other_range):
        """
        checks to see if the given range overlaps the object

        Args:
            other_range (Range): the range to check

        Returns:
            boolean: True = the range overlaps the object
        """
        retval = False
        if (self.start <= other_range.stop and other_range.start <= self.stop):
            retval = True
        return retval

    def completely_contains(self, other_range):
        """
        checks to see if the given range is completely contained by the object

        Args:
            other_range (Range): the range to check

        Returns:
            boolean: True = the range is completely overlaped bt the object
        """
        retval = False
        if (self.start <= other_range.start <= self.stop and
            self.start <= other_range.stop <= self.stop):
            retval = True
        return retval

    def should_fracture(self, other_range):
        """
        checks to see if the given range should be split since while it overlaps,
        it does not completely overlap the givien range

        Args:
            other_range (Range): the range to check

        Returns:
            boolean: True = the range is completely overlaped bt the object
        """

        retval = False
        if self.overlaps(other_range) and not self.completely_contains(other_range):
            retval = True
        return retval

    def __str__(self):
        retval = []
        retval.append(f'start: {self.start} stop: {self.stop}')
        return '\n'.join(retval)


def print_ranges(ranges):
    """
    print out the string representation of a list of ranges

    Args:
        ranges (list of Ranges): The list of ranges to print
    """
    print('Range inputs')
    for j, srange in enumerate(ranges):
        print(f'Range {j} = {srange}')
    print()


def check_overlaps(ranges):
    """
    print a table of overlap tests for a list of ranges.
    iterate over the list of ranges and determines which ones overlap./

    Args:
        ranges (list of Ranges): The list of ranges to check
    """
    print('Check over laps')
    print(' ', end = '')
    for j in range(len(ranges)):
        print(f'{j:2}', end = '')
    print()
    for j, y_range in enumerate(ranges):
        print(f'{j:<2}', end = '')
        for k, x_range in enumerate(ranges):
            if y_range.overlaps(x_range):
                print('Y ', end = '')
            else:
                print('N ', end = '')
        print()
    print()


def check_contains(ranges):
    """
    print a table of containing tests for a list of ranges.
    iterate over the list of ranges and determines which ones contain the others

    Args:
        ranges (list of Ranges): The list of ranges to check
    """
    print('Check completely contains')

    print(' ', end = '')
    for j in range(len(ranges)):
        print(f'{j:2}', end = '')
    print()
    for j, y_range in enumerate(ranges):
        print(f'{j:<2}', end = '')
        for k, x_range in enumerate(ranges):
            if y_range.completely_contains(x_range):
                print('Y ', end = '')
            else:
                print('N ', end = '')
        print()
    print()


def check_needs_to_be_split(ranges):
    """
    print a table of containing tests if a range should be split

    Args:
        ranges (list of Ranges): The list of ranges to check
    """
    print('Needs to be split')

    print(' ', end = '')
    for j in range(len(ranges)):
        print(f'{j:2}', end = '')
    print()
    for j, y_range in enumerate(ranges):
        print(f'{j:<2}', end = '')
        for k, x_range in enumerate(ranges):
            if y_range.should_fracture(x_range):
                print('Y ', end = '')
            else:
                print('N ', end = '')
        print()
    print()



def main():
    """
    Self test of the range class
    """
    ranges = []
    ranges.append(Range(1, 10))
    ranges.append(Range(5, 10))
    ranges.append(Range(2, 2))
    ranges.append(Range(20, 5))

    print_ranges(ranges)
    check_overlaps(ranges)
    check_contains(ranges)

if __name__ == '__main__':
    main()
