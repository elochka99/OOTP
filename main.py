from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog,\
    QProgressBar,QMessageBox, QTableWidgetItem, QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from .player import Player


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

    def initUi(self):
        """
        Initialize gui
        """

        self.tracksTable.resizeColumnToContents(1)
        self.tracksTable.cellClicked.connect(self.cell_clicked) #coord

        add_folder_action = self.ui.actionAdd_Folder
        add_folder_action.triggered.connect(self.show_folder_dialog)

        add_file_action = self.ui.actionAdd_File
        add_file_action.triggered.connect(self.show_file_dialog)

        exit_action = self.ui.actionExit
        exit_action.triggered.connect(self.show_quit_message)

        self.ui.show()

    def cell_clicked(self, r, c):

        item = self.tracksTable.item(r, 2) #title
        for file in self.files:
            if item.text() == file.track_info['title']:
                self.statusBar.showMessage('Track size: {} mb File path: {}'
                                           .format(file.track_info['track_size'],
                                                   file.file_path))
                self.current_file_index = self.files.index(file)
                self.update_tag_table(file)

                if Tag.bool_:
                    play_action = self.ui.actionPlay

                    self.player = Player(file.file_path)
                    Tag.bool_ = True
                    play_action.triggered.connect(self.play)

                    pause_action = self.ui.actionPause
                    pause_action.triggered.connect(self.pause)

                stop_action = self.ui.actionStop
                stop_action.triggered.connect(self.stop)





