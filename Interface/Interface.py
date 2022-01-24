from tkinter import *


class Interface(Tk):

    WIDTH = 1800
    HEIGHT = 1000

    def __init__(self):
        super().__init__()

        self.geometry("{}x{}".format(self.WIDTH, self.HEIGHT))
        # self.resizable(width=False, height=False)

