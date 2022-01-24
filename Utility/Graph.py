from Utility.Vertex import Vertex
from Utility.Edge import Edge
from Utility.Chain import Chain


class Graph:

    def __init__(self, points):
        self.showed = False
        self.__vertexes = points

        self.__edges = []
        self.__build_edges()
        self.start_edges = self.__edges[:]

        self.__sort_vertexes()
        self.__sort_edges()

        self.__first = self.__vertexes[0]
        self.__last = self.__vertexes[-1]
        self.__max_index_vertexes = len(self.__vertexes)
        self.__max_index_edges = 0

        self.__adjacency_list = None
        self.__build_adjacency_list()

        self.__count_weights_vertexes()
        #
        # print("Edges before regularization")
        # self.print_edges()

        self.regularization()

        # print("Edges after regularization")
        # self.print_edges()
        #

        self.chains = []
        self.__get_chains()

        # self.print_edges()

    def get_edges(self):
        return self.__edges

    def get_vertexes(self):
        return self.__vertexes

    def __build_edges(self):
        for i in range(len(self.__vertexes)):
            try:
                self.__edges.append(Edge(self.__vertexes[i], self.__vertexes[i + 1]))
            except IndexError:
                self.__edges.append(Edge(self.__vertexes[len(self.__vertexes) - 1], self.__vertexes[0]))

    def print_regularized(self):
        for edge in self.regularized:
            print(edge)

        print()

    def print_vertexes(self):
        for vertex in self.__vertexes:
            print(vertex)

        print()

    def print_edges(self):
        for edge in self.__edges:
            print(edge)

        print()

    def print_adjacency(self):

        for vert in self.__adjacency_list.keys():
            print(vert, "-> ", self.__adjacency_list[vert])

    def __sort_vertexes(self):
        self.__vertexes = sorted(self.__vertexes)
        for i in range(len(self.__vertexes)):
            self.__vertexes[i].set_index(str(i + 1))

    def __sort_edges(self):
        self.__edges = sorted(self.__edges)
        for i in range(len(self.__edges)):
            self.__edges[i].set_index(i + 1)

    def __build_adjacency_list(self):

        self.__adjacency_list = {vert: [] for vert in self.__vertexes}
        for edge in self.__edges:
            self.__adjacency_list[edge.get_begin()].append(edge.get_end())

    def __count_weights_vertexes(self):
        for el in self.__adjacency_list.values():
            for vert in el:
                if vert != self.__last:
                    vert.weight -= 1

        for vert in list(self.__adjacency_list.keys())[1:]:
            if self.__adjacency_list[vert]:
                vert.weight += len(self.__adjacency_list[vert])

    def __insert_edge(self, edge):
        self.__edges.append(edge)
        self.regularized = sorted(self.__edges)
        for i in range(len(self.__edges)):
            self.__edges[i].set_index(i + 1)

    def get_left_and_right_edge(self, vertex):
        possible = []

        for edge in self.__edges:
            if (edge.get_begin().get_y() < vertex.get_y()) and (edge.get_end().get_y() > vertex.get_y()):
                possible.append(edge)

        index = 0
        possible = self.__sort_edges_x(possible)

        for edge in possible:
            if edge.get_side(vertex) == "left":
                break
            index += 1

        if index == 0:
            return possible[index]
        else:
            try:
                return possible[index - 1], possible[index]
            except IndexError:
                return possible[index - 1]

    def all_points_between_two_edges(self, edge1, edge2, vert):
        points = []

        for vertex in self.__vertexes:

            on_line = (edge1.get_side(vertex) == "on edge" or edge2.get_side(vertex) == "on edge")
            if (edge1.get_side(vertex) != "right" or edge2.get_side(vertex) != "left") and not on_line:
                continue
            if vert.weight < 0:
                if vertex.get_y() >= vert.get_y() and vertex != vert:
                    points.append(vertex)

            elif vert.weight > 0:
                if vertex.get_y() <= vert.get_y() and vertex != vert:
                    points.append(vertex)

        return points

    def all_points_one_edge(self, edge, vert):
        points = []
        side = edge.get_side(vert)
        for vertex in self.__vertexes:
            if (edge.get_side(vertex) == "on edge") or (edge.get_side(vertex) == side):
                if vert.weight < 0:
                    if vertex.get_y() >= vert.get_y() and vertex != vert:
                        points.append(vertex)

                elif vert.weight > 0:
                    if vertex.get_y() <= vert.get_y() and vertex != vert:
                        points.append(vertex)

        return points

    def regularization(self):
        for vertex in self.__vertexes[1:-1]:
            edges = self.get_left_and_right_edge(vertex)

            if type(edges) == tuple:
                points = self.all_points_between_two_edges(edges[0], edges[1], vertex)
                points = sorted(points)

                if vertex.weight > 0:
                    self.__insert_edge(Edge(vertex, points[-1], weight=vertex.weight))
                    points[-1].weight += 1
                    vertex.weight = 0
                if vertex.weight < 0:
                    self.__insert_edge(Edge(vertex, points[0], weight=abs(vertex.weight)))
                    points[0].weight += 1
                    vertex.weight = 0
            else:
                points = self.all_points_one_edge(edges, vertex)
                points = sorted(points)

                if vertex.weight > 0:
                    self.__insert_edge(Edge(vertex, points[-1], "out", weight=vertex.weight))
                    points[-1].weight += 1
                    vertex.weight = 0
                if vertex.weight < 0:
                    self.__insert_edge(Edge(vertex, points[0], "out", weight=abs(vertex.weight)))
                    points[0].weight += 1
                    vertex.weight = 0

        self.__build_adjacency_list()

    def lefter(self, edge1, edge2):
        x_min = edge1.get_begin().get_x() if edge1.get_begin().get_x() < edge1.get_end().get_x() else edge1.get_end().get_x()
        x_begin, x_end = edge2.get_begin().get_x(), edge2.get_end().get_x()

        if x_min == x_begin:
            return x_end > edge1.get_end().get_x()

        return (x_begin > x_min) and (x_end > x_min)

    def __sort_edges_x(self, edges):
        for i in range(len(edges)):
            try:
                if self.lefter(edges[i], edges[i + 1]):
                    edges[i], edges[i + 1] = edges[i + 1], edges[i]
            except IndexError:
                continue

        return edges

    def __get_chains(self):
        self.__form_chains()
        self.__sort_chains()
        # for chain in self.chains:
        #     print(chain)

    def __form_chains(self):
        start_vertex = self.__vertexes[0]
        start_edges = self.get_edges_vertex(start_vertex)

        for edge in start_edges:

            while True:
                if edge.weight <= 0:
                    break
                chain = Chain()
                chain.append_edge(edge)
                edge.weight -= 1
                current = edge.get_end()

                if current == self.__vertexes[-1]:
                    chain.append_edge(edge)
                    self.chains.append(chain)
                    break

                while True:

                    next_edges = self.get_edges_vertex(current)
                    next_edge = next_edges[0]
                    for ed in next_edges:
                        if ed.weight != 0:
                            next_edge = ed
                            break

                    next_edge.weight -= 1

                    chain.append_edge(next_edge)
                    current = next_edge.get_end()

                    if current == self.__vertexes[-1]:
                        break

                self.chains.append(chain)

    def __sort_chains(self):
        self.chains = sorted(self.chains)

    def __edge_equal(self, vert_begin, vert_end, edge):
        if edge.get_edge() == (vert_begin, vert_end):
            return True

    def get_edges_vertex(self, vertex):
        edges = []

        for edge in self.__edges:

            if edge.get_begin() == vertex:
                edges.append(edge)

        return edges

    def get_next_edge(self, edge):
        end = edge.get_end()
        for ed in self.get_edges_vertex(end):
            if ed.weight != 0:
                ed.weight -= 1
                return ed

    def is_inside(self, vertex):
        left_chain, right_chain = self.find_chains(vertex)

        same = []
        if left_chain and right_chain:

            for edge in left_chain.edges:
                if edge in right_chain.edges:
                    same.append(edge)

            if not same:
                return "inside"

        if same:
            if len(same) > 1:
                return "outside"

            edge = same[0]
            if edge.location == "out":
                return "inside"
            else:
                return "outside"

        return "outside"

    def find_chains(self, vertex):
        right_chain = self.chains[0]
        left_chain = None

        if self.chains[-1].get_orientation(vertex) == "left":
            return self.chains[-1], None

        for i in range(len(self.chains)):
            if self.chains[i].get_orientation(vertex) == "left":
                right_chain = self.chains[i + 1]
                left_chain = self.chains[i]

        return left_chain, right_chain
