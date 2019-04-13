import os
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog,\
    QProgressBar,QMessageBox, QTableWidgetItem, QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from .player import Player
from .tag_extractor import TagExtractor


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

    def play(self):
        if Tag.bool_:
            self.player.play()
            Tag.bool_ = False
        self.player.unpause()

    def pause(self):
        self.player.pause()

    def stop(self):
        self.player.stop()
        Tag.bool_ = True

    def show_quit_message(self):

        reply = QMessageBox.question(self, 'Quit massage', 'Are you sure want'
                                                           'to exit Music Tag'
                                                           'Viever?',
                                     QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.ui.close()

    def show_file_dialog(self):
        self.files.clear()
        if not Tag.bool_:
            self.stop()
        file_name = QFileDialog.getOpenFileName(self, 'Open file', '/home',
                                                '*.mp3')[0]
        if file_name:
            self.files.append(TagExtractor(file_name))
        self.update_tracks_table()

    def show_folder_dialog(self):
        self.files.clear()
        if not Tag.bool_:
            self.stop()
        folders_items = QFileDialog\
            .getExistingDirectory(self, 'Open folder', '/home',
                                  QFileDialog.ShowDirsOnly
                                  | QFileDialog.DontResolveSymlinks)
        completed = 0  # for progress bar
        self.progressBar.setMaximumSize(180, 20)
        self.progressBar.addPermanentWidget(self.progressBar)
        self.statusBar.showMessage('Load songs...')
        if folders_items:
            for item in os.listdir(folders_items):
                path = folders_items + '/' + item
                if os.path.isfile(path):
                    self.files.append(
                        TagExtractor(folders_items + '/' + item))
                else:
                    continue
                self.progressBar.setValue(completed)
                completed += 100 / len(os.listdir(folders_items)) + 0.1
        self.progressBar.close()
        self.stetusBar.showMessage('Added' + str(len(self.files)) + ' tracks')

        self.update_tracks_table()

    def update_tag_table(self, file):
        for count in range(1, 2):
            for row, tag in enumerate(self.tags_str_keys):
                new_item = QTableWidgetItem(file.track_info[tag])
                self.tagsTable.setItem(row, count, new_item)
                if count < 2:
                    t_item = self.tagsTable.item(row, count)
                    t_item.setFlags(
                        Qt.ItemIsDragEnabled | Qt.ItemIsUserCheckable
                        | Qt.ItemIsEnabled)


