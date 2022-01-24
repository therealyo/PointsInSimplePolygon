from tkinter import *
import tkinter.font as font

import random

from Utility.Vertex import Vertex
from Utility.PolygonReader import PolygonReader


class MainWindow:

    DRAWABLE = False
    RADIUS = 2

    SETTINGS = {
        "Font": {"size": 22},
        "Canvas": {},
        "Main Window": {}
    }

    CHAINS_COLORS = ["red", "black", "yellow", "grey", "blue", "orange", "purple"]

    PLACE_OPTIONS = {
        "Drawable Button": {"relx": 0.01, "rely": 0.03, "relwidth": 32/192, "relheight": 10/108},
        "Random Button": {"relx": 0.01, "rely": 0.14, "relwidth": 32/192, "relheight": 10/108},
        "Clear Button": {"relx": 0.01, "rely": 0.87, "relwidth": 32/192, "relheight": 10/108},
        "Prev Button": {"relx": 0.75, "rely": 0.87, "relwidth": 25/192, "relheight": 10/108},
        "Next Button": {"relx": 0.87, "rely": 0.87, "relwidth": 25/192, "relheight": 10/108},
        "Canvas": {"relx": 0.18, "rely": 0.02, "relwidth": 107/192, "relheight": 105/108},
        "Input Label": {"relx": 0.01, "rely": 0.25, "relwidth": 30/192, "relheight": 5/108},
        "Input Field": {"relx": 0.01, "rely": 0.3, "relwidth": 30/192, "relheight": 5/108},
        "Input Button": {"relx": 0.14, "rely": 0.3, "relwidth": 7/192, "relheight": 5/108},
        "Show Button": {"relx": 0.77, "rely": 0.03, "relwidth": 40/192, "relheight": 10/108},
        "Current Button": {"relx": 0.77, "rely": 0.14, "relwidth": 40/192, "relheight": 10/108},
        "All Button": {"relx": 0.77, "rely": 0.25, "relwidth": 40 / 192, "relheight": 10 / 108},
        "Solve Button": {"relx": 0.77, "rely": 0.37, "relwidth": 40/192, "relheight": 10/108},
        "Main Window": {}
    }

    def __init__(self, container):
        self.points = []
        self.inside = []
        self.outside = []
        self.polygon_reader = PolygonReader()
        self.graphs = self.polygon_reader.get_graphs()
        self.container = container

        self.__create_widgets()

    def __create_widgets(self):
        button_font = font.Font(**self.SETTINGS["Font"])

        self.drawable_button = Button(self.container, text="Ввести самостійно", font=button_font)
        self.drawable_button["command"] = self.__allow_drawing
        self.drawable_button.place(**self.PLACE_OPTIONS["Drawable Button"])

        self.random_button = Button(self.container, text="Ввести випадково", font=button_font)
        self.random_button["command"] = self.__create_random_input_field
        self.random_button.place(**self.PLACE_OPTIONS["Random Button"])

        self.clear_button = Button(self.container, text="Очистити", font=button_font)
        self.clear_button["command"] = self.__clear_all
        self.clear_button.place(**self.PLACE_OPTIONS["Clear Button"])

        self.show_button = Button(self.container, text="Показати ланцюги", font=button_font)
        self.show_button["command"] = self.__show_regularized
        self.show_button.place(**self.PLACE_OPTIONS["Show Button"])

        self.next_button = Button(self.container, text="Показати багатокутник", font=button_font)
        self.next_button["command"] = self.__current_polygon
        self.next_button.place(**self.PLACE_OPTIONS["Current Button"])

        self.all_button = Button(self.container, text="Показати всі", font=button_font)
        self.all_button["command"] = self.__show_all
        self.all_button.place(**self.PLACE_OPTIONS["All Button"])

        self.solve_button = Button(self.container, text="Розв\'язок", font=button_font)
        self.solve_button["command"] = self.__solve
        self.solve_button.place(**self.PLACE_OPTIONS["Solve Button"])

        self.next_button = Button(self.container, text="Наступний", font=button_font)
        self.next_button["command"] = self.__next_polygon
        self.next_button.place(**self.PLACE_OPTIONS["Next Button"])

        self.prev_button = Button(self.container, text="Минулий", font=button_font)
        self.prev_button["command"] = self.__prev_polygon
        self.prev_button.place(**self.PLACE_OPTIONS["Prev Button"])

        self.canvas = Canvas(self.container, bg='#ffffff')
        self.canvas.bind("<Button-1>", self.__enter_by_hand)
        self.canvas.bind("<Button-3>", self.__stop_drawing)
        self.canvas.place(**self.PLACE_OPTIONS["Canvas"])

    def __allow_drawing(self):
        self.__clear_canvas()
        self.DRAWABLE = True

    def __stop_drawing(self, event=None):
        self.DRAWABLE = False

    def __create_random_input_field(self):
        self.text = Label(self.container, text="Введіть кількість точок: ", font=font.Font(size=15))
        self.text.place(**self.PLACE_OPTIONS["Input Label"])

        self.input_field = Entry(self.container, font=font.Font(size=15))
        self.input_field.place(**self.PLACE_OPTIONS["Input Field"])

        self.input_button = Button(self.container, text="OK")
        self.input_button["command"] = self.__random_input_points
        self.input_button.place(**self.PLACE_OPTIONS["Input Button"])

    def __random_input_points(self):
        self.__clear_all(True)

        amount_of_points = int(self.input_field.get())
        self.points = [(random.randrange(0, 850), random.randrange(0, 800)) for _ in range(amount_of_points)]
        self.points = [Vertex(point[0], point[1]) for point in self.points]

        self.__draw_points()
        self.__stop_drawing()

    def __draw_points(self):
        for point in self.points:
            self.__draw_point(point, point.color)

    def __draw_point(self, point, color="black"):
        x, y = point.get_coords()
        self.canvas.create_oval(x - self.RADIUS, y - self.RADIUS, x + self.RADIUS, y + self.RADIUS, fill=color, outline=color)

    def __draw_edge(self, edge):
        start, finish = edge.get_edge()
        x_start, y_start = start.get_coords()
        x_finish, y_finish = finish.get_coords()
        self.canvas.create_line(x_start, y_start, x_finish, y_finish, width=3)

    def __clear_all(self, state=False):
        self.points = []
        self.canvas.delete("all")
        if state:
            for polygon in self.polygon_reader.get_graphs():
                if polygon.showed:
                    self.__draw_polygon(polygon, clear=False)

    def __clear_canvas(self):
        self.canvas.delete("all")
        for polygon in self.polygon_reader.get_graphs():
            if polygon.showed:
                self.__draw_polygon(polygon, clear=False)

    def __enter_by_hand(self, event):
        if self.DRAWABLE:
            point = Vertex(event.x, event.y)
            x, y = point.get_coords()
            self.points.append(point)
            self.canvas.create_oval(x - self.RADIUS, y - self.RADIUS, x + self.RADIUS, y + self.RADIUS, fill="#000000")

    def __next_polygon(self):
        self.polygon_reader.current_polygon().showed = False
        polygon = self.polygon_reader.next_polygon()
        polygon.showed = True
        self.__draw_polygon(polygon)

    def __current_polygon(self):
        polygon = self.polygon_reader.current_polygon()
        self.__draw_polygon(polygon)

    def __prev_polygon(self):
        self.polygon_reader.current_polygon().showed = False
        polygon = self.polygon_reader.prev_polygon()
        polygon.showed = True
        self.__draw_polygon(polygon)

    def __draw_polygon(self, polygon, clear=True):
        if polygon.showed:
            if clear:
                self.__clear_canvas()
                self.__draw_points()

                for point in polygon.get_vertexes():
                    self.__draw_point(point)

                for edge in polygon.start_edges:
                    self.__draw_edge(edge)
            else:
                for point in polygon.get_vertexes():
                    self.__draw_point(point)

                for edge in polygon.start_edges:
                    self.__draw_edge(edge)

    def __show_regularized(self):
        self.__clear_canvas()
        self.__draw_points()

        polygon = self.polygon_reader.current_polygon()
        for point in polygon.get_vertexes():
            self.__draw_point(point)

        for chain in polygon.chains:
            # self.__draw_edge(edge)
            color = random.choice(self.CHAINS_COLORS)
            self.__draw_chain(chain, color)

    def __draw_chain(self, chain, color="black"):
        for edge in chain.edges:
            start, finish = edge.get_edge()
            x_start, y_start = start.get_coords()
            x_finish, y_finish = finish.get_coords()
            self.canvas.create_line(x_start, y_start, x_finish, y_finish, fill=color, width=3)

    def __show_all(self):
        for polygon in self.polygon_reader.graphs:
            polygon.showed = True
            self.__draw_polygon(polygon, clear=False)

    def __solve(self):
        self.__clear_canvas()
        showed = []
        for polygon in self.polygon_reader.graphs:
            if polygon.showed:
                for point in self.points:
                    if point not in showed:
                        point_state = polygon.is_inside(point)
                        if point_state == "outside":
                            color = "red"
                        else:
                            color = "green"
                            showed.append(point)

                        self.__draw_point(point, color)

