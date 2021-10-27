from enum import IntEnum


class SuperIntEnum(IntEnum):
    # https://stackoverflow.com/a/61438054
    # https://stackoverflow.com/a/38017095
    def _generate_next_value_(self, start, count, last_values):
        return count

    def first(self):
        if len(list(self.__class__)) == 0:
            raise ValueError('Enumeration has no values')
        return SuperIntEnum(0)

    def last(self):
        if len(list(self.__class__)) == 0:
            raise ValueError('Enumeration has no values')
        return SuperIntEnum(len(list(self.__class__)))

    def pred(self, step=1):
        v = self.value - step
        if v == 0:
            raise ValueError('Enumeration ended')
        return SuperIntEnum(v)

    def succ(self, step=1):
        v = self.value + step
        if v > len(list(self.__class__)):
            raise ValueError('Enumeration ended')
        return SuperIntEnum(v)
