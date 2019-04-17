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
        self.setWindowFlags(Qt.WindowMinimizeButtonHint
                            | Qt.WindowMaximizeButtonHint
                            | Qt.WindowCloseButtonHint)
        stylesheet = "::section{Background-color:rgb(204,204,204);}"
        self.tracksTable.horizontalHeader().setStyleSheet(stylesheet)
        self.tagsTable.horizontalHeader().setStyleSheet(stylesheet)
        self.tracksTable.resizeColumnToContents(1)

    def trigger(self, cell_clicked, show_folder_dialog,
                show_file_dialog, show_quit_message,
                show_web_search_dialog, play, pause, stop):

        self.tracksTable.cellClicked.connect(cell_clicked)
        self.actionAdd_Folder.triggered.connect(show_folder_dialog)
        self.actionAdd_File.triggered.connect(show_file_dialog)
        self.actionExit.triggered.connect(show_quit_message)
        self.actionSearch_on_Web.triggered.connect(show_web_search_dialog)
        self.actionPlay.triggered.connect(play)
        self.actionPause.triggered.connect(pause)
        self.actionStop.triggered.connect(stop)
