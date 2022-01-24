from Utility.Graph import Graph
from Utility.Vertex import Vertex


class PolygonReader:

    FILENAME = "../App/polygons.txt"

    def __init__(self):
        self.current_index = -1
        self.graphs = []

        self.__read_polygons()

    def __read_polygons(self):
        with open(self.FILENAME, "r") as finput:
            all_points = finput.read().split(sep="\n")
            while all_points:
                if "" in all_points:
                    point_delimiter = all_points.index("")
                    temp_points = all_points[:point_delimiter]
                    all_points = all_points[point_delimiter + 1:]

                    temp_points = [list(map(float, i.split())) for i in temp_points]

                    points = [Vertex(point[0], point[1]) for point in temp_points]
                    self.graphs.append(Graph(points))
                else:
                    all_points = [list(map(float, i.split())) for i in all_points]
                    points = [Vertex(point[0], point[1]) for point in all_points]
                    self.graphs.append(Graph(points))
                    all_points = []

    def get_graphs(self):
        return self.graphs

    def show_polygons(self):
        for polygon in self.graphs:
            polygon.print_edges()

    def current_polygon(self):
        return self.graphs[self.current_index]

    def next_polygon(self):
        if self.current_index == len(self.graphs) - 1:
            return self.graphs[self.current_index]

        else:
            self.current_index += 1
            return self.graphs[self.current_index]

    def prev_polygon(self):
        if self.current_index == -1:
            self.current_index += 1
            return self.graphs[self.current_index]

        elif self.current_index == 0:
            return self.graphs[self.current_index]

        else:
            self.current_index -= 1
            return self.graphs[self.current_index]

