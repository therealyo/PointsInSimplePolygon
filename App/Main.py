from Interface.Interface import Interface
from Interface.MainWindow import MainWindow


def main():
    app = Interface()
    window = MainWindow(app)
    app.mainloop()


if __name__ == "__main__":
    main()
