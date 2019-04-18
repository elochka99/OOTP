from PyQt5.QtWidgets import QApplication
from sys import argv, exit
from ControllerMainWindow import Main


if __name__ == "__main__":
    app = QApplication(argv)
    ex = Main()
    exit(app.exec())
