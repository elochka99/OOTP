from pattern import singleton
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5 import uic

@singleton
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('tag_editor.ui', self)
        self.setWindowTitle('Music Tag Viewer')
        self.setWindowIcon(QIcon('icons/window_icon.png'))
        self.setWindowFlags(Qt.WindowMinimizeButtonHint | Qt.WindowMaximizeButtonHint | Qt.WindowCloseButtonHint)
        stylesheet = "::section{Background-color:rgb(204,204,204);}"
        self.tracksTable.horizontalHeader().setStyleSheet(stylesheet)
        self.tagsTable.horizontalHeader().setStyleSheet(stylesheet)
        self.tracksTable.resizeColumnToContents(1)
