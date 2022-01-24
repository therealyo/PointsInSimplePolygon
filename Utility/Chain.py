from Utility.Vertex import Vertex
from Utility.Edge import Edge


class Chain:

    def __init__(self):
        self.edges = []
        self.vertexes = []

        self.vertexes_amount = 0
        self.edges_amount = 0

    def append_edge(self, edge):
        if edge not in self.edges:
            self.append_vertex(edge.get_begin())
            self.append_vertex(edge.get_end())
            self.edges.append(edge)
            self.edges_amount += 1

    def append_vertex(self, vertex):
        if vertex not in self.vertexes:
            self.vertexes.append(vertex)
            self.vertexes_amount += 1

    def get_orientation(self, vertex):
        x, y = vertex.get_coords()

        if y >= self.vertexes[-1].get_y() or y <= self.vertexes[0].get_y():
            return False

        for edge in self.edges:
            if edge.get_end().get_y() > y:
                return edge.get_orientation(vertex)

    def __search_y(self, y):
        for i in range(self.vertexes_amount):
            max_y = self.vertexes[i].get_y()
            if y < max_y:
                return i

    def __str__(self):
        res = "Chain : \n"
        for edge in self.edges:
            res += str(edge) + "\n"

        return res

    def __lt__(self, other):
        if self.edges[0] == other.edges[0]:
            first, second = self.edges[1], other.edges[1]
        else:
            first, second = self.edges[0], other.edges[0]

        return first.get_end().get_x() < second.get_end().get_x()

    def __eq__(self, other):
        return self.edges == other.edges

    #
    # def __get_side(self, vertex, low, high):
    #     if self.__count_pseudoscalar_product(vertex) > 0:
    #         return "left"
    #     elif self.__count_pseudoscalar_product(vertex) < 0:
    #         return "right"
    #
    #     return "on line"



