class Edge:

    def __init__(self, begin, end, location="in", weight=1):

        if begin < end:
            self.__begin = begin
            self.__end = end

        else:
            self.__begin = end
            self.__end = begin

        self.location = location

        self.weight = weight
        self.__index = 0

    def get_edge(self):
        return self.__begin, self.__end

    def set_index(self, index):
        self.__index = index

    def get_index(self):
        return self.__index

    def get_begin(self):
        return self.__begin

    def get_end(self):
        return self.__end

    def set_begin(self, begin):
        self.__begin = begin

    def set_end(self, end):
        self.__end = end

    def __str__(self):
        return "{} -> {}, edge_index={}, location={}, weight={}".format(self.__begin, self.__end, self.__index, self.location, self.weight)

    def __lt__(self, other):
        self_begin, self_end = self.get_edge()
        other_begin, other_end = other.get_edge()

        if self_begin != other_begin:
            return self_begin < other_begin

        else:
            return self_end < other_end

    def get_orientation(self, vertex):
        x, y = vertex.get_coords()

        if y >= self.__end.get_y() or y <= self.__begin.get_y():
            return False
        else:
            return self.get_side(vertex)

    def get_side(self, vertex):
        if self.__count_pseudoscalar_product(vertex) > 0:
            return "right"
        elif self.__count_pseudoscalar_product(vertex) < 0:
            return "left"
        else:
            return "on edge"

    def __count_pseudoscalar_product(self, vertex):
        vector1 = (self.__end.get_x() - self.__begin.get_x(), self.__end.get_y() - self.__begin.get_y())
        vector2 = (vertex.get_x() - self.__begin.get_x(), vertex.get_y() - self.__begin.get_y())

        return vector1[0] * vector2[1] - vector1[1] * vector2[0]
