class Vertex:

    def __init__(self, x, y, color="black"):
        self.__x = x
        self.__y = y

        self.weight = 0
        self.__index = 0
        self.color = color

    def get_coords(self):
        return self.__x, self.__y

    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y

    def __lt__(self, other):
        x_self, y_self = self.get_coords()
        x_other, y_other = other.get_coords()
        if y_self != y_other:
            return y_self < y_other
        else:
            return x_self < x_other

    def set_index(self, index):
        self.__index = index

    def get_index(self):
        return self.__index

    def __str__(self):
        x, y = self.get_coords()
        return "({}, {}, index={}, weight={})".format(x, y, self.__index, self.weight)

    def __eq__(self, other):
        return self.get_coords() == other.get_coords()

    def __hash__(self):
        return hash(self.__index)
