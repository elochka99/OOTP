from pattern import singleton
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5 import uic

@singleton
class MainWindow(QMainWindow):
    """
    class for MainWindow viev
    """
    def __init__(self):
        """
        Initialize the CLASS.
        """
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
                show_web_search_dialog, play, pause, stop, volume):
        """
        Bind view elements to controller elements
        :param cell_clicked: action
        :param show_folder_dialog: action
        :param show_file_dialog: action
        :param show_quit_message: action
        :param show_web_search_dialog: action
        :param play: action
        :param pause: action
        :param stop: action
        :param volume: action
        """

        self.tracksTable.cellClicked.connect(cell_clicked)
        self.actionAdd_Folder.triggered.connect(show_folder_dialog)
        self.actionAdd_File.triggered.connect(show_file_dialog)
        self.actionExit.triggered.connect(show_quit_message)
        self.actionSearch_on_Web.triggered.connect(show_web_search_dialog)
        self.actionPlay.triggered.connect(play)
        self.actionPause.triggered.connect(pause)
        self.actionStop.triggered.connect(stop)
        self.volume.valueChanged.connect(volume)