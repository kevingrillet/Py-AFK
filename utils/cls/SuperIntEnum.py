from enum import IntEnum


class SuperIntEnum(IntEnum):
    # https://stackoverflow.com/a/61438054
    # https://stackoverflow.com/a/38017095
    def _generate_next_value_(self, start, count, last_values):
        return count

    def first(self):
        """
            return first element of the enum
        """
        cls = self.__class__
        members = list(cls)
        if len(members) == 0:
            raise ValueError('Enumeration has no values')
        return members[0]

    def last(self):
        """
            return last element of the enum
        """
        cls = self.__class__
        members = list(cls)
        if len(members) == 0:
            raise ValueError('Enumeration has no values')
        return members[-1]

    def prev(self, step=1):
        """
            return previous element of the enum
        """
        cls = self.__class__
        members = list(cls)
        index = members.index(self) - step
        if index < 0:
            raise StopIteration('Enumeration ended')
        return members[index]

    def next(self, step=1):
        """
            return next element of the enum
        """
        cls = self.__class__
        members = list(cls)
        index = members.index(self) + step
        if index >= len(members):
            raise StopIteration('Enumeration ended')
        return members[index]
