from functools import total_ordering

@total_ordering
class Point:
    """Simple 2-dimensional point."""
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return not self == other

    def __lt__(self, other):
        return self.manhattan < other.manhattan

    def __str__(self):
        return "({}, {})".format(self.x, self.y)

    def __hash__(self):
        return hash(tuple((self.x, self.y)))

    @property
    def manhattan(self):
        return abs(self.x) + abs(self.y)
