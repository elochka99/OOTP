from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog,\
    QProgressBar,QMessageBox, QTableWidgetItem, QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon


class Tag(QMainWindow):
    bool_ = True #for player (play/pause)

    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi('tag_editor.ui')
        self.ui.setWindowTitle('Music Tag Viewer')
        self.ui.setWindowIcon(QIcon(':/icons/icons/window_icon.png'))
        self.ui.setWindowFlags(Qt.WindowMinimizeButtonHint |
                               Qt.WindowMaximizeButtonHint)
        self.statusBar = self.ui.statusBar()
        self.tracksTable = self.ui.tableWidgetItems
        self.tagsTable = self.ui.tableWidget
        self.progressBar = QProgressBar()

        self.files = []
        self.current_file_index = 0
        self.tags_str_keys = ['artist', 'title', 'album', 'genre',
                              'tracknuber', 'date', 'quality']

        stylesheet = "::section{Background-color:rgb(204,204,204);}"
        self.tracksTable.horizontalHeader().setStyleSheet(stylesheet)
        self.tagsTable.horizontalHeader().setStyleSheet(stylesheet)




