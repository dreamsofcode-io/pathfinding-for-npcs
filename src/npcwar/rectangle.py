class Rectangle2D:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def __str__(self):
        return f"Rectangle2D({self.x}, {self.y}, {self.width}, {self.height})"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.width == other.width and self.height == other.height

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash((self.x, self.y, self.width, self.height))

    def __contains__(self, other):
        return self.x <= other.x <= self.x + self.width and self.y <= other.y <= self.y + self.height

    def __iter__(self):
        yield self.x
        yield self.y
        yield self.width
        yield self.height

    def __getitem__(self, item):
        if item == 0:
            return self.x
        elif item == 1:
            return self.y
        elif item == 2:
            return self.width
        elif item == 3:
            return self.height
        else:
            raise IndexError(f"Index {item} out of range")

    def __setitem__(self, key, value):
        if key == 0:
            self.x = value
        elif key == 1:
            self.y = value
        elif key == 2:
            self.width = value
        elif key == 3:
            self.height = value
        else:
            raise IndexError(f"Index {key} out of range")

    def __len__(self):
        return 4

    def __add__(self, other):
        return Rectangle2D(self.x + other.x, self.y + other.y, self.width + other.width, self.height + other.height)

    def __sub__(self, other):
        return Rectangle2D(self.x - other.x, self.y - other.y, self.width - other.width, self.height - other.height)

    def __mul__(self, other):
        return Rectangle2D(self.x * other.x, self.y * other.y, self.width * other.width, self.height * other.height)
