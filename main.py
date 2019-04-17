import os
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog,\
    QProgressBar, QMessageBox, QTableWidgetItem, QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
# import resource_rс
from player import Player
from tag_extractor import TagExtractor
import webbrowser


class Tag(QMainWindow):
    """
    Gui class.

    This class contain main window and application gui.
    """
    bool_ = True  # for player (play/pause)

    def __init__(self):
        """
        class initialization function
        """
        super().__init__()
        self.ui = uic.loadUi('tag_editor.ui')
        self.ui.setWindowTitle('Music Tag Viewer')
        self.ui.setWindowIcon(QIcon(':/icons/icons/window_icon.png'))
        self.ui.setWindowFlags(Qt.WindowMinimizeButtonHint |
                               Qt.WindowMaximizeButtonHint | Qt.WindowCloseButtonHint)
        self.statusBar = self.ui.statusBar()
        self.tracksTable = self.ui.tracksTable
        self.tagsTable = self.ui.tagsTable
        self.progressBar = QProgressBar()

        # -- all imported tracks_information
        self.files = []
        self.current_file_index = 0
        self.tags_str_keys = ['artist', 'title', 'album', 'genre',
                              'tracknumber', 'date', 'quality']

        # -- set stylesheet
        stylesheet = "::section{Background-color:rgb(204,204,204);}"
        self.tracksTable.horizontalHeader().setStyleSheet(stylesheet)
        self.tagsTable.horizontalHeader().setStyleSheet(stylesheet)
        self.searchDialog = SearchDialog()  # for web search

        self.initUi()

    def initUi(self):
        """
        Initialize gui
        """

        # -- resize column
        self.tracksTable.resizeColumnToContents(1)
        # -- activate cell
        self.tracksTable.cellClicked.connect(self.cell_clicked) #coord

        # -- actions
        # add folder action
        add_folder_action = self.ui.actionAdd_Folder
        add_folder_action.triggered.connect(self.show_folder_dialog)

        # add file action
        add_file_action = self.ui.actionAdd_File
        add_file_action.triggered.connect(self.show_file_dialog)

        # close app action
        exit_action = self.ui.actionExit
        exit_action.triggered.connect(self.show_quit_message)

        # search on web action
        search_on_web_action = self.ui.actionSearch_on_Web
        search_on_web_action.triggered.connect(self.show_web_search_dialog)


        self.ui.show()

    def cell_clicked(self, r, c):
        """
        When cell clicked slot.

        :param r: row
        :param c: count
        """

        item = self.tracksTable.item(r, 2) #title
        for file in self.files:
            if item.text() == file.track_info['title']:
                self.statusBar.showMessage('Track size: {} mb File path: {}'
                                           .format(file.track_info['track_size'],
                                                   file.file_path))
                self.current_file_index = self.files.index(file)
                self.update_tag_table(file)
                # -- player actions
                # play action
                if Tag.bool_:
                    play_action = self.ui.actionPlay
                    # create instance of Player object
                    self.player = Player()
                    self.player.load(file.file_path)
                    Tag.bool_ = True
                    play_action.triggered.connect(self.play)

                    # pause action
                    pause_action = self.ui.actionPause
                    pause_action.triggered.connect(self.pause)

                # stop action
                stop_action = self.ui.actionStop
                stop_action.triggered.connect(self.stop)

    # -- slots for player
    def play(self):
        """
        use for start playing
        """
        if Tag.bool_:
            self.player.play()
            Tag.bool_ = False
        self.player.unpause()

    def pause(self):
        """
        use for pause playing
        """
        self.player.pause()

    def stop(self):
        """
        use for stop playing
        """
        self.player.stop()
        Tag.bool_ = True

    def show_quit_message(self):
        """
        Show quit window.
        """
        reply = QMessageBox.question(self, 'Quit massage', 'Are you sure want'
                                                           'to exit Music Tag'
                                                           'Viever?',
                                     QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.ui.close()
            self.searchDialog.ui.close()

    def show_file_dialog(self):
        """
        Displays file selection window.
        """
        self.files.clear()
        if not Tag.bool_:
            self.stop()
        file_name = QFileDialog.getOpenFileName(self, 'Open file', '/home',
                                                '*.mp3')[0]
        if file_name:
            self.files.append(TagExtractor(file_name))
        # update trackTable widget
        self.update_tracks_table()

    def show_folder_dialog(self):
        """
        Displays folder selection window
        """
        self.files.clear()
        if not Tag.bool_:
            self.stop()
        folder_items = QFileDialog \
            .getExistingDirectory(self, 'Open folder', '/home',
                                  QFileDialog.ShowDirsOnly
                                  | QFileDialog.DontResolveSymlinks)
        completed = 0  # for progress bar
        self.progressBar.setMaximumSize(180, 20)
        self.statusBar.addPermanentWidget(self.progressBar)
        self.statusBar.showMessage('Load songs...')
        # -- add TagExtractor objects to files list
        if folder_items:
            for item in os.listdir(folder_items):
                path = folder_items + '/' + item
                if os.path.isfile(path):
                    if path.endswith('.mp3'):
                        self.files.append(
                            TagExtractor(folder_items + '/' + item))
                else:
                    continue
                self.progressBar.setValue(completed)
                completed += 100 / len(os.listdir(folder_items)) + 0.1
        self.progressBar.close()
        self.statusBar.showMessage('Added' + str(len(self.files)) + ' tracks')
        # -- update trackTable widget
        self.update_tracks_table()

    def update_tag_table(self, file):
        """
        Fills the tag table with values.
        :param file: file
        """
        for count in range(1, 2):
            for row, tag in enumerate(self.tags_str_keys):
                new_item = QTableWidgetItem(file.track_info[tag])
                self.tagsTable.setItem(row, count, new_item)
                if count < 2:
                    t_item = self.tagsTable.item(row, count)
                    t_item.setFlags(
                        Qt.ItemIsDragEnabled | Qt.ItemIsUserCheckable
                        | Qt.ItemIsEnabled)

    def update_tracks_table(self):
        """
        Fills the track table with values.
        """
        self.tracksTable.setRowCount(len(self.files))
        keys = ['artist', 'length', 'title']
        for r, item in enumerate(self.files):
            for c, key in enumerate(keys):
                new_item = QTableWidgetItem(item.track_info[key])
                self.tracksTable.setItem(r, c, new_item)
                t_item = self.tracksTable.item(r, c)  # get item
                t_item.setFlags(Qt.ItemIsDragEnabled | Qt.ItemIsUserCheckable
                                | Qt.ItemIsEnabled)
                item_for_icon = self.tracksTable.item(r, 0)
                # set item icon
                item_for_icon.setIcon(QIcon(':/icons/icons/song_icon.png'))

    def show_web_search_dialog(self):
        """
        Slot.

        Activate web search dialog.
        """
        self.searchDialog.ui.show()


class SearchDialog(QWidget):
    """
    This class use for displays web search dialog.
    """
    def __init__(self):
        """
        class initialization function
        """
        super().__init__()
        self.ui = uic.loadUi('search_on_web.ui')
        self.ui.setWindowTitle('Search track on Web')
        self.ui.setWindowIcon(QIcon(':/icons/icons/web_search_icon.png'))
        self.ui.setWindowFlags(Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint)
        self.search_btn = self.ui.searchButton
        self.url = self.ui.url
        self.search_btn.clicked.connect(self.btn_clicked)

    def btn_clicked(self):
        """
        This function shows the action by pressing the button.
        """
        usr_inp = self.url.text()
        if usr_inp != '':
            webbrowser.open('https://soundcloud.com/search/sounds?q={}'.
                            format(usr_inp))
            self.ui.hide()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Tag()
    sys.exit(app.exec())
